document.addEventListener("DOMContentLoaded", () => {
  // Handle template usage buttons
  const useTemplateButtons = document.querySelectorAll(".use-template-btn");

  useTemplateButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      const card = event.target.closest(".template-card");
      const templateName = card.querySelector("h3").textContent;

      // Show confirmation message
      showNotification(`Using template: ${templateName}`, "success");

      // Simulate template deployment
      button.textContent = "Deploying...";
      button.disabled = true;

      setTimeout(() => {
        button.textContent = "✓ Template Ready";
        button.style.background =
          "linear-gradient(135deg, #4CAF50 0%, #45a049 100%)";

        setTimeout(() => {
          button.textContent = "Use Template";
          button.disabled = false;
          button.style.background = "";
        }, 2000);
      }, 1500);
    });
  });

  // Smooth scroll for navigation links
  document.querySelectorAll('.nav-item[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const targetId = link.getAttribute("href").substring(1);
      const targetElement = document.getElementById(targetId);

      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });

        // Update active state
        document
          .querySelectorAll(".nav-item")
          .forEach((item) => item.classList.remove("active"));
        link.classList.add("active");
      }
    });
  });

  // Add hover effects to model cards
  const modelCards = document.querySelectorAll(".model-card");
  modelCards.forEach((card) => {
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-3px) scale(1.02)";
    });

    card.addEventListener("mouseleave", () => {
      card.style.transform = "";
    });
  });

  // Notification system
  function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 15px 25px;
      background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
      color: #1a237e;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      font-weight: 600;
      z-index: 1000;
      animation: slideIn 0.3s ease;
      border: 2px solid white;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = "slideOut 0.3s ease";
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 3000);
  }

  // Add CSS animations
  const style = document.createElement("style");
  style.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    @keyframes slideOut {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);

  // Initialize with welcome message
  setTimeout(() => {
    showNotification("Welcome to ApSciOs Build Template Gallery!", "info");
  }, 500);
});
