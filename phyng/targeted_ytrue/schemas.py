"""Schemas for v5.7.3 targeted y_true extraction."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TargetedYTrueCandidate(BaseModel):
    ytrue_candidate_id: str
    input_location_id: str
    source_id: str
    source_title: str
    source_year: int | None = None
    source_identity: dict = Field(default_factory=dict)
    local_pdf_path: str
    local_pdf_hash: str
    page_number: int | None = None
    location_label: str
    observable_class: str
    variable_name: str
    numeric_value: float | None = None
    original_value_text: str | None = None
    unit: str | None = None
    normalized_unit: str | None = None
    conditions: dict = Field(default_factory=dict)
    extraction_method: str
    provenance_status: str
    qc_status: str
    limitations: list[str] = Field(default_factory=list)
    rejection_reason: str | None = None


class AcceptedTargetedYTrue(BaseModel):
    y_true_id: str
    dataset_version: str = "v5.7.3"
    source_id: str
    source_title: str
    source_authors_or_authority: str
    source_year: int
    source_doi_or_arxiv_or_url: str
    local_pdf_path: str
    local_pdf_hash: str
    page_number: int
    location_label: str
    observable_class: str
    variable_name: str
    value_numeric: float
    original_value_text: str
    unit: str
    normalized_unit: str
    conditions: dict = Field(default_factory=dict)
    extraction_method: str
    provenance_status: str
    qc_status: str
    limitations: list[str] = Field(default_factory=list)
    claim_impact: str = "DATASET_EXPANSION_ONLY"


class RejectedTargetedYTrue(BaseModel):
    ytrue_candidate_id: str
    input_location_id: str
    source_id: str
    rejection_reason: str
    qc_status: str
    notes: list[str] = Field(default_factory=list)


class YTrueAuditRecord(BaseModel):
    candidate_id: str
    input_location_id: str
    source_id: str
    decision: str
    decision_reason: str
    checks_passed: list[str] = Field(default_factory=list)
    checks_failed: list[str] = Field(default_factory=list)
    normalization_actions: list[str] = Field(default_factory=list)
    deduplication_actions: list[str] = Field(default_factory=list)
    reviewer_notes: list[str] = Field(default_factory=list)


class DatasetQuality(BaseModel):
    dataset_id: str
    total_accepted_ytrue_count: int
    new_accepted_ytrue_count: int
    independent_source_count: int
    observable_class_distribution: dict = Field(default_factory=dict)
    qc_status_distribution: dict = Field(default_factory=dict)
    source_distribution: dict = Field(default_factory=dict)
    condition_key_distribution: dict = Field(default_factory=dict)
    limitation_flags: list[str] = Field(default_factory=list)
    quality_status: str
    benchmark_readiness: str
    notes: list[str] = Field(default_factory=list)


class TargetedYTrueCampaignResult(BaseModel):
    campaign_id: str = "FRONTERA-C-TARGETED-YTRUE-EXTRACTION-v5_7_3"
    status: str
    candidates: list[TargetedYTrueCandidate] = Field(default_factory=list)
    accepted: list[AcceptedTargetedYTrue] = Field(default_factory=list)
    rejected: list[RejectedTargetedYTrue] = Field(default_factory=list)
    audit_trail: list[YTrueAuditRecord] = Field(default_factory=list)
    expanded_dataset: dict = Field(default_factory=dict)
    dataset_quality: DatasetQuality | None = None
    next_gate_decision: dict = Field(default_factory=dict)
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
