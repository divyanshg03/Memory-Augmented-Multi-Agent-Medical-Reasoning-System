from memory.qdrant_memory import LongTermMemory
from memory.schema import ReasoningEpisode

memory = LongTermMemory()
memory.initialize()

episode = ReasoningEpisode(
    state_summary="Chest tightness with anxiety symptoms",
    decision="Likely anxiety-related episode",
    reasoning_factors=[
        "Normal ECG",
        "High anxiety markers",
        "No pulmonary abnormality"
    ],
    confidence=0.9,
    domain="healthcare",
    disagreement=False
)

memory.write_episode(episode)
print("✅ Episode inserted")
