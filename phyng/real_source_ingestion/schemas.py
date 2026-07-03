"""Schemas for real literature ingestion and PHI_GRADIENT source gates."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord


class RealSourceManifestEntry(BaseModel):
    source_id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    source_type: str
    acquisition_method: str
    url: str | None = None
    local_path: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    slots_targeted: list[str] = Field(default_factory=list)
    acquisition_status: str
    ingestion_status: str = "REAL_SOURCE_NOT_INGESTED"
    notes: list[str] = Field(default_factory=list)
    is_fixture: bool = False
    is_test_double: bool = False


class RealSourceManifest(BaseModel):
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    entries: list[RealSourceManifestEntry] = Field(default_factory=list)
    fixture_entries: list[str] = Field(default_factory=list)
    real_entries: list[str] = Field(default_factory=list)
    test_double_entries: list[str] = Field(default_factory=list)
    actual_real_sources_ingested: bool = False
    status: str


class RealSourceExtract(BaseModel):
    extract_id: str
    source_id: str
    slot_id: str
    extracted_text_or_paraphrase: str
    exact_quote_available: bool = False
    equation_text: str | None = None
    observable_text: str | None = None
    parameter_constraint_text: str | None = None
    benchmark_data_text: str | None = None
    supported_components: list[str] = Field(default_factory=list)
    contradicted_components: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    extractor_notes: list[str] = Field(default_factory=list)
    validation_status: str = "EXTRACT_REQUIRES_MANUAL_REVIEW"
    is_fixture: bool = False
    is_test_double: bool = False


class RealSourceExtractValidationResult(BaseModel):
    extract_id: str
    source_id: str
    status: str
    counts_as_real_support: bool
    slot_id: str
    supported_components: list[str] = Field(default_factory=list)
    contradicted_components: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


class RealBenchmarkRecord(BaseModel):
    benchmark_id: str
    source_id: str
    observable: str
    parameter_ranges: dict[str, tuple[float, float]] = Field(default_factory=dict)
    comparison_variable: str | None = None
    data_table_or_values: str | None = None
    limitations: list[str] = Field(default_factory=list)
    comparable_to_phi_gradient: bool = False
    is_fixture: bool = False
    is_test_double: bool = False


class PhiGradientRealSourceGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    manifest: RealSourceManifest
    validations: list[RealSourceExtractValidationResult] = Field(default_factory=list)
    benchmarks: list[RealBenchmarkRecord] = Field(default_factory=list)
    accepted_real_support_extracts: list[str] = Field(default_factory=list)
    rejected_analogy_extracts: list[str] = Field(default_factory=list)
    negative_extracts: list[str] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    actual_real_sources_ingested: bool = False
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientRealLiteratureCampaignResult(BaseModel):
    campaign_id: str
    status: str
    gate_result: PhiGradientRealSourceGateResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
