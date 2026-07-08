"""v0.5.5 real-provider evidence integrity gate."""

from .evidence_gate import (
    EvidenceIntegrityConfig,
    evaluate_evidence_integrity,
    write_evidence_integrity_artifacts,
)

__all__ = [
    "EvidenceIntegrityConfig",
    "evaluate_evidence_integrity",
    "write_evidence_integrity_artifacts",
]
