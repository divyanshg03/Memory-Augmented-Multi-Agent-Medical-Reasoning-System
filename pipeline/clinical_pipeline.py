from memory.episode_ingestion import EpisodeIngestor
from memory.case_retrieval import CaseRetriever
from memory.case_context import build_case_context
from agents.agent_loop import AgentLoop
from agents.consensus import synthesize_decision
from memory.memory_updater import MemoryUpdater
from memory.outcome_schema import EpisodeOutcome
def run_clinical_pipeline(
    episode_input,
    episode_memory,
):
    """
    Runs Step 2 → Step 5 end-to-end.
    """

    # ---------------- STEP 2 ----------------
    ingestor = EpisodeIngestor(episode_memory)
    episode = ingestor.ingest(episode_input)

    print(f"🧾 Episode ingested: {episode.episode_id}")

    # ---------------- STEP 3 ----------------
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

    # ---------------- STEP 4 ----------------
    loop = AgentLoop()
    agent_summary = loop.run(case_context)

    final_text = synthesize_decision(case_context, agent_summary)

    print("🧠 Final synthesized decision generated")

    # ---------------- STEP 5 ----------------
    # Simple, transparent heuristics
    agent_confidences = []
    disagreement = False

    for r in agent_summary["raw_opinions"]:
        output = r["output"].lower()
        if "confidence" in output:
            try:
                agent_confidences.append(float(output.split("confidence")[-1][:4]))
            except:
                pass
        if "disagree" in output:
            disagreement = True

    final_confidence = (
        sum(agent_confidences) / len(agent_confidences)
        if agent_confidences else 0.7
    )

    outcome = EpisodeOutcome(
        episode_id=episode.episode_id,  # 🔑 SAME ID
        decision=final_text,
        reasoning_factors=[
            "Multi-agent consensus",
            "Patient history considered",
            "Population-level similarity used",
        ],
        confidence=round(final_confidence, 2),
        disagreement=disagreement,
    )

    updater = MemoryUpdater(episode_memory)
    updater.apply_outcome(outcome)

    print("📚 Episode updated and learned from")

    return {
        "episode_id": episode.episode_id,
        "final_decision": final_text,
        "confidence": final_confidence,
        "disagreement": disagreement,
    }
