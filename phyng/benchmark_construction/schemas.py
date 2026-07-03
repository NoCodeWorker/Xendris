"""Schemas for v4.0 benchmark construction."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


class BenchmarkDatasetManifest(BaseModel):
    dataset_id: str
    candidate_family: str
    phi_family: str
    created_at: str
    source_pressure_ref: str
    validation_pack_ref: str
    debt_registry_ref: str
    benchmark_row_count: int
    observable_alignment_count: int
    negative_control_count: int
    excluded_claims: list[str] = Field(default_factory=list)
    allowed_usage: list[str] = Field(default_factory=list)
    blocked_usage: list[str] = Field(default_factory=list)
    status: str
    notes: list[str] = Field(default_factory=list)


class BenchmarkRow(BaseModel):
    benchmark_id: str
    source_id: str
    extract_id: str
    sha256: str
    page_number: int | None = None
    observable_type: str
    observable_text: str
    regime_text: str
    mass_range: str | None = None
    time_range: str | None = None
    length_or_separation_range: str | None = None
    temperature_or_pressure: str | None = None
    parameter_constraints: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    benchmark_use: str
    allowed_model_comparison: bool
    gradient_claim_allowed: bool = False


class ObservableAlignmentRecord(BaseModel):
    alignment_id: str
    source_id: str
    extract_id: str
    observable: str
    source_observable_text: str
    phygn_observable_mapping: str
    baseline_model_mapping: str
    candidate_model_mapping: str
    alignment_status: str
    limitations: list[str] = Field(default_factory=list)


class NegativeControl(BaseModel):
    control_id: str
    source_id: str
    slot_id: str
    control_type: str
    what_it_tests: str
    failure_condition: str
    expected_result_if_PHIGRADIENT_is_only_analogy: str
    expected_result_if_candidate_has_signal: str


class NegativeControlPlan(BaseModel):
    plan_id: str = "PHI-GRADIENT-NEGATIVE-CONTROL-PLAN-v4_0"
    created_at: str = "2026-07-01"
    controls: list[NegativeControl] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class BenchmarkConstructionGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    manifest: BenchmarkDatasetManifest
    rows: list[BenchmarkRow] = Field(default_factory=list)
    observable_alignment: list[ObservableAlignmentRecord] = Field(default_factory=list)
    negative_control_plan: NegativeControlPlan = Field(default_factory=NegativeControlPlan)
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


class BenchmarkConstructionCampaignResult(BaseModel):
    campaign_id: str = "PHI-GRADIENT-BENCHMARK-CONSTRUCTION-v4_0"
    status: str
    gate_result: BenchmarkConstructionGateResult
    report_paths: dict[str, str] = Field(default_factory=dict)


class BenchmarkConstructionInputs(BaseModel):
    source_pressure_decision: dict = Field(default_factory=dict)
    extract_pressure_map: dict = Field(default_factory=dict)
    slot_pressure_summary: dict = Field(default_factory=dict)
    benchmark_alignment: dict = Field(default_factory=dict)
    contradiction_map: dict = Field(default_factory=dict)
    next_model_update_recommendations: dict = Field(default_factory=dict)
    validation_ready_pack: dict = Field(default_factory=dict)
    source_hashes: dict = Field(default_factory=dict)
    blocked_reason: str | None = None
