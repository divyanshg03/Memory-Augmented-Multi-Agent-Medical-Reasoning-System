from pipeline.orchestrator import run_full_clinical_orchestrator
from utils.output_formatter import format_clinical_output


def intake_patient():
    print("\n--- Patient Intake ---")
    return {
        "name": input("Name (optional): ") or "Anonymous",
        "age": int(input("Age: ")),
        "gender": input("Gender: "),
        "known_conditions": input("Known conditions (comma-separated): ").split(",")
        if input("Any known conditions? (y/n): ").lower() == "y"
        else [],
        "medications": input("Medications (comma-separated): ").split(",")
        if input("On medications? (y/n): ").lower() == "y"
        else [],
        "past_similar_episodes": input("Had similar episodes before? (y/n): ").lower()
        == "y",
    }


def intake_episode(patient_id: str):
    print("\n--- Episode Intake ---")
    return {
        "symptoms": input("Symptoms (comma-separated): ").split(","),
        "duration_minutes": int(input("Duration (minutes): ")),
        "severity": int(input("Severity (1–10): ")),
        "triggers": input("Triggers (comma-separated): ").split(",")
        if input("Any triggers? (y/n): ").lower() == "y"
        else [],
    }


def main():
    print("🧠 Memory-Augmented Clinical Reasoning System")

    while True:
        print("\nEnter a new patient episode\n")

        patient_data = intake_patient()
        episode_data = intake_episode(patient_id=None)

        result = run_full_clinical_orchestrator(
            patient_data=patient_data,
            episode_data=episode_data,
        )

        print(format_clinical_output(result))

        if input("\nAdd another episode? (y/n): ").lower() != "y":
            break


if __name__ == "__main__":
    main()
