"""Source acquisition record model for local fixture validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .acquisition_types import ContaminationRisk, OriginCandidate, SourceType


@dataclass(frozen=True)
class SourceAcquisitionRecord:
    source_id: str
    source_type: SourceType
    source_url: str | None
    retrieved_at: str | None
    license: str | None
    source_hash: str | None
    raw_snapshot_path: str | None
    normalized_snapshot_path: str | None
    adapted_task_path: str | None
    origin_candidate: OriginCandidate
    contamination_risk: ContaminationRisk
    adaptation_required: bool
    adaptation_notes: str | None
    promotion_allowed: bool = False
    rejection_reasons: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SourceAcquisitionRecord":
        return cls(
            source_id=str(payload.get("source_id", "")),
            source_type=SourceType(payload.get("source_type", "UNKNOWN")),
            source_url=payload.get("source_url"),
            retrieved_at=payload.get("retrieved_at"),
            license=payload.get("license"),
            source_hash=payload.get("source_hash"),
            raw_snapshot_path=payload.get("raw_snapshot_path"),
            normalized_snapshot_path=payload.get("normalized_snapshot_path"),
            adapted_task_path=payload.get("adapted_task_path"),
            origin_candidate=OriginCandidate(payload.get("origin_candidate", "UNKNOWN")),
            contamination_risk=ContaminationRisk(payload.get("contamination_risk", "BLOCKED")),
            adaptation_required=bool(payload.get("adaptation_required", False)),
            adaptation_notes=payload.get("adaptation_notes"),
            promotion_allowed=bool(payload.get("promotion_allowed", False)),
            rejection_reasons=tuple(payload.get("rejection_reasons", [])),
            warnings=tuple(payload.get("warnings", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_type": self.source_type.value,
            "source_url": self.source_url,
            "retrieved_at": self.retrieved_at,
            "license": self.license,
            "source_hash": self.source_hash,
            "raw_snapshot_path": self.raw_snapshot_path,
            "normalized_snapshot_path": self.normalized_snapshot_path,
            "adapted_task_path": self.adapted_task_path,
            "origin_candidate": self.origin_candidate.value,
            "contamination_risk": self.contamination_risk.value,
            "adaptation_required": self.adaptation_required,
            "adaptation_notes": self.adaptation_notes,
            "promotion_allowed": self.promotion_allowed,
            "rejection_reasons": list(self.rejection_reasons),
            "warnings": list(self.warnings),
        }

