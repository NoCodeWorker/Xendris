"""Schemas for v3.4 exact extract review."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord
from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest


class ExactReviewedExtract(BaseModel):
    exact_extract_id: str
    source_id: str
    slot_id: str
    source_title: str | None = None
    location_type: str = "UNKNOWN_LOCATION_REQUIRES_REVIEW"
    location_value: str = ""
    exact_quote: str | None = None
    paraphrase_context: str | None = None
    equation_text: str | None = None
    observable_text: str | None = None
    parameter_range_text: str | None = None
    benchmark_range_text: str | None = None
    negative_constraint_text: str | None = None
    supported_components: list[str] = Field(default_factory=list)
    contradicted_components: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    review_status: str = "EXACT_EXTRACT_REQUIRES_LOCATION"
    reviewer_notes: list[str] = Field(default_factory=list)
    validation_ready: bool = False
    manual_review_required: bool = True


class ExactReviewedExtractPack(BaseModel):
    exact_extract_pack_id: str = "PHI-GRADIENT-EXACT-EXTRACT-PACK-v3_4"
    source_manifest_id: str = "PHI-GRADIENT-REVIEWED-SOURCE-PACK-v3_2"
    extracts: list[ExactReviewedExtract] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ExactExtractLocationValidationResult(BaseModel):
    exact_extract_id: str
    source_id: str
    slot_id: str
    status: str
    validation_ready: bool = False
    missing_requirements: list[str] = Field(default_factory=list)


class EquationObservableMapEntry(BaseModel):
    source_id: str
    exact_extract_id: str
    equation_text: str | None = None
    observable_text: str | None = None
    model_role: str
    slot_id: str
    candidate_relevance: str
    limitations: list[str] = Field(default_factory=list)


class EquationObservableMap(BaseModel):
    entries: list[EquationObservableMapEntry] = Field(default_factory=list)


class ParameterRangeMapEntry(BaseModel):
    source_id: str
    exact_extract_id: str
    mass_range: str | None = None
    length_or_separation_range: str | None = None
    time_range: str | None = None
    visibility_or_decoherence_measure: str | None = None
    environmental_conditions: str | None = None
    alpha_like_constraint: str | None = None
    gamma_env_constraint: str | None = None
    comparability_status: str
    missing_requirements: list[str] = Field(default_factory=list)


class ParameterRangeMap(BaseModel):
    entries: list[ParameterRangeMapEntry] = Field(default_factory=list)


class PhiGradientExactExtractReviewGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    manifest: SeedSourceManifest | None = None
    seed_extract_pack: SeedSourceExtractPack | None = None
    exact_extract_pack: ExactReviewedExtractPack
    location_results: list[ExactExtractLocationValidationResult] = Field(default_factory=list)
    equation_observable_map: EquationObservableMap
    parameter_range_map: ParameterRangeMap
    manual_review_debt_before: int = 0
    manual_review_debt_after: int = 0
    exact_extract_count: int = 0
    validation_ready_count: int = 0
    unresolved_extract_count: int = 0
    equation_map_count: int = 0
    observable_map_count: int = 0
    parameter_range_count: int = 0
    benchmark_range_count: int = 0
    negative_constraint_count: int = 0
    blocked_reason: str | None = None
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientExactExtractReviewCampaignResult(BaseModel):
    campaign_id: str
    status: str
    gate_result: PhiGradientExactExtractReviewGateResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
