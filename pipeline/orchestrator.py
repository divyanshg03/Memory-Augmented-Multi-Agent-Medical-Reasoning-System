from memory.patient_memory import PatientMemory
from memory.patient_schema import PatientProfile

from memory.qdrant_memory import LongTermMemory
from memory.episode_input import EpisodeInput
from memory.episode_ingestion import EpisodeIngestor
from memory.case_retrieval import CaseRetriever
from memory.case_context import build_case_context
from memory.memory_updater import MemoryUpdater
from memory.outcome_schema import EpisodeOutcome

from agents.agent_loop import AgentLoop
from agents.consensus import synthesize_decision


def run_full_clinical_orchestrator(
    patient_data: dict,
    episode_data: dict,
):
    """
    Runs the COMPLETE system:
    Step 1 → Step 5 in correct chronological order
    """

    # ================= STEP 1 =================
    # Patient identity & memory
    patient_memory = PatientMemory()
    patient_memory.initialize()

    patient = PatientProfile(**patient_data)
    patient_memory.store_patient(patient)

    # ================= STEP 2 =================
    # Episode ingestion
    episode_memory = LongTermMemory()
    episode_memory.initialize()

    episode_input = EpisodeInput(
        patient_id=patient.patient_id,
        **episode_data,
    )

    ingestor = EpisodeIngestor(episode_memory)
    episode = ingestor.ingest(episode_input)

    # ================= STEP 3 =================
    # Memory-RAG retrieval
    retriever = CaseRetriever(episode_memory)
    case_memory = retriever.retrieve_case_context(
        patient_id=episode.patient_id,
        episode_summary=episode.state_summary,
    )

    case_context = build_case_context(
        episode.state_summary,
        case_memory["patient_history"],
        case_memory["population_cases"],
    )

    # ================= STEP 4 =================
    # Multi-agent reasoning loop
    loop = AgentLoop()
    agent_summary = loop.run(case_context)

    final_decision_text = synthesize_decision(
        case_context,
        agent_summary,
    )

    # ================= STEP 5 =================
    # Learning / memory update
    agent_confidences = []
    disagreement = False

    for r in agent_summary["raw_opinions"]:
        output = r["output"].lower()
        if "confidence" in output:
            try:
                agent_confidences.append(
                    float(output.split("confidence")[-1][:4])
                )
            except:
                pass
        if "disagree" in output:
            disagreement = True

    final_confidence = (
        sum(agent_confidences) / len(agent_confidences)
        if agent_confidences else 0.7
    )

    outcome = EpisodeOutcome(
        episode_id=episode.episode_id,
        decision=final_decision_text,
        reasoning_factors=[
            "Patient history considered",
            "Population-level memory retrieved",
            "Multi-agent consensus reasoning",
        ],
        confidence=round(final_confidence, 2),
        disagreement=disagreement,
    )

    updater = MemoryUpdater(episode_memory)
    updater.apply_outcome(outcome)

    # ================= FINAL OUTPUT =================
    return {
    "patient_id": episode.patient_id,   # ✅ ADD THIS
    "episode_id": episode.episode_id,
    "final_decision": final_decision_text,
    "confidence": final_confidence,
    "disagreement": disagreement,
}

