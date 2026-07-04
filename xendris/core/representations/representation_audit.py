"""RepresentationAudit implementation for tracking consistency gate decisions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from xendris.core.representations.representation import ClaimRepresentation
from xendris.core.representations.consistency_gate import RepresentationConsistencyDecision


@dataclass(frozen=True)
class RepresentationAudit:
    """A compact audit record of consistency gate decisions across representations."""

    audit_id: str
    representation_ids: tuple[str, ...]
    relation_summary: str
    final_decision: str
    reason: str
    recommended_claim_id: str | None
    rejected_claim_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    evidence_refs_used: tuple[str, ...]
    risk_level: str

    @classmethod
    def create(
        cls,
        audit_id: str,
        representations: list[ClaimRepresentation],
        decision: RepresentationConsistencyDecision,
    ) -> RepresentationAudit:
        """Create a RepresentationAudit record from a RepresentationConsistencyDecision."""
        evidence_used = []
        for r in representations:
            evidence_used.extend(r.evidence_refs)

        return cls(
            audit_id=audit_id,
            representation_ids=tuple(r.representation_id for r in representations),
            relation_summary=decision.relation.value,
            final_decision=decision.decision,
            reason=decision.reason,
            recommended_claim_id=decision.recommended_claim.representation_id if decision.recommended_claim else None,
            rejected_claim_ids=tuple(r.representation_id for r in decision.rejected_claims),
            limitations=decision.limitations,
            evidence_refs_used=tuple(set(evidence_used)),
            risk_level="MEDIUM",
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a simple JSON-compatible representation."""
        return {
            "audit_id": self.audit_id,
            "representation_ids": list(self.representation_ids),
            "relation_summary": self.relation_summary,
            "final_decision": self.final_decision,
            "recommended_claim_id": self.recommended_claim_id,
            "rejected_claim_ids": list(self.rejected_claim_ids),
            "limitations": list(self.limitations),
            "evidence_refs_used": list(self.evidence_refs_used),
            "risk_level": self.risk_level,
        }
