// Point this to your deployed backend URL once live on Render,
// e.g. "https://footballiq-ai.onrender.com"
const API_BASE = window.location.origin;

let currentPlayerId = null;

document.getElementById("create-player-btn").addEventListener("click", async () => {
  const name = document.getElementById("player-name").value.trim();
  const age = document.getElementById("player-age").value;
  const city = document.getElementById("player-city").value.trim();
  const status = document.getElementById("player-status");

  if (!name || !age) {
    status.textContent = "Please enter your name and age.";
    return;
  }

  const form = new FormData();
  form.append("name", name);
  form.append("age", age);
  form.append("city", city);

  status.textContent = "Saving...";
  try {
    const res = await fetch(`${API_BASE}/players`, { method: "POST", body: form });
    const data = await res.json();
    currentPlayerId = data.id;
    status.textContent = `Player saved (ID: ${data.id}). Now upload a drill video below.`;
  } catch (err) {
    status.textContent = "Error saving player. Is the backend running?";
    console.error(err);
  }
});

document.getElementById("upload-btn").addEventListener("click", async () => {
  const status = document.getElementById("upload-status");
  const drillType = document.getElementById("drill-type").value;
  const fileInput = document.getElementById("video-input");

  if (!currentPlayerId) {
    status.textContent = "Save your player details first (step 1).";
    return;
  }
  if (!fileInput.files.length) {
    status.textContent = "Choose a video file first.";
    return;
  }

  const form = new FormData();
  form.append("player_id", currentPlayerId);
  form.append("drill_type", drillType);
  form.append("video", fileInput.files[0]);

  status.textContent = "Analyzing video... this may take a moment.";
  try {
    const res = await fetch(`${API_BASE}/sessions`, { method: "POST", body: form });
    const data = await res.json();
    status.textContent = "Done!";
    renderScores(data.scores, data.feedback);
    await loadPlan();
  } catch (err) {
    status.textContent = "Error analyzing video.";
    console.error(err);
  }
});

function renderScores(scores, feedback) {
  const resultsCard = document.getElementById("results-card");
  resultsCard.classList.remove("hidden");

  const scoresDiv = document.getElementById("scores");
  scoresDiv.innerHTML = "";
  for (const [category, score] of Object.entries(scores)) {
    const row = document.createElement("div");
    row.className = "score-row";
    row.innerHTML = `
      <span>${capitalize(category)}</span>
      <div class="score-bar-bg"><div class="score-bar-fill" style="width:${score}%"></div></div>
      <span>${score}</span>
    `;
    scoresDiv.appendChild(row);
  }

  const feedbackList = document.getElementById("feedback");
  feedbackList.innerHTML = "";
  feedback.forEach((f) => {
    const li = document.createElement("li");
    li.textContent = f;
    feedbackList.appendChild(li);
  });
}

async function loadPlan() {
  const planCard = document.getElementById("plan-card");
  const planDiv = document.getElementById("plan");
  try {
    const res = await fetch(`${API_BASE}/players/${currentPlayerId}/plan`);
    const data = await res.json();
    planCard.classList.remove("hidden");
    planDiv.innerHTML = `
      <p>${data.message}</p>
      <ul>${(data.weekly_drills || []).map((d) => `<li>${d}</li>`).join("")}</ul>
    `;
  } catch (err) {
    console.error(err);
  }
}

function capitalize(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
