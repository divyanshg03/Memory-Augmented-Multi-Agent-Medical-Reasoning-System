from memory.qdrant_memory import LongTermMemory
from memory.episode_input import EpisodeInput
from pipeline.clinical_pipeline import run_clinical_pipeline
from utils.output_formatter import format_clinical_output   # ✅ ADD THIS

# Setup memory
episode_memory = LongTermMemory()
episode_memory.initialize()

# Example episode input
episode_input = EpisodeInput(
    patient_id="d65ad7c6-7453-442c-860d-591a1fc10468",
    symptoms=[
        "sudden fear",
        "heart racing",
        "shortness of breath",
        "dizziness",
    ],
    duration_minutes=10,
    severity=7,
    triggers=["stress"],
)

# Run everything
result = run_clinical_pipeline(
    episode_input=episode_input,
    episode_memory=episode_memory,
)

# ✅ FORMATTED OUTPUT (THIS IS THE RIGHT PLACE)
print(format_clinical_output(result))
