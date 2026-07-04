"""TrustLedgerReader implementation for querying ledger records."""

from __future__ import annotations

from typing import Any
from xendris.core.ledger.event_type import TrustEventType
from xendris.core.ledger.record import TrustLedgerRecord
from xendris.core.ledger.writer import TrustLedgerWriter


class TrustLedgerReader:
    """Provides querying and filtering over trust ledger records."""

    def __init__(self, source: list[TrustLedgerRecord] | TrustLedgerWriter) -> None:
        if isinstance(source, TrustLedgerWriter):
            self._records = source.export_records()
        else:
            self._records = list(source)

    def list_records(self) -> list[TrustLedgerRecord]:
        """List all records in the reader."""
        return list(self._records)

    def find_by_run_id(self, run_id: str) -> list[TrustLedgerRecord]:
        """Find records matching the given run ID."""
        return [r for r in self._records if r.run_id == run_id]

    def find_by_claim_id(self, claim_id: str) -> list[TrustLedgerRecord]:
        """Find records matching the given claim ID."""
        return [r for r in self._records if r.claim_id == claim_id]

    def find_by_model_id(self, model_id: str) -> list[TrustLedgerRecord]:
        """Find records matching the given model ID."""
        return [r for r in self._records if r.model_id == model_id]

    def find_by_event_type(self, event_type: TrustEventType) -> list[TrustLedgerRecord]:
        """Find records matching the given event type."""
        return [r for r in self._records if r.event_type == event_type]

    def summarize_run(self, run_id: str) -> dict[str, Any]:
        """Compute aggregate summary stats for a run ID."""
        records = self.find_by_run_id(run_id)
        total = len(records)
        
        event_counts: dict[str, int] = {}
        blocked = 0
        human_review = 0
        allowed_limitations = 0
        selected_models: set[str] = set()
        rejected_models: set[str] = set()
        limitations: set[str] = set()

        for r in records:
            event_counts[r.event_type.name] = event_counts.get(r.event_type.name, 0) + 1
            if r.decision == "BLOCK" or r.decision == "BLOCKED":
                blocked += 1
            elif r.decision == "HUMAN_REVIEW" or r.decision == "HUMAN_REVIEW_REQUIRED":
                human_review += 1
            elif r.decision == "ALLOW_WITH_LIMITATIONS" or r.decision == "APPROVED_WITH_LIMITATIONS":
                allowed_limitations += 1

            if r.model_id:
                if r.event_type == TrustEventType.MODEL_SELECTED:
                    selected_models.add(r.model_id)
                elif r.event_type == TrustEventType.MODEL_REJECTED:
                    rejected_models.add(r.model_id)

            for limit in r.limitations:
                limitations.add(limit)

        return {
            "run_id": run_id,
            "total_records": total,
            "event_counts": event_counts,
            "blocked_count": blocked,
            "human_review_count": human_review,
            "allowed_with_limitations_count": allowed_limitations,
            "selected_models": list(selected_models),
            "rejected_models": list(rejected_models),
            "limitations": list(limitations),
        }
