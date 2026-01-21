from memory.episode_input import EpisodeInput
from memory.schema import ReasoningEpisode


class EpisodeIngestor:
    def __init__(self, memory):
        self.memory = memory  # LongTermMemory

    def ingest(self, episode_input: EpisodeInput) -> ReasoningEpisode:
        """
        Store a raw episode before diagnosis.
        """

        episode = ReasoningEpisode(
            patient_id=episode_input.patient_id,
            state_summary=episode_input.to_summary(),
            decision="Pending expert reasoning",
            reasoning_factors=[],
            confidence=0.0,
            domain="healthcare",
            disagreement=False,
        )

        self.memory.write_episode(episode)
        return episode
