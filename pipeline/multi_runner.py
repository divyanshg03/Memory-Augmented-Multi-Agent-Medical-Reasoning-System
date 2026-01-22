from pipeline.orchestrator import run_full_clinical_orchestrator
from utils.output_formatter import format_clinical_output


def run_multiple_patients(patients: list[dict]) -> list[dict]:
    """
    Runs the full system (Steps 1–5) for multiple patients.

    patients = [
        {
            "patient_data": {...},
            "episode_data": {...}
        },
        ...
    ]
    """

    results = []

    for idx, case in enumerate(patients, start=1):
        print(f"\n🧍 Processing patient {idx}...\n")

        result = run_full_clinical_orchestrator(
            patient_data=case["patient_data"],
            episode_data=case["episode_data"],
        )

        print(format_clinical_output(result))

        results.append(result)

    return results
