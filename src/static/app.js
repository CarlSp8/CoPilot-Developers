document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const loginBtn = document.getElementById("login-btn");
  const logoutBtn = document.getElementById("logout-btn");
  const userInfo = document.getElementById("user-info");
  const loginModal = document.getElementById("login-modal");
  const signupModal = document.getElementById("signup-modal");
  const loginForm = document.getElementById("login-form");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const searchBox = document.getElementById("search-box");
  const categoryFilter = document.getElementById("category-filter");
  const sortSelect = document.getElementById("sort-select");

  let allActivities = {};
  let isLoggedIn = false;
  let currentActivityForSignup = null;

  // Modal close buttons
  document.querySelectorAll(".close").forEach((closeBtn) => {
    closeBtn.addEventListener("click", () => {
      loginModal.classList.remove("show");
      loginModal.classList.add("hidden");
      signupModal.classList.remove("show");
      signupModal.classList.add("hidden");
    });
  });

  // Close modals when clicking outside
  window.addEventListener("click", (event) => {
    if (event.target === loginModal) {
      loginModal.classList.remove("show");
      loginModal.classList.add("hidden");
    }
    if (event.target === signupModal) {
      signupModal.classList.remove("show");
      signupModal.classList.add("hidden");
    }
  });

  // Login button click
  loginBtn.addEventListener("click", () => {
    loginModal.classList.remove("hidden");
    loginModal.classList.add("show");
  });

  // Logout button click
  logoutBtn.addEventListener("click", () => {
    isLoggedIn = false;
    loginBtn.classList.remove("hidden");
    logoutBtn.classList.add("hidden");
    userInfo.classList.add("hidden");
    showMessage("Logged out successfully", "success");
    fetchActivities();
  });

  // Login form submission
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      const result = await response.json();

      if (response.ok) {
        isLoggedIn = true;
        loginBtn.classList.add("hidden");
        logoutBtn.classList.remove("hidden");
        userInfo.textContent = `Welcome, ${result.name}`;
        userInfo.classList.remove("hidden");
        
        loginModal.classList.remove("show");
        loginModal.classList.add("hidden");
        loginForm.reset();
        
        showMessage("Login successful!", "success");
        fetchActivities();
      } else {
        document.getElementById("login-message").textContent = result.detail;
        document.getElementById("login-message").className = "error";
        document.getElementById("login-message").classList.remove("hidden");
      }
    } catch (error) {
      document.getElementById("login-message").textContent = "Login failed. Please try again.";
      document.getElementById("login-message").className = "error";
      document.getElementById("login-message").classList.remove("hidden");
      console.error("Error logging in:", error);
    }
  });

  // Signup form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("student-email").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(currentActivityForSignup)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        signupModal.classList.remove("show");
        signupModal.classList.add("hidden");
        signupForm.reset();
        showMessage(result.message, "success");
        fetchActivities();
      } else {
        document.getElementById("signup-message").textContent = result.detail;
        document.getElementById("signup-message").className = "error";
        document.getElementById("signup-message").classList.remove("hidden");
      }
    } catch (error) {
      document.getElementById("signup-message").textContent = "Failed to sign up. Please try again.";
      document.getElementById("signup-message").className = "error";
      document.getElementById("signup-message").classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Function to show message
  function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = type;
    messageDiv.classList.remove("hidden");

    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, 5000);
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      allActivities = await response.json();

      displayActivities();
    } catch (error) {
      activitiesList.innerHTML =
        "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Function to display activities with filtering and sorting
  function displayActivities() {
    const searchTerm = searchBox.value.toLowerCase();
    const categoryValue = categoryFilter.value;
    const sortValue = sortSelect.value;

    // Filter activities
    let filtered = Object.entries(allActivities).filter(([name, details]) => {
      const matchesSearch = name.toLowerCase().includes(searchTerm) || 
                           details.description.toLowerCase().includes(searchTerm);
      const matchesCategory = !categoryValue || details.category === categoryValue;
      return matchesSearch && matchesCategory;
    });

    // Sort activities
    filtered.sort(([nameA, detailsA], [nameB, detailsB]) => {
      if (sortValue === "name") {
        return nameA.localeCompare(nameB);
      } else if (sortValue === "schedule") {
        return detailsA.schedule.localeCompare(detailsB.schedule);
      } else if (sortValue === "availability") {
        const availA = detailsA.max_participants - detailsA.participants.length;
        const availB = detailsB.max_participants - detailsB.participants.length;
        return availB - availA;
      }
      return 0;
    });

    // Clear and populate activities list
    activitiesList.innerHTML = "";

    if (filtered.length === 0) {
      activitiesList.innerHTML = "<p>No activities found matching your criteria.</p>";
      return;
    }

    filtered.forEach(([name, details]) => {
      const activityCard = document.createElement("div");
      activityCard.className = "activity-card";

      const spotsLeft = details.max_participants - details.participants.length;

      // Create participants HTML
      const participantsHTML =
        details.participants.length > 0
          ? `<div class="participants-section">
            <h5>Participants (${details.participants.length}/${details.max_participants}):</h5>
            <ul class="participants-list">
              ${details.participants
                .map(
                  (email) =>
                    `<li>
                      <span class="participant-email">${email}</span>
                      ${isLoggedIn ? `<button class="delete-btn" data-activity="${name}" data-email="${email}">❌</button>` : ''}
                    </li>`
                )
                .join("")}
            </ul>
          </div>`
          : `<p><em>No participants yet</em></p>`;

      activityCard.innerHTML = `
        <span class="category-badge">${details.category || 'General'}</span>
        <h4>${name}</h4>
        <p>${details.description}</p>
        <p><strong>Schedule:</strong> ${details.schedule}</p>
        <p><strong>Availability:</strong> ${spotsLeft} spots left (${details.participants.length}/${details.max_participants})</p>
        <div class="participants-container">
          ${participantsHTML}
        </div>
        <div class="activity-actions">
          <button class="register-btn" data-activity="${name}" ${spotsLeft === 0 || !isLoggedIn ? 'disabled' : ''}>
            ${isLoggedIn ? (spotsLeft === 0 ? 'Full' : 'Register Student') : 'Login to Register'}
          </button>
        </div>
      `;

      activitiesList.appendChild(activityCard);
    });

    // Add event listeners to register buttons
    document.querySelectorAll(".register-btn").forEach((button) => {
      button.addEventListener("click", (e) => {
        const activityName = e.target.getAttribute("data-activity");
        currentActivityForSignup = activityName;
        document.getElementById("activity-name").textContent = activityName;
        signupModal.classList.remove("hidden");
        signupModal.classList.add("show");
      });
    });

    // Add event listeners to delete buttons
    document.querySelectorAll(".delete-btn").forEach((button) => {
      button.addEventListener("click", handleUnregister);
    });
  }

  // Handle unregister functionality
  async function handleUnregister(event) {
    const button = event.target;
    const activity = button.getAttribute("data-activity");
    const email = button.getAttribute("data-email");

    if (!isLoggedIn) {
      showMessage("You must be logged in to unregister students", "error");
      return;
    }

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        fetchActivities();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to unregister. Please try again.", "error");
      console.error("Error unregistering:", error);
    }
  }

  // Add event listeners for search, filter, and sort
  searchBox.addEventListener("input", displayActivities);
  categoryFilter.addEventListener("change", displayActivities);
  sortSelect.addEventListener("change", displayActivities);

  // Initialize app
  fetchActivities();
});
