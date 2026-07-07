"""Adaptation record model for v0.3.3 audit examples."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from benchmarks.finitexo_code_matrix_v0_3.source_acquisition import ContaminationRisk, OriginCandidate

from .adaptation_types import (
    AdaptationType,
    BenchmarkFitStatus,
    LeakageRisk,
    PromotionRecommendation,
    TaskValidityStatus,
)


@dataclass(frozen=True)
class AdaptationRecord:
    adaptation_id: str
    source_id: str
    acquisition_record_path: str | None
    source_origin_candidate: OriginCandidate
    adapted_candidate_path: str | None
    normalized_source_path: str | None
    raw_source_hash: str | None
    adapted_candidate_hash: str | None
    adaptation_type: AdaptationType
    adaptation_summary: str | None
    semantic_preservation_score: float
    structural_change_score: float
    difficulty_shift_score: float
    contamination_risk: ContaminationRisk
    leakage_risk: LeakageRisk
    task_validity_status: TaskValidityStatus
    benchmark_fit_status: BenchmarkFitStatus
    requires_human_review: bool
    promotion_recommendation: PromotionRecommendation
    rejection_reasons: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    task_metadata: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AdaptationRecord":
        return cls(
            adaptation_id=str(payload.get("adaptation_id", "")),
            source_id=str(payload.get("source_id", "")),
            acquisition_record_path=payload.get("acquisition_record_path"),
            source_origin_candidate=OriginCandidate(payload.get("source_origin_candidate", "UNKNOWN")),
            adapted_candidate_path=payload.get("adapted_candidate_path"),
            normalized_source_path=payload.get("normalized_source_path"),
            raw_source_hash=payload.get("raw_source_hash"),
            adapted_candidate_hash=payload.get("adapted_candidate_hash"),
            adaptation_type=AdaptationType(payload.get("adaptation_type", "UNKNOWN")),
            adaptation_summary=payload.get("adaptation_summary"),
            semantic_preservation_score=float(payload.get("semantic_preservation_score", 0.0)),
            structural_change_score=float(payload.get("structural_change_score", 1.0)),
            difficulty_shift_score=float(payload.get("difficulty_shift_score", 1.0)),
            contamination_risk=ContaminationRisk(payload.get("contamination_risk", "BLOCKED")),
            leakage_risk=LeakageRisk(payload.get("leakage_risk", "BLOCKED")),
            task_validity_status=TaskValidityStatus(payload.get("task_validity_status", "BLOCKED")),
            benchmark_fit_status=BenchmarkFitStatus(payload.get("benchmark_fit_status", "BLOCKED")),
            requires_human_review=bool(payload.get("requires_human_review", False)),
            promotion_recommendation=PromotionRecommendation(payload.get("promotion_recommendation", "DO_NOT_PROMOTE")),
            rejection_reasons=tuple(payload.get("rejection_reasons", [])),
            warnings=tuple(payload.get("warnings", [])),
            task_metadata=payload.get("task_metadata") or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "adaptation_id": self.adaptation_id,
            "source_id": self.source_id,
            "acquisition_record_path": self.acquisition_record_path,
            "source_origin_candidate": self.source_origin_candidate.value,
            "adapted_candidate_path": self.adapted_candidate_path,
            "normalized_source_path": self.normalized_source_path,
            "raw_source_hash": self.raw_source_hash,
            "adapted_candidate_hash": self.adapted_candidate_hash,
            "adaptation_type": self.adaptation_type.value,
            "adaptation_summary": self.adaptation_summary,
            "semantic_preservation_score": self.semantic_preservation_score,
            "structural_change_score": self.structural_change_score,
            "difficulty_shift_score": self.difficulty_shift_score,
            "contamination_risk": self.contamination_risk.value,
            "leakage_risk": self.leakage_risk.value,
            "task_validity_status": self.task_validity_status.value,
            "benchmark_fit_status": self.benchmark_fit_status.value,
            "requires_human_review": self.requires_human_review,
            "promotion_recommendation": self.promotion_recommendation.value,
            "rejection_reasons": list(self.rejection_reasons),
            "warnings": list(self.warnings),
            "task_metadata": self.task_metadata or {},
        }

