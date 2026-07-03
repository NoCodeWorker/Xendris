"""Schemas for PHI_CURVATURE minimal source/y_true campaign v4.8."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


class PhiCurvatureMinimalInputs(BaseModel):
    screening_decision: dict = Field(default_factory=dict)
    source_screen: dict = Field(default_factory=dict)
    observable_screen: dict = Field(default_factory=dict)
    ytrue_screen: dict = Field(default_factory=dict)
    public_dataset_screen: dict = Field(default_factory=dict)
    experimental_feasibility_screen: dict = Field(default_factory=dict)
    claim_risk_screen: dict = Field(default_factory=dict)
    phi_gradient_method_only: dict = Field(default_factory=dict)
    slot4_debt: dict = Field(default_factory=dict)
    missing_files: list[str] = Field(default_factory=list)


class SourceResolutionRecord(BaseModel):
    source_ref_raw: str
    source_id: str | None = None
    title: str | None = None
    authors: list[str] = Field(default_factory=list)
    publication: str | None = None
    year: int | None = None
    volume: str | None = None
    page_or_article: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    url: str | None = None
    resolution_status: str
    confidence: str
    blockers: list[str] = Field(default_factory=list)


class SourceAvailabilityRecord(BaseModel):
    source_id: str
    local_pdf_available: bool = False
    local_pdf_path: str | None = None
    local_pdf_hash: str | None = None
    supplementary_available: bool = False
    supplementary_paths: list[str] = Field(default_factory=list)
    external_dataset_available: bool = False
    external_dataset_paths: list[str] = Field(default_factory=list)
    availability_status: str
    required_next_action: str


class PhiCurvatureCandidateObservable(BaseModel):
    observable_id: str
    candidate_family: str = "PHI_CURVATURE"
    source_id: str
    observable_class: str
    variable_name: str
    expected_unit: str | None = None
    source_location_type: str | None = None
    source_location_value: str | None = None
    candidate_text: str | None = None
    numeric_candidate_present: bool = False
    extraction_status: str
    blockers: list[str] = Field(default_factory=list)


class PhiCurvatureYTrueCandidate(BaseModel):
    candidate_id: str
    observable_id: str
    source_id: str
    source_hash: str | None = None
    observable_class: str
    variable_name: str
    value: float | None = None
    unit: str | None = None
    uncertainty: float | None = None
    source_location_type: str | None = None
    source_location_value: str | None = None
    extraction_method: str
    provenance_status: str
    qc_status: str
    matched_prediction_placeholder: bool = True
    can_enter_dataset: bool = False
    rejection_reason: str | None = None


class PhiCurvatureAcceptedYTrue(BaseModel):
    y_true_id: str
    candidate_id: str
    observable_id: str
    source_id: str
    source_hash: str
    observable_class: str
    variable_name: str
    value: float
    unit: str
    uncertainty: float | None = None
    source_location_type: str
    source_location_value: str
    extraction_method: str
    limitations: list[str] = Field(default_factory=list)


class PhiCurvatureRejectedYTrue(BaseModel):
    candidate_id: str
    observable_id: str
    source_id: str
    rejection_reason: str
    claim_impact: str
    required_next_action: str


class EvidenceAuditEvent(BaseModel):
    audit_id: str
    object_id: str
    event_type: str
    decision: str
    reason: str
    claim_impact: str


class PhiCurvatureMinimalYTrueDataset(BaseModel):
    dataset_id: str = "PHI-CURVATURE-MINIMAL-YTRUE-v4_8"
    candidate_family: str = "PHI_CURVATURE"
    accepted_ytrue_count: int = 0
    minimum_threshold: int = 3
    threshold_reached: bool = False
    records: list[dict] = Field(default_factory=list)
    predictive_gain_status: str = "UNDEFINED_NOT_COMPUTED_IN_MINIMAL_CAMPAIGN"
    physical_claim_permission: str = "BLOCKED"
    notes: list[str] = Field(default_factory=list)


class PhiCurvatureNextGateDecision(BaseModel):
    candidate_family: str = "PHI_CURVATURE"
    final_status: str
    accepted_ytrue_count: int
    threshold_reached: bool
    source_resolution_summary: dict = Field(default_factory=dict)
    source_availability_summary: dict = Field(default_factory=dict)
    blocked_claims: list[str] = Field(default_factory=list)
    allowed_claims: list[str] = Field(default_factory=list)
    allowed_next_phase: str | None = None
    blocked_next_phases: list[str] = Field(default_factory=list)
    required_before_predictive_gain: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PhiCurvatureMinimalCampaignResult(BaseModel):
    campaign_id: str = "PHI-CURVATURE-MINIMAL-SOURCE-YTRUE-CAMPAIGN-v4_8"
    status: str
    canonical_status: CanonicalStatusRecord
    inputs_loaded: bool
    source_resolution: list[SourceResolutionRecord] = Field(default_factory=list)
    source_availability: list[SourceAvailabilityRecord] = Field(default_factory=list)
    candidate_observables: list[PhiCurvatureCandidateObservable] = Field(default_factory=list)
    ytrue_candidates: list[PhiCurvatureYTrueCandidate] = Field(default_factory=list)
    accepted_ytrue: list[PhiCurvatureAcceptedYTrue] = Field(default_factory=list)
    rejected_ytrue: list[PhiCurvatureRejectedYTrue] = Field(default_factory=list)
    audit_trail: list[EvidenceAuditEvent] = Field(default_factory=list)
    dataset: PhiCurvatureMinimalYTrueDataset
    next_gate: PhiCurvatureNextGateDecision
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
