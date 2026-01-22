from memory.patient_memory import PatientMemory
from memory.patient_schema import PatientProfile
from memory.qdrant_memory import LongTermMemory
from memory.episode_input import EpisodeInput
from memory.episode_ingestion import EpisodeIngestor

# --- Setup ---
patient_memory = PatientMemory()
patient_memory.initialize()

episode_memory = LongTermMemory()
episode_memory.initialize()

# --- Create patient ---
patient = PatientProfile(
    age=21,
    gender="male",
    known_conditions=["anxiety"],
    past_similar_episodes=True,
)

patient_memory.store_patient(patient)

# --- Ingest episode ---
episode_input = EpisodeInput(
    patient_id=patient.patient_id,
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

ingestor = EpisodeIngestor(episode_memory)
episode = ingestor.ingest(episode_input)

print("✅ Episode ingested")
print("Patient ID:", episode.patient_id)
print("Summary:", episode.state_summary)
