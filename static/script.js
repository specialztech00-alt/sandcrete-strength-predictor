/* ------------------------------------------------------------------
   Prediction Tool — frontend logic

   Calls POST /predict on app/main.py, which returns:
     { predicted_strength, unit, standards_recommendation }

   NON_LOAD_BEARING_MIN / LOAD_BEARING_MIN below are only used to label
   the strength category (Low / Moderate / High) shown next to the
   result. Keep them in sync with the same thresholds in app/standards.py.
------------------------------------------------------------------- */

const NON_LOAD_BEARING_MIN = 2.5;  // keep in sync with standards.py
const LOAD_BEARING_MIN = 3.45;     // keep in sync with standards.py
const GAUGE_MAX = 10; // upper bound of the gauge in MPa — adjust only if the dataset's max strength is meaningfully different
const REQUEST_TIMEOUT_MS = 25000;

const form = document.getElementById("predict-form");
const runButton = document.getElementById("run-button");
const formError = document.getElementById("form-error");
const resultSection = document.getElementById("result-section");
const resultNumber = document.getElementById("result-number");
const resultCategory = document.getElementById("result-category");
const resultAdvice = document.getElementById("result-advice-text");

async function fetchWithTimeout(url, options = {}, timeoutMs = REQUEST_TIMEOUT_MS) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

function setLoading(isLoading) {
  runButton.disabled = isLoading;
  runButton.classList.toggle("is-loading", isLoading);
  runButton.querySelector(".button__label").textContent = isLoading
    ? "Predicting…"
    : "Predict Strength";
}

function categoryFor(strength) {
  if (strength >= LOAD_BEARING_MIN) return { label: "High Strength", css: "high" };
  if (strength >= NON_LOAD_BEARING_MIN) return { label: "Moderate Strength", css: "moderate" };
  return { label: "Low Strength", css: "low" };
}

const strengthFill = document.getElementById("strength-fill");

function resetGauge() {
  if (!strengthFill) return;
  strengthFill.style.transition = "none";
  strengthFill.style.width = "0%";
  requestAnimationFrame(() => {
    strengthFill.style.transition = "width 0.72s ease-out";
  });
}

function strengthToFillWidth(strength) {
  const minStrength = 0;
  const maxStrength = 10;
  const clampedStrength = Math.max(minStrength, Math.min(maxStrength, strength));
  return (clampedStrength / maxStrength) * 100;
}

function animateGauge(strength) {
  if (!strengthFill) return;
  const width = strengthToFillWidth(strength);
  strengthFill.style.width = `${width}%`;
}

function renderResult(strength, recommendation) {
  const category = categoryFor(strength);
  resultNumber.textContent = strength.toFixed(2);
  resultCategory.textContent = category.label;
  resultCategory.className = `result__category result__category--${category.css}`;
  resultAdvice.textContent = recommendation;
  resultSection.hidden = false;
  resultSection.classList.remove("result--error");
  console.log("[gauge] renderResult", { strength });
  animateGauge(strength);
}

function renderError(message) {
  resetGauge();
  resultNumber.textContent = "—";
  resultCategory.textContent = "";
  resultCategory.className = "result__category";
  resultAdvice.textContent = message;
  resultSection.hidden = false;
  resultSection.classList.add("result--error");
}

async function parseJsonSafe(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  formError.textContent = "";
  setLoading(true);

  const payload = {
    curing_technique: form.curing_technique.value,
    cement_brand: form.cement_brand.value,
    mix_ratio: form.mix_ratio.value,
    curing_age: parseFloat(form.curing_age.value),
    water_cement_ratio: parseFloat(form.water_cement_ratio.value),
  };

  try {
    resetGauge();
    const response = await fetchWithTimeout("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await parseJsonSafe(response);

    if (!response.ok) {
      const detail = data?.detail || `Server returned ${response.status}.`;
      renderError(detail);
      return;
    }
    if (!data) {
      renderError("The server responded but sent something unreadable. Check the terminal running uvicorn.");
      return;
    }

    renderResult(data.predicted_strength, data.standards_recommendation);
  } catch (err) {
    if (err.name === "AbortError") {
      renderError(`Request timed out after ${REQUEST_TIMEOUT_MS / 1000}s. The server may still be loading the model — try again.`);
    } else {
      renderError(`Couldn't reach the server: ${err.message}. Check that uvicorn is still running.`);
    }
  } finally {
    setLoading(false);
  }
});
