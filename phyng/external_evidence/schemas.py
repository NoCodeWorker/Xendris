"""Schemas for v4.5 external evidence sprint."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel


class TableReviewResult(BaseModel):
    review_id: str
    target_id: str
    source_id: str
    local_pdf_path: str | None
    page_number: int | None
    table_number: str | None
    candidate_value_text: str | None
    numeric_value: float | None
    unit: str | None
    uncertainty: float | None
    evidence_status: str
    blockers: list[str]
    next_action: str


class SupplementarySearchResult(BaseModel):
    search_id: str
    source_id: str
    target_ids: list[str]
    supplementary_path: str | None
    supplementary_url_or_reference: str | None
    file_hash: str | None
    expected_observables: list[str]
    found_numeric_values: bool
    candidate_records: list[dict[str, Any]]
    evidence_status: str
    blockers: list[str]


class PublicDatasetSearchResult(BaseModel):
    search_id: str
    source_id: str
    target_ids: list[str]
    repository_name: str | None
    repository_reference: str | None
    local_dataset_path: str | None
    dataset_hash: str | None
    expected_observables: list[str]
    found_numeric_values: bool
    candidate_records: list[dict[str, Any]]
    evidence_status: str
    blockers: list[str]


class ExternalYTrueCandidate(BaseModel):
    candidate_id: str
    acquisition_track: str
    target_id: str
    benchmark_id: str
    source_id: str
    source_hash: str
    observable_class: str
    normalized_variable_name: str
    candidate_value_text: str
    numeric_value: float | None
    unit: str | None
    uncertainty: float | None
    source_location_type: str
    source_location_value: str
    local_artifact_path: str | None
    local_artifact_hash: str | None
    extraction_method: str
    provenance_status: str
    qc_status: str
    matched_prediction_ids: list[str]
    can_enter_dataset: bool
    blockers: list[str]


class AcceptedExternalYTrueRecord(BaseModel):
    y_true_id: str
    candidate_id: str
    acquisition_track: str
    target_id: str
    benchmark_id: str
    source_id: str
    source_hash: str
    observable_class: str
    normalized_variable_name: str
    value: float
    unit: str
    uncertainty: float | None
    source_location_type: str
    source_location_value: str
    local_artifact_path: str | None
    local_artifact_hash: str | None
    extraction_method: str
    approximate: bool
    qc_status: str
    matched_prediction_ids: list[str]
    limitations: list[str]


class RejectedExternalYTrueRecord(BaseModel):
    candidate_id: str
    target_id: str
    source_id: str
    acquisition_track: str
    rejection_reason: str
    required_next_action: str
    claim_impact: str


class AssembledYTrueDatasetv45(BaseModel):
    dataset_id: str
    created_at: str
    previous_dataset_ref: str | None
    external_evidence_ref: str | None
    previous_y_true_count: int
    new_y_true_count: int
    total_y_true_count: int
    records: list[Any]
    ready_for_predictive_gain: bool
    predictive_gain_status: str
    minimum_viable_y_true_count: int
    matched_prediction_count: int
    slot4_debt_status: str
    physical_claim_permission: str
    notes: list[str]


class NextPredictiveGainInputsv45(BaseModel):
    ready_for_predictive_gain: bool
    predictive_gain_status: str
    minimum_viable_y_true_count: int
    recommended_next_phase: str
    y_true_dataset_path: str
    model_predictions_path: str
    accepted_y_true_count: int
    matched_prediction_count: int
    allowed_claims: list[str]
    blocked_claims: list[str]
    notes: list[str]


class CandidateFreezeDecision(BaseModel):
    decision_id: str
    accepted_y_true_count: int
    minimum_viable_y_true_count: int
    ready_for_predictive_gain: bool
    freeze_status: str
    freeze_reason: str | None
    allowed_future_work: list[str]
    blocked_future_work: list[str]
    required_to_unfreeze: list[str]
    recommended_next_phase: str


class CampaignResultv45(BaseModel):
    status: str
    accepted_records: int
    blocked_targets: int
    ready_for_predictive_gain: bool
