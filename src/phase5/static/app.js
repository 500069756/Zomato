const form = document.getElementById("recommendation-form");
const statusMessage = document.getElementById("status-message");
const summaryContainer = document.getElementById("recommendation-summary");
const cardsContainer = document.getElementById("recommendation-cards");

function setStatus(text, isError = false) {
  statusMessage.textContent = text;
  statusMessage.style.color = isError ? "#dc2626" : "#16a34a";
}

function clearResults() {
  summaryContainer.textContent = "";
  cardsContainer.innerHTML = "";
}

function renderRecommendation(card) {
  const element = document.createElement("div");
  element.className = "recommendation-card";
  
  // Handle missing or zero ratings
  const ratingDisplay = card.rating && card.rating > 0 ? `${card.rating} \u2605` : "Not available";
  
  element.innerHTML = `
    <h2>${card.restaurant_name}</h2>
    <p><strong>Cuisine:</strong> ${card.cuisine || "Not specified"}</p>
    <p><strong>Location:</strong> ${card.location || "Not specified"}</p>
    <p><strong>Rating:</strong> ${ratingDisplay}</p>
    <p><strong>Budget:</strong> ${card.budget_label ? card.budget_label.charAt(0).toUpperCase() + card.budget_label.slice(1) : "Not specified"}</p>
    <p><strong>Explanation:</strong> ${card.explanation || "Matches your preferences based on location, cuisine, and other criteria."}</p>
    ${card.address ? `<p><strong>Address:</strong> ${card.address}</p>` : ""}
  `;
  cardsContainer.appendChild(element);
}

async function loadLocalities() {
  try {
    const response = await fetch("/api/localities");
    if (!response.ok) {
      throw new Error("Failed to load localities");
    }
    const data = await response.json();
    const locationSelect = document.getElementById("location");

    // Clear existing options except the first one
    locationSelect.innerHTML = '<option value="">Select a location</option>';

    // Add localities as options
    data.localities.forEach(locality => {
      const option = document.createElement("option");
      option.value = locality;
      option.textContent = locality;
      locationSelect.appendChild(option);
    });
  } catch (error) {
    console.error("Error loading localities:", error);
    setStatus("Failed to load locations. Please refresh the page.", true);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus("Loading recommendations...");
  clearResults();

  const payload = {
    location: document.getElementById("location").value.trim(),
    budget: document.getElementById("budget").value,
    cuisine: document.getElementById("cuisine").value.trim(),
    minimum_rating: document.getElementById("minimum_rating").value,
    additional_preferences: document.getElementById("additional_preferences").value.trim(),
    top_n: document.getElementById("top_n").value,
  };

  console.log("Sending payload:", payload);

  try {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    console.log("Response status:", response.status);
    const result = await response.json();
    console.log("Response data:", result);
    
    if (!response.ok) {
      setStatus(result.error || result.fallback_message || "Unable to fetch recommendations.", true);
      return;
    }
    
    if (!result.success) {
      setStatus(result.fallback_message || "No matching restaurants found.", true);
      return;
    }

    setStatus(result.warning ? `Warning: ${result.warning}` : "Recommendations loaded successfully!");
    summaryContainer.textContent = result.summary;

    result.recommendations.forEach((item) => renderRecommendation(item));
  } catch (err) {
    setStatus("Unable to reach the recommendation service. Please try again.", true);
    console.error("Fetch error:", err);
  }
});

// Load localities when the page loads
document.addEventListener("DOMContentLoaded", loadLocalities);
