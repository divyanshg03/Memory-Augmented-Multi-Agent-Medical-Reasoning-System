from memory.qdrant_memory import LongTermMemory
from memory.schema import ReasoningEpisode
from reasoning.reasoner import MemoryAwareReasoner

# 1. Setup memory
memory = LongTermMemory()
memory.initialize()

# 2. Insert ONE episode (run once)
episode = ReasoningEpisode(
    state_summary="Chest tightness and anxiety symptoms",
    decision="Likely anxiety-related episode",
    reasoning_factors=[
        "Normal ECG",
        "High anxiety markers",
        "No pulmonary abnormality",
    ],
    confidence=0.9,
    domain="healthcare",
    disagreement=False,
)

memory.write_episode(episode)

# 3. Run reasoning
reasoner = MemoryAwareReasoner(memory)

result = reasoner.reason(
    query="Patient presents chest tightness with anxiety",
    domain="healthcare",
)

print("Used memory:", result["used_memory"])
print("\nGroq Response:\n")
print(result["response"])
