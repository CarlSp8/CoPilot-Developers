"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

SECURITY NOTES FOR PRODUCTION:
- Passwords should be hashed (bcrypt/Argon2) not stored in plaintext
- Use session tokens or JWT instead of Basic Auth with every request
- Implement proper database with ACID properties instead of JSON files
- Add file locking or use a database to prevent race conditions
- Use HTTPS in production to protect credentials in transit
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
import json

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Load activities from JSON file
activities_file = os.path.join(Path(__file__).parent, "activities.json")
with open(activities_file, "r") as f:
    activities = json.load(f)

# Load teachers credentials from JSON file
teachers_file = os.path.join(Path(__file__).parent, "teachers.json")
with open(teachers_file, "r") as f:
    teachers_data = json.load(f)
    teachers = {teacher["username"]: teacher["password"] for teacher in teachers_data["teachers"]}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/auth/login")
def login(username: str, password: str):
    """Authenticate a teacher"""
    if username in teachers and teachers[username] == password:
        return {"success": True, "message": "Login successful", "username": username}
    raise HTTPException(status_code=401, detail="Invalid credentials")


def verify_teacher_auth(authorization: str = Header(None)):
    """Verify teacher authentication from Authorization header
    
    NOTE: This is a simple demonstration. In production:
    - Use hashed passwords, not plaintext comparison
    - Use session tokens/JWT instead of sending credentials with each request
    - Implement rate limiting to prevent brute force attacks
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        # Expected format: "Bearer username:password"
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization format")
        
        credentials = authorization[7:]  # Remove "Bearer "
        username, password = credentials.split(":", 1)
        
        if username not in teachers or teachers[username] != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return username
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization format")


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, authorization: str = Header(None)):
    """Sign up a student for an activity (teachers only)"""
    # Verify teacher authentication
    verify_teacher_auth(authorization)
    
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    
    # Save activities back to JSON file
    # NOTE: In production, use a database or implement file locking to prevent race conditions
    with open(activities_file, "w") as f:
        json.dump(activities, f, indent=2)
    
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, authorization: str = Header(None)):
    """Unregister a student from an activity (teachers only)"""
    # Verify teacher authentication
    verify_teacher_auth(authorization)
    
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    
    # Save activities back to JSON file
    # NOTE: In production, use a database or implement file locking to prevent race conditions
    with open(activities_file, "w") as f:
        json.dump(activities, f, indent=2)
    
    return {"message": f"Unregistered {email} from {activity_name}"}
