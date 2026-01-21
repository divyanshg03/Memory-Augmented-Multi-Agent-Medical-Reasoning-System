from dataclasses import dataclass, field
import time
from typing import List


@dataclass
class EpisodeInput:
    patient_id: str
    symptoms: List[str]
    duration_minutes: int
    severity: int  # 1–10
    triggers: List[str] = field(default_factory=list)
    notes: str | None = None
    created_at: float = field(default_factory=lambda: time.time())

    def to_summary(self) -> str:
        return (
            f"Symptoms: {', '.join(self.symptoms)}. "
            f"Duration: {self.duration_minutes} minutes. "
            f"Severity: {self.severity}/10."
        )
