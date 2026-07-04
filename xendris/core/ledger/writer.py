"""Append-only TrustLedgerWriter implementation."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import Any, Mapping
from xendris.core.ledger.event_type import TrustEventType
from xendris.core.ledger.record import TrustLedgerRecord


class TrustLedgerWriter:
    """Deterministic, append-only ledger writer linking records via hash chain."""

    def __init__(self) -> None:
        self._records: list[TrustLedgerRecord] = []

    def append(self, record: TrustLedgerRecord) -> TrustLedgerRecord:
        """Calculate link hashes, set sequence index, hash, and append record."""
        sequence_index = len(self._records)
        prev_hash = self._records[-1].record_hash if self._records else None

        # Build intermediate record with links
        linked_record = replace(
            record,
            sequence_index=sequence_index,
            previous_record_hash=prev_hash,
        )

        # Compute hash and write final record
        final_hash = linked_record.calculate_record_hash()
        final_record = replace(linked_record, record_hash=final_hash)

        self._records.append(final_record)
        return final_record

    def append_event(
        self,
        record_id: str,
        run_id: str,
        event_type: TrustEventType,
        source_component: str,
        decision: str,
        reason: str,
        risk_level: str,
        claim_id: str | None = None,
        model_id: str | None = None,
        provider: str | None = None,
        limitations: tuple[str, ...] = (),
        evidence_refs: tuple[str, ...] = (),
        input_hash: str = "",
        output_hash: str = "",
        metadata: Mapping[str, Any] | None = None,
    ) -> TrustLedgerRecord:
        """Construct and append a new event to the ledger."""
        record = TrustLedgerRecord(
            record_id=record_id,
            run_id=run_id,
            event_type=event_type,
            sequence_index=0,
            source_component=source_component,
            decision=decision,
            reason=reason,
            risk_level=risk_level,
            claim_id=claim_id,
            model_id=model_id,
            provider=provider,
            limitations=limitations,
            evidence_refs=evidence_refs,
            input_hash=input_hash,
            output_hash=output_hash,
            metadata=metadata if metadata is not None else {},
        )
        return self.append(record)

    def write_jsonl(self, path: str) -> None:
        """Write all ledger records to a JSONL file."""
        with open(path, "w", encoding="utf-8") as f:
            for record in self._records:
                line = json.dumps(record.to_dict())
                f.write(line + "\n")

    def export_records(self) -> list[TrustLedgerRecord]:
        """Return the current list of records."""
        return list(self._records)

    def clear(self) -> None:
        """Reset the ledger records list (intended for test-mode only)."""
        self._records.clear()
