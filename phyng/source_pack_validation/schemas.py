"""Schemas for v3.3 source-pack validation."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord
from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest


class SourcePackExtractValidationResult(BaseModel):
    extract_id: str
    source_id: str
    slot_id: str
    status: str
    counts_as_real_support: bool = False
    requires_manual_review: bool = False
    supported_components: list[str] = Field(default_factory=list)
    contradicted_components: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


class SourcePackValidatedExtract(BaseModel):
    extract_id: str
    source_id: str
    slot_id: str
    validation_status: str


class SourcePackSlotCoverageRecord(BaseModel):
    slot_id: str
    candidate_source_count: int = 0
    extract_count: int = 0
    validated_support_count: int = 0
    analogy_rejection_count: int = 0
    manual_review_count: int = 0
    contradiction_count: int = 0
    benchmark_comparable_count: int = 0
    coverage_status: str
    missing_requirements: list[str] = Field(default_factory=list)


class SourcePackSlotCoverageMatrix(BaseModel):
    records: list[SourcePackSlotCoverageRecord] = Field(default_factory=list)
    source_pressure_score: float = 0.0
    manual_review_debt: int = 0
    missing_slots: list[str] = Field(default_factory=list)


class SourcePackBenchmarkScoringResult(BaseModel):
    status: str
    benchmark_comparable_count: int = 0
    benchmark_score: float = 0.0
    missing_requirements: list[str] = Field(default_factory=list)


class SourcePackNegativePressureResult(BaseModel):
    status: str
    negative_pressure_count: int = 0
    negative_extract_ids: list[str] = Field(default_factory=list)


class PhiGradientSourcePackValidationGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    manifest: SeedSourceManifest | None = None
    extract_pack: SeedSourceExtractPack | None = None
    extract_validations: list[SourcePackExtractValidationResult] = Field(default_factory=list)
    validated_extracts: list[SourcePackValidatedExtract] = Field(default_factory=list)
    slot_coverage: SourcePackSlotCoverageMatrix
    benchmark_scoring: SourcePackBenchmarkScoringResult
    negative_pressure: SourcePackNegativePressureResult
    validated_support_count: int = 0
    manual_review_count: int = 0
    rejected_analogy_count: int = 0
    blocked_reason: str | None = None
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientSourcePackValidationCampaignResult(BaseModel):
    campaign_id: str
    status: str
    gate_result: PhiGradientSourcePackValidationGateResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
