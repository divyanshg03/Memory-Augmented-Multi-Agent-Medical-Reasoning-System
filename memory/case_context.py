def build_case_context(
    episode_summary: str,
    patient_history: list,
    population_cases: list,
) -> str:
    context = f"CURRENT EPISODE:\n{episode_summary}\n\n"

    if patient_history:
        context += "PATIENT HISTORY:\n"
        for i, ep in enumerate(patient_history, 1):
            context += (
                f"{i}. Decision: {ep['decision']} "
                f"(Confidence: {ep['confidence']})\n"
            )
    else:
        context += "PATIENT HISTORY:\nNone\n"

    context += "\n"

    if population_cases:
        context += "SIMILAR PAST CASES:\n"
        for i, ep in enumerate(population_cases, 1):
            context += (
                f"{i}. Decision: {ep['decision']} "
                f"(Confidence: {ep['confidence']})\n"
            )
    else:
        context += "SIMILAR PAST CASES:\nNone\n"

    return context
