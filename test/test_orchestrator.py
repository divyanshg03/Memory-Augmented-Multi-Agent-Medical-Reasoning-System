from pipeline.orchestrator import run_full_clinical_orchestrator
from utils.output_formatter import format_clinical_output

def main():
    patient_data = {
        "name": "Anonymous",
        "age": 21,
        "gender": "male",
        "known_conditions": ["anxiety"],
        "medications": [],
        "past_similar_episodes": True,
    }

    episode_data = {
        "symptoms": [
            "sudden fear",
            "heart racing",
            "shortness of breath",
            "dizziness",
        ],
        "duration_minutes": 10,
        "severity": 7,
        "triggers": ["stress"],
    }

    result = run_full_clinical_orchestrator(
        patient_data=patient_data,
        episode_data=episode_data,
    )

    # ✅ PRINT EXACTLY ONCE
    print(format_clinical_output(result))


if __name__ == "__main__":
    main()
