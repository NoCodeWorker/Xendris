"""Expansion candidate model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .expansion_types import ExpansionReadiness, ExpansionSourceClass, FreezeRecommendation


@dataclass(frozen=True)
class ExpansionCandidate:
    expansion_candidate_id: str
    source_id: str
    source_origin: ExpansionSourceClass
    source_type: str
    source_url: str | None
    source_license: str | None
    acquisition_record_ref: str | None
    adaptation_record_ref: str | None
    proposed_task_ref: str | None
    proposed_task_hash: str | None
    provenance_ref: str | None
    contamination_risk: str
    leakage_risk: str
    task_validity_status: str
    benchmark_fit_status: str
    difficulty_estimate: str
    semantic_preservation_score: float
    structural_change_score: float
    difficulty_shift_score: float
    human_review_required: bool
    human_review_status: str
    expansion_readiness: ExpansionReadiness = ExpansionReadiness.NEEDS_MORE_VALIDATION
    freeze_recommendation: FreezeRecommendation = FreezeRecommendation.DO_NOT_RECOMMEND
    rejection_reasons: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    provider_execution_required: bool = False
    network_required: bool = False
    secrets_required: bool = False
    external_superiority_claim_authorized: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExpansionCandidate":
        return cls(
            expansion_candidate_id=data["expansion_candidate_id"],
            source_id=data["source_id"],
            source_origin=ExpansionSourceClass(data.get("source_origin", "UNKNOWN")),
            source_type=data.get("source_type", "UNKNOWN"),
            source_url=data.get("source_url"),
            source_license=data.get("source_license"),
            acquisition_record_ref=data.get("acquisition_record_ref"),
            adaptation_record_ref=data.get("adaptation_record_ref"),
            proposed_task_ref=data.get("proposed_task_ref"),
            proposed_task_hash=data.get("proposed_task_hash"),
            provenance_ref=data.get("provenance_ref"),
            contamination_risk=data.get("contamination_risk", "UNKNOWN"),
            leakage_risk=data.get("leakage_risk", "UNKNOWN"),
            task_validity_status=data.get("task_validity_status", "UNKNOWN"),
            benchmark_fit_status=data.get("benchmark_fit_status", "UNKNOWN"),
            difficulty_estimate=data.get("difficulty_estimate", "unknown"),
            semantic_preservation_score=float(data.get("semantic_preservation_score", 0.0)),
            structural_change_score=float(data.get("structural_change_score", 1.0)),
            difficulty_shift_score=float(data.get("difficulty_shift_score", 1.0)),
            human_review_required=bool(data.get("human_review_required", False)),
            human_review_status=data.get("human_review_status", "NOT_REQUIRED"),
            expansion_readiness=ExpansionReadiness(data.get("expansion_readiness", "NEEDS_MORE_VALIDATION")),
            freeze_recommendation=FreezeRecommendation(data.get("freeze_recommendation", "DO_NOT_RECOMMEND")),
            rejection_reasons=tuple(data.get("rejection_reasons", [])),
            warnings=tuple(data.get("warnings", [])),
            provider_execution_required=bool(data.get("provider_execution_required", False)),
            network_required=bool(data.get("network_required", False)),
            secrets_required=bool(data.get("secrets_required", False)),
            external_superiority_claim_authorized=bool(data.get("external_superiority_claim_authorized", False)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "expansion_candidate_id": self.expansion_candidate_id,
            "source_id": self.source_id,
            "source_origin": self.source_origin.value,
            "source_type": self.source_type,
            "source_url": self.source_url,
            "source_license": self.source_license,
            "acquisition_record_ref": self.acquisition_record_ref,
            "adaptation_record_ref": self.adaptation_record_ref,
            "proposed_task_ref": self.proposed_task_ref,
            "proposed_task_hash": self.proposed_task_hash,
            "provenance_ref": self.provenance_ref,
            "contamination_risk": self.contamination_risk,
            "leakage_risk": self.leakage_risk,
            "task_validity_status": self.task_validity_status,
            "benchmark_fit_status": self.benchmark_fit_status,
            "difficulty_estimate": self.difficulty_estimate,
            "semantic_preservation_score": self.semantic_preservation_score,
            "structural_change_score": self.structural_change_score,
            "difficulty_shift_score": self.difficulty_shift_score,
            "human_review_required": self.human_review_required,
            "human_review_status": self.human_review_status,
            "expansion_readiness": self.expansion_readiness.value,
            "freeze_recommendation": self.freeze_recommendation.value,
            "rejection_reasons": list(self.rejection_reasons),
            "warnings": list(self.warnings),
            "provider_execution_required": self.provider_execution_required,
            "network_required": self.network_required,
            "secrets_required": self.secrets_required,
            "external_superiority_claim_authorized": self.external_superiority_claim_authorized,
        }
