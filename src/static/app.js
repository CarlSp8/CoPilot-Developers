document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const userIcon = document.getElementById("user-icon");
  const loginModal = document.getElementById("login-modal");
  const signupModal = document.getElementById("signup-modal");
  const closeLogin = document.getElementById("close-login");
  const closeSignup = document.getElementById("close-signup");
  const loginForm = document.getElementById("login-form");
  const signupForm = document.getElementById("signup-form");
  const loginMessage = document.getElementById("login-message");
  const signupMessage = document.getElementById("signup-message");
  const searchInput = document.getElementById("search-input");
  const categoryFilter = document.getElementById("category-filter");
  const sortSelect = document.getElementById("sort-select");

  let allActivities = {};
  let authToken = null;
  let currentActivityForSignup = null;

  // Authentication state
  function isLoggedIn() {
    return authToken !== null;
  }

  // Update UI based on login state
  function updateLoginUI() {
    if (isLoggedIn()) {
      userIcon.classList.add("logged-in");
      userIcon.title = "Logged in as teacher";
    } else {
      userIcon.classList.remove("logged-in");
      userIcon.title = "Click to login";
    }
  }

  // Modal controls
  userIcon.addEventListener("click", () => {
    if (!isLoggedIn()) {
      loginModal.style.display = "block";
    } else {
      if (confirm("Do you want to logout?")) {
        authToken = null;
        updateLoginUI();
        displayActivities();
        showMessage(loginMessage, "Logged out successfully", "success");
      }
    }
  });

  closeLogin.addEventListener("click", () => {
    loginModal.style.display = "none";
  });

  closeSignup.addEventListener("click", () => {
    signupModal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target === loginModal) {
      loginModal.style.display = "none";
    }
    if (event.target === signupModal) {
      signupModal.style.display = "none";
    }
  });

  // Login form submission
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch(
        `/auth/login?username=${encodeURIComponent(
          username
        )}&password=${encodeURIComponent(password)}`,
        { method: "POST" }
      );

      const result = await response.json();

      if (response.ok) {
        authToken = `${username}:${password}`;
        loginModal.style.display = "none";
        loginForm.reset();
        updateLoginUI();
        displayActivities();
        showMessage(loginMessage, "Login successful!", "success");
      } else {
        showMessage(loginMessage, result.detail || "Login failed", "error");
      }
    } catch (error) {
      showMessage(loginMessage, "Login failed. Please try again.", "error");
      console.error("Error logging in:", error);
    }
  });

  // Function to show messages
  function showMessage(element, text, type) {
    element.textContent = text;
    element.className = `message ${type}`;
    element.classList.remove("hidden");
    setTimeout(() => {
      element.classList.add("hidden");
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

  // Function to filter and sort activities
  function getFilteredAndSortedActivities() {
    const searchTerm = searchInput.value.toLowerCase();
    const category = categoryFilter.value;
    const sortBy = sortSelect.value;

    let filtered = Object.entries(allActivities).filter(([name, details]) => {
      // Search filter
      const matchesSearch =
        name.toLowerCase().includes(searchTerm) ||
        details.description.toLowerCase().includes(searchTerm);

      // Category filter
      const matchesCategory =
        category === "all" || details.category === category;

      return matchesSearch && matchesCategory;
    });

    // Sort
    filtered.sort((a, b) => {
      if (sortBy === "name") {
        return a[0].localeCompare(b[0]);
      } else if (sortBy === "time") {
        return a[1].time_sort.localeCompare(b[1].time_sort);
      }
      return 0;
    });

    return filtered;
  }

  // Function to display activities
  function displayActivities() {
    const filtered = getFilteredAndSortedActivities();
    activitiesList.innerHTML = "";

    if (filtered.length === 0) {
      activitiesList.innerHTML = "<p>No activities found matching your criteria.</p>";
      return;
    }

    filtered.forEach(([name, details]) => {
      const activityCard = document.createElement("div");
      activityCard.className = "activity-card";

      const spotsLeft = details.max_participants - details.participants.length;

      // Create participants HTML with delete icons
      const participantsHTML =
        details.participants.length > 0
          ? `<div class="participants-section">
            <h5>Participants (${details.participants.length}):</h5>
            <ul class="participants-list">
              ${details.participants
                .map(
                  (email) =>
                    `<li>
                      <span class="participant-email">${email}</span>
                      <button class="delete-btn" data-activity="${name}" data-email="${email}" ${
                      !isLoggedIn() ? "disabled" : ""
                    }>❌</button>
                    </li>`
                )
                .join("")}
            </ul>
          </div>`
          : `<p><em>No participants yet</em></p>`;

      activityCard.innerHTML = `
        <span class="category-badge">${details.category}</span>
        <h4>${name}</h4>
        <p>${details.description}</p>
        <p><strong>Schedule:</strong> ${details.schedule}</p>
        <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        <button class="register-btn" data-activity="${name}" ${
        !isLoggedIn() ? "disabled" : ""
      }>
          ${isLoggedIn() ? "Register Student" : "Login to Register"}
        </button>
        <div class="participants-container">
          ${participantsHTML}
        </div>
      `;

      activitiesList.appendChild(activityCard);
    });

    // Add event listeners to delete buttons
    document.querySelectorAll(".delete-btn").forEach((button) => {
      if (isLoggedIn()) {
        button.addEventListener("click", handleUnregister);
      }
    });

    // Add event listeners to register buttons
    document.querySelectorAll(".register-btn").forEach((button) => {
      if (isLoggedIn()) {
        button.addEventListener("click", handleRegisterClick);
      }
    });
  }

  // Handle register button click
  function handleRegisterClick(event) {
    const button = event.target;
    currentActivityForSignup = button.getAttribute("data-activity");
    signupModal.style.display = "block";
  }

  // Handle signup form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = currentActivityForSignup;

    if (!activity) {
      showMessage(signupMessage, "No activity selected", "error");
      return;
    }

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(
          activity
        )}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(signupMessage, result.message, "success");
        signupForm.reset();
        signupModal.style.display = "none";
        fetchActivities(); // Refresh activities list
      } else {
        showMessage(signupMessage, result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage(signupMessage, "Failed to sign up. Please try again.", "error");
      console.error("Error signing up:", error);
    }
  });

  // Handle unregister functionality
  async function handleUnregister(event) {
    const button = event.target;
    const activity = button.getAttribute("data-activity");
    const email = button.getAttribute("data-email");

    if (!confirm(`Are you sure you want to unregister ${email} from ${activity}?`)) {
      return;
    }

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(
          activity
        )}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      const result = await response.json();

      if (response.ok) {
        fetchActivities(); // Refresh activities list
      } else {
        alert(result.detail || "An error occurred");
      }
    } catch (error) {
      alert("Failed to unregister. Please try again.");
      console.error("Error unregistering:", error);
    }
  }

  // Event listeners for filters and search
  searchInput.addEventListener("input", displayActivities);
  categoryFilter.addEventListener("change", displayActivities);
  sortSelect.addEventListener("change", displayActivities);

  // Initialize app
  updateLoginUI();
  fetchActivities();
});
