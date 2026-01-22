from memory.case_retrieval import CaseRetriever
from memory.case_context import build_case_context
from memory.qdrant_memory import LongTermMemory

# Existing episode memory
episode_memory = LongTermMemory()
episode_memory.initialize()

# Example episode
patient_id = "d65ad7c6-7453-442c-860d-591a1fc10468"
episode_summary = (
    "Symptoms: sudden fear, heart racing, shortness of breath, dizziness. "
    "Duration: 10 minutes. Severity: 7/10."
)

retriever = CaseRetriever(episode_memory)
case_memory = retriever.retrieve_case_context(
    patient_id=patient_id,
    episode_summary=episode_summary,
)

print("Patient history:", case_memory["patient_history"])
print("Population cases:", case_memory["population_cases"])

context = build_case_context(
    episode_summary,
    case_memory["patient_history"],
    case_memory["population_cases"],
)

print("\nCASE CONTEXT:\n")
print(context)
