from memory.patient_memory import PatientMemory
from memory.patient_schema import PatientProfile

# Initialize patient memory
patient_memory = PatientMemory()
patient_memory.initialize()

# Simulated intake
patient = PatientProfile(
    name="Anonymous",
    age=21,
    gender="male",
    known_conditions=["anxiety"],
    medications=[],
    past_similar_episodes=True,
)

patient_memory.store_patient(patient)

print("✅ Patient stored")
print("Patient ID:", patient.patient_id)

# Retrieve patient
retrieved = patient_memory.get_patient(patient.patient_id)
print("\nRetrieved patient profile:")
print(retrieved)
