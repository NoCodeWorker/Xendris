"""Types for smoke diagnostic scoring."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SmokeScoreRecord:
    task_id: str
    provider_name: str
    score_total: float
    score_components: dict[str, float]
    scoring_confidence: str
    scoring_limitations: list[str]
    statistical_claim_authorized: bool
    provider_superiority_claim_authorized: bool
    external_benchmark_validation_claim_authorized: bool

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
