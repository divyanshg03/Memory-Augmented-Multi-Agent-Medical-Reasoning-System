from dataclasses import dataclass, field
import uuid
import time
from typing import List


@dataclass
class PatientProfile:
    patient_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str | None = None   # optional / anonymized
    age: int = 0
    gender: str = "unspecified"
    known_conditions: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    past_similar_episodes: bool = False
    risk_flags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=lambda: time.time())

    def embedding_text(self) -> str:
        """
        Minimal embedding for semantic linking (NOT heavy).
        """
        return (
            f"Age {self.age}, Gender {self.gender}, "
            f"Conditions {', '.join(self.known_conditions)}"
        )

    def payload(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "known_conditions": self.known_conditions,
            "medications": self.medications,
            "past_similar_episodes": self.past_similar_episodes,
            "risk_flags": self.risk_flags,
            "created_at": self.created_at,
        }
