from dataclasses import dataclass
from typing import List


@dataclass
class EpisodeOutcome:
    episode_id: str
    decision: str
    reasoning_factors: List[str]
    confidence: float
    disagreement: bool
