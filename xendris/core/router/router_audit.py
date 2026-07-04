"""RouterAudit record definition for serialization and determinism checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from xendris.core.router.route_request import RouteDecision


@dataclass(frozen=True)
class RouterAudit:
    """A deterministic audit record documenting a routing decision."""

    route_id: str
    request_id: str
    selected_model_id: str | None
    rejected_models: tuple[str, ...]
    decision: str
    reason: str
    required_gates: tuple[str, ...]
    estimated_cost: float
    estimated_latency_ms: int
    limitations: tuple[str, ...]
    audit_tags: tuple[str, ...]

    @classmethod
    def create(
        cls,
        route_id: str,
        request_id: str,
        decision: RouteDecision,
    ) -> RouterAudit:
        """Create a deterministic RouterAudit record from a RouteDecision."""
        return cls(
            route_id=route_id,
            request_id=request_id,
            selected_model_id=decision.selected_model_id,
            rejected_models=decision.rejected_models,
            decision=decision.decision,
            reason=decision.reason,
            required_gates=decision.required_gates,
            estimated_cost=decision.estimated_cost,
            estimated_latency_ms=decision.estimated_latency_ms,
            limitations=decision.limitations,
            audit_tags=decision.audit_tags,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert the audit to a standard Python dictionary for serialization."""
        return {
            "route_id": self.route_id,
            "request_id": self.request_id,
            "selected_model_id": self.selected_model_id,
            "rejected_models": list(self.rejected_models),
            "decision": self.decision,
            "reason": self.reason,
            "required_gates": list(self.required_gates),
            "estimated_cost": self.estimated_cost,
            "estimated_latency_ms": self.estimated_latency_ms,
            "limitations": list(self.limitations),
            "audit_tags": list(self.audit_tags),
        }
