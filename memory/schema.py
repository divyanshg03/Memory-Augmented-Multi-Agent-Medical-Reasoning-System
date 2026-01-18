from dataclasses import dataclass, field
from typing import List
from datetime import datetime
import time
import uuid
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

@dataclass
class ReasoningEpisode:
    episode_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    state_summary: str = ""
    decision: str = ""
    reasoning_factors: List[str] = field(default_factory=list)
    confidence: float = 0.0
    disagreement: bool = False
    validated: bool = False
    domain: str = "generic"
    tags: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=lambda: time.time())
    
    def embedding_text(self) -> str:
        """
        What actually gets embedded.
        This is the cognitive core of memory.
        """
        return (
            self.state_summary
            + " Decision: "
            + self.decision
            + " Reasoning: "
            + " ".join(self.reasoning_factors)
        )

    def payload(self) -> dict:
        """
        What gets stored as metadata in Qdrant.
        """
        return {
            "episode_id": self.episode_id,
            "state_summary": self.state_summary,
            "decision": self.decision,
            "reasoning_factors": self.reasoning_factors,
            "confidence": self.confidence,
            "disagreement": self.disagreement,
            "validated": self.validated,
            "domain": self.domain,
            "tags": self.tags,
            "timestamp": self.timestamp,
        }
