class MemoryUpdater:
    def __init__(self, episode_memory):
        """
        episode_memory: LongTermMemory
        """
        self.memory = episode_memory

    def apply_outcome(self, outcome):
        """
        Apply final reasoning outcome to an existing episode.
        """

        # 1. Mark episode as validated + update confidence
        self.memory.update_episode(
            episode_id=outcome.episode_id,
            validated=True,
            confidence=outcome.confidence,
        )

        # 2. Update decision-related fields
        self.memory.client().set_payload(
            collection_name=self.memory.collection,
            payload={
                "decision": outcome.decision,
                "reasoning_factors": outcome.reasoning_factors,
                "disagreement": outcome.disagreement,
            },
            points=[outcome.episode_id],
        )
