from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional

from pipeline.orchestrator import run_full_clinical_orchestrator
from utils.output_formatter import format_clinical_output

app = FastAPI(
    title="Memory-Augmented Clinical Reasoning System",
    version="1.0.0",
)

# ---------------- INPUT SCHEMAS ----------------

class PatientInput(BaseModel):
    name: Optional[str] = "Anonymous"
    age: int
    gender: str
    known_conditions: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    past_similar_episodes: bool = False


class EpisodeInput(BaseModel):
    symptoms: List[str]
    duration_minutes: int
    severity: int
    triggers: List[str] = Field(default_factory=list)


class ClinicalRequest(BaseModel):
    patient: PatientInput
    episode: EpisodeInput


# ---------------- API ----------------

@app.post("/submit-episode")
def submit_episode(request: ClinicalRequest):
    result = run_full_clinical_orchestrator(
        patient_data=request.patient.model_dump(),
        episode_data=request.episode.model_dump(),
    )
    return {
        "formatted_report": format_clinical_output(result),
        "confidence": result["confidence"],
        "disagreement": result["disagreement"],
    }


# ---------------- SLIM UI ----------------

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    return """
<!DOCTYPE html>
<html>
<head>
  <title>Clinical Decision Support</title>
  <style>
    body {
      font-family: Inter, Arial, sans-serif;
      background: #f6f8fa;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 900px;
      margin: 40px auto;
      padding: 20px;
    }
    h1 {
      text-align: center;
      margin-bottom: 30px;
    }
    .card {
      background: white;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    label {
      font-weight: 600;
      display: block;
      margin-top: 10px;
    }
    input, textarea {
      width: 100%;
      padding: 8px;
      margin-top: 4px;
      border-radius: 4px;
      border: 1px solid #ccc;
    }
    textarea { resize: vertical; }
    button {
      background: #2563eb;
      color: white;
      border: none;
      padding: 12px 18px;
      border-radius: 6px;
      font-size: 15px;
      cursor: pointer;
      margin-top: 15px;
    }
    button:hover { background: #1e4fd8; }
    .output {
      white-space: pre-wrap;
      background: #f9fafb;
      border-left: 4px solid #2563eb;
      padding: 15px;
      font-size: 14px;
    }
    .meta {
      font-size: 14px;
      margin-bottom: 10px;
    }
  </style>
</head>

<body>
<div class="container">

  <h1>🧠 Memory-Augmented Clinical Decision Support</h1>

  <div class="card">
    <h3>Patient Information</h3>

    <label>Name</label>
    <input id="name" placeholder="Anonymous">

    <label>Age</label>
    <input id="age" type="number">

    <label>Gender</label>
    <input id="gender">
  </div>

  <div class="card">
    <h3>Episode Details</h3>

    <label>Symptoms (comma-separated)</label>
    <textarea id="symptoms"></textarea>

    <label>Duration (minutes)</label>
    <input id="duration" type="number">

    <label>Severity (1–10)</label>
    <input id="severity" type="number">
  </div>

  <div class="card">
    <button onclick="submitEpisode()">Run Clinical Reasoning</button>
  </div>

  <div class="card">
    <h3>System Output</h3>
    <div class="meta" id="meta"></div>
    <div class="output" id="output">Awaiting input…</div>
  </div>

</div>

<script>
async function submitEpisode() {
  document.getElementById("output").textContent = "Processing…";

  const payload = {
    patient: {
      name: document.getElementById("name").value || "Anonymous",
      age: Number(document.getElementById("age").value),
      gender: document.getElementById("gender").value,
      known_conditions: [],
      medications: [],
      past_similar_episodes: false
    },
    episode: {
      symptoms: document.getElementById("symptoms").value.split(","),
      duration_minutes: Number(document.getElementById("duration").value),
      severity: Number(document.getElementById("severity").value),
      triggers: []
    }
  };

  const res = await fetch("/submit-episode", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await res.json();

  document.getElementById("meta").textContent =
    "Confidence: " + Math.round(data.confidence * 100) + "% | Disagreement: " + (data.disagreement ? "Yes" : "No");

  document.getElementById("output").textContent = data.formatted_report;
}
</script>

</body>
</html>
"""
