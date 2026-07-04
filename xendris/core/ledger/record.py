"""TrustLedgerRecord definition for append-only trust events."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping
from xendris.core.ledger.event_type import TrustEventType


@dataclass(frozen=True)
class TrustLedgerRecord:
    """Immutable ledger record representing a deterministic trust decision event."""

    record_id: str
    run_id: str
    event_type: TrustEventType
    sequence_index: int
    source_component: str
    decision: str
    reason: str
    risk_level: str
    claim_id: str | None = None
    model_id: str | None = None
    provider: str | None = None
    limitations: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    input_hash: str = ""
    output_hash: str = ""
    previous_record_hash: str | None = None
    record_hash: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self, exclude_hash: bool = False) -> dict[str, Any]:
        """Convert the record to a serializable dictionary, optionally excluding the hash."""
        d = {
            "record_id": self.record_id,
            "run_id": self.run_id,
            "event_type": self.event_type.name,
            "sequence_index": self.sequence_index,
            "source_component": self.source_component,
            "decision": self.decision,
            "reason": self.reason,
            "risk_level": self.risk_level,
            "claim_id": self.claim_id,
            "model_id": self.model_id,
            "provider": self.provider,
            "limitations": list(self.limitations),
            "evidence_refs": list(self.evidence_refs),
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "previous_record_hash": self.previous_record_hash,
            "metadata": dict(sorted(self.metadata.items())),
        }
        if not exclude_hash:
            d["record_hash"] = self.record_hash
        return d

    def calculate_record_hash(self) -> str:
        """Compute the deterministic SHA-256 hash of the record contents."""
        serialized = json.dumps(self.to_dict(exclude_hash=True), sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
