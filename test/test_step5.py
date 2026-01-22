from memory.memory_updater import MemoryUpdater
from memory.outcome_schema import EpisodeOutcome
from memory.qdrant_memory import LongTermMemory

# Episode memory (same collection as before)
episode_memory = LongTermMemory()
episode_memory.initialize()

# ⚠️ Replace this with REAL episode_id from Step 2
episode_id = "PUT_REAL_EPISODE_ID_HERE"

outcome = EpisodeOutcome(
    episode_id=episode_id,
    decision="Likely panic attack",
    reasoning_factors=[
        "Sudden onset",
        "Autonomic symptoms",
        "Past similar episodes",
        "No cardiac or neurological red flags",
    ],
    confidence=0.82,
    disagreement=False,
)

updater = MemoryUpdater(episode_memory)
updater.apply_outcome(outcome)

print("✅ Episode updated and learned from")
