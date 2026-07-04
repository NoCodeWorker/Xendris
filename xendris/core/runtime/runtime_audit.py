"""RuntimeAudit compiling execution results and decisions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RuntimeAudit:
    """Immutable audit record consolidating all claims, routing, and final decisions of a runtime execution."""

    runtime_id: str
    request_id: str
    selected_model_id: str | None
    total_claims: int
    allowed_claims: int
    limited_claims: int
    hypothesis_claims: int
    blocked_claims: int
    human_review_claims: int
    ledger_record_count: int
    final_decision: str
    limitations: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Convert the runtime audit to a dictionary representation."""
        return {
            "runtime_id": self.runtime_id,
            "request_id": self.request_id,
            "selected_model_id": self.selected_model_id,
            "total_claims": self.total_claims,
            "allowed_claims": self.allowed_claims,
            "limited_claims": self.limited_claims,
            "hypothesis_claims": self.hypothesis_claims,
            "blocked_claims": self.blocked_claims,
            "human_review_claims": self.human_review_claims,
            "ledger_record_count": self.ledger_record_count,
            "final_decision": self.final_decision,
            "limitations": list(self.limitations),
        }
