"""LedgerAudit compiling verification outcomes over a ledger sequence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from xendris.core.ledger.record import TrustLedgerRecord
from xendris.core.ledger.event_type import TrustEventType
from xendris.core.ledger.hashchain import TrustHashChain


@dataclass(frozen=True)
class LedgerAudit:
    """Consolidated audit summary evaluating the integrity and decisions in a ledger run."""

    run_id: str
    record_count: int
    event_type_counts: dict[str, int]
    blocked_count: int
    human_review_count: int
    allowed_with_limitations_count: int
    selected_model_count: int
    rejected_model_count: int
    chain_valid: bool
    limitations: tuple[str, ...]

    @classmethod
    def summarize(cls, run_id: str, records: list[TrustLedgerRecord]) -> LedgerAudit:
        """Create a LedgerAudit record summarizing all events of the specified run ID."""
        run_records = [r for r in records if r.run_id == run_id]
        record_count = len(run_records)

        event_counts: dict[str, int] = {}
        blocked = 0
        human_review = 0
        allowed_limitations = 0
        selected_models: set[str] = set()
        rejected_models: set[str] = set()
        limitations: set[str] = set()

        for r in run_records:
            name = r.event_type.name
            event_counts[name] = event_counts.get(name, 0) + 1
            if r.decision == "BLOCK" or r.decision == "BLOCKED" or r.event_type == TrustEventType.CLAIM_BLOCKED:
                blocked += 1
            elif r.decision == "HUMAN_REVIEW" or r.decision == "HUMAN_REVIEW_REQUIRED" or r.event_type == TrustEventType.HUMAN_REVIEW_ROUTED:
                human_review += 1
            elif r.decision == "ALLOW_WITH_LIMITATIONS" or r.decision == "APPROVED_WITH_LIMITATIONS" or r.event_type == TrustEventType.CLAIM_ALLOWED_WITH_LIMITATIONS:
                allowed_limitations += 1

            if r.model_id:
                if r.event_type == TrustEventType.MODEL_SELECTED or r.event_type == TrustEventType.ROUTING_DECISION:
                    selected_models.add(r.model_id)
                elif r.event_type == TrustEventType.MODEL_REJECTED:
                    rejected_models.add(r.model_id)

            for limit in r.limitations:
                limitations.add(limit)

        # Check chain validity
        chain_valid = TrustHashChain.verify_chain(run_records)

        return cls(
            run_id=run_id,
            record_count=record_count,
            event_type_counts=event_counts,
            blocked_count=blocked,
            human_review_count=human_review,
            allowed_with_limitations_count=allowed_limitations,
            selected_model_count=len(selected_models),
            rejected_model_count=len(rejected_models),
            chain_valid=chain_valid,
            limitations=tuple(sorted(limitations)),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert the audit summary to a standard Python dictionary for serialization."""
        return {
            "run_id": self.run_id,
            "record_count": self.record_count,
            "event_type_counts": self.event_type_counts,
            "blocked_count": self.blocked_count,
            "human_review_count": self.human_review_count,
            "allowed_with_limitations_count": self.allowed_with_limitations_count,
            "selected_model_count": self.selected_model_count,
            "rejected_model_count": self.rejected_model_count,
            "chain_valid": self.chain_valid,
            "limitations": list(self.limitations),
        }
