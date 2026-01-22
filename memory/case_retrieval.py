from typing import List, Dict


class CaseRetriever:
    def __init__(self, episode_memory):
        """
        episode_memory: LongTermMemory instance
        """
        self.memory = episode_memory

    def retrieve_case_context(
        self,
        patient_id: str,
        episode_summary: str,
        limit_patient: int = 3,
        limit_population: int = 3,
    ) -> Dict:
        """
        Retrieve memory relevant to the current case.
        """

        # --- 1. Patient-specific memory ---
        patient_history = self.memory.retrieve_relevant_episodes(
            query_text=episode_summary,
            limit=limit_patient,
            min_confidence=0.0,          # do not filter yet
            domain="healthcare",
            days_back=365,
            allow_disagreement=True,
        )

        # Keep only same-patient episodes
        patient_history = [
            ep for ep in patient_history
            if ep.get("patient_id") == patient_id
        ]

        # --- 2. Population-level memory ---
        population_cases = self.memory.retrieve_relevant_episodes(
            query_text=episode_summary,
            limit=limit_population,
            min_confidence=0.7,           # higher bar
            domain="healthcare",
            days_back=730,
            allow_disagreement=False,
        )

        # Remove same-patient episodes
        population_cases = [
            ep for ep in population_cases
            if ep.get("patient_id") != patient_id
        ]

        return {
            "patient_history": patient_history,
            "population_cases": population_cases,
        }
