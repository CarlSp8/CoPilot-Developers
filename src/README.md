# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- **NEW:** ApSciOs Build Template Gallery with design system and blueprints

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - Main application: http://localhost:8000/
   - **Template Gallery**: http://localhost:8000/static/template-gallery.html
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister from an activity                                    |

## ApSciOs Build Template Gallery

The application now includes a comprehensive build template gallery featuring:

### Design System
- **White-rimmed chromium sidebar** with metallic gradient effects
- **Gold center accents** representing excellence and achievement
- Responsive, modern UI design

### Templates
1. Basic Activity Template (FastAPI, Python, Open Source)
2. Enhanced UI Template (CSS3, JavaScript, Responsive)
3. Admin Dashboard Template (Admin Panel, CRUD, Analytics)
4. Authentication Template (OAuth, JWT, Security)
5. Analytics Template (Charts, Reports, Insights)
6. Multi-language Template (i18n, Localization, Global)

### Build Blueprints
- **Development Blueprint**: Local setup, hot reload, debug tools
- **Production Blueprint**: Optimization, CDN, performance monitoring
- **Testing Blueprint**: Unit tests, integration tests, CI/CD pipeline

### Open Source Models
- FastAPI Framework
- Uvicorn Server
- Python

See the complete documentation in [BUILD_BLUEPRINT.md](../BUILD_BLUEPRINT.md)

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
