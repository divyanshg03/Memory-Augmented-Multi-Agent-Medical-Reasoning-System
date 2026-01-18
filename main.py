from memory.qdrant_memory import LongTermMemory
from memory.schema import ReasoningEpisode


memory = LongTermMemory()
memory.initialize()

episode = ReasoningEpisode(
    state_summary="Flood evacuation planning in coastal region",
    decision="Early evacuation recommended",
    reasoning_factors=[
        "Rising water levels",
        "Past evacuation delays caused casualties",
        "Weather forecast worsening"
    ],
    confidence=0.9,
    disagreement=False,
    domain="disaster_response",
    tags=["flood", "evacuation"]
)

memory.write_episode(episode)
print("✅ Memory written to Qdrant Cloud")
