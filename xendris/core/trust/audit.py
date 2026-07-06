"""Reasoning audit model for the Xendris Trust Kernel."""

from __future__ import annotations

from dataclasses import dataclass

from .claims import Claim
from .types import AuditDecision, RiskLevel


def _validate_confidence(confidence: float) -> None:
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("global_confidence must be between 0.0 and 1.0")


@dataclass(frozen=True)
class ReasoningAudit:
    """Structural audit for an answer and its declared claims.

    This object represents audit posture. It does not prove factual truth,
    model quality, or external source support.
    """

    answer: str
    claims: tuple[Claim, ...]
    global_confidence: float
    risk_level: RiskLevel
    decision: AuditDecision
    unsupported_claims: tuple[Claim, ...] = ()
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.answer.strip():
            raise ValueError("answer must not be empty")
        _validate_confidence(self.global_confidence)
        object.__setattr__(self, "claims", tuple(self.claims))
        object.__setattr__(self, "unsupported_claims", tuple(self.unsupported_claims))

    def to_dict(self) -> dict[str, object]:
        """Return a simple JSON-compatible representation."""

        return {
            "answer": self.answer,
            "claims": [claim.to_dict() for claim in self.claims],
            "global_confidence": self.global_confidence,
            "risk_level": self.risk_level.value,
            "decision": self.decision.value,
            "unsupported_claims": [claim.to_dict() for claim in self.unsupported_claims],
            "notes": self.notes,
        }
