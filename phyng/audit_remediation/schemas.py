"""Schemas for v4.4.2 audit remediation."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


class AuditRemediationInputs(BaseModel):
    full_suite: dict = Field(default_factory=dict)
    status_permission: dict = Field(default_factory=dict)
    claim_leakage: dict = Field(default_factory=dict)
    test_logic: dict = Field(default_factory=dict)
    debt_boundary: dict = Field(default_factory=dict)
    metric_integrity: dict = Field(default_factory=dict)
    remediation_plan: dict = Field(default_factory=dict)
    missing_files: list[str] = Field(default_factory=list)


class StatusMappingRemediationRecord(BaseModel):
    status: str
    source_location: str
    occurrence_count: int
    current_mapping_state: str
    proposed_mapping_action: str
    canonical_permission: str | None = None
    evidence_level: str | None = None
    support_level: str | None = None
    risk_level: str | None = None
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    required_next_gate: str | None = None
    remediation_status: str
    notes: list[str] = Field(default_factory=list)


class StatusQuarantineRecord(BaseModel):
    status: str
    reason: str
    severity: str
    may_appear_in_reports: bool
    may_gate_claims: bool
    may_unlock_next_phase: bool
    replacement_status: str | None = None
    required_remediation: str


class TestHardeningPlanItem(BaseModel):
    test_file: str
    test_name: str
    issue_type: str
    current_weakness: str
    required_negative_fixture: str
    required_assertion_upgrade: str
    priority: str
    remediation_status: str


class TestHardeningResults(BaseModel):
    initial_status_only_count: int = 0
    hardened_test_count: int = 0
    remaining_status_only_count: int = 0
    negative_fixture_count_added: int = 0
    contradiction_fixture_count_added: int = 0
    debt_bypass_fixture_count_added: int = 0
    metric_misuse_fixture_count_added: int = 0
    recommendations: list[str] = Field(default_factory=list)


class ClaimLeakageRemediationRecord(BaseModel):
    leakage_id: str
    artifact_path: str
    claim_text: str
    leakage_status: str
    severity: str
    remediation_action: str
    rewritten_claim: str | None = None
    final_status: str
    blocks_next_gate: bool


class MetricIntegrityRemediationRecord(BaseModel):
    metric_name: str
    artifact_path: str
    misuse_risk: str
    remediation_action: str
    required_label: str
    forbidden_label: str | None = None
    final_status: str


class AcceptedResidualAuditDebt(BaseModel):
    debt_id: str
    source_issue_id: str
    category: str
    severity: str
    reason_accepted: str
    owner: str
    next_review_phase: str
    may_continue_pipeline: bool
    blocks_claims: list[str] = Field(default_factory=list)
    does_not_block: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PostRemediationAuditDelta(BaseModel):
    initial_nonblocking_issue_count: int = 0
    remaining_nonblocking_issue_count: int = 0
    initial_unmapped_status_count: int = 0
    remaining_unmapped_status_count: int = 0
    critical_unmapped_status_count: int = 0
    initial_status_only_test_issue_count: int = 0
    remaining_status_only_test_issue_count: int = 0
    blocker_count_before: int = 0
    blocker_count_after: int = 0
    claims_rewritten_count: int = 0
    metrics_relabelled_count: int = 0
    debt_items_accepted_count: int = 0
    continuation_gate: str


class ContinuationGate(BaseModel):
    gate_status: str
    can_continue_pipeline: bool
    recommended_next_phase: str
    required_before_v4_5: list[str] = Field(default_factory=list)
    accepted_residual_debt_ref: str
    blocked_claims: list[str] = Field(default_factory=list)
    allowed_claims: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class AuditRemediationCampaignResult(BaseModel):
    campaign_id: str = "PHYGN-AUDIT-REMEDIATION-v4_4_2"
    status: str
    canonical_status: CanonicalStatusRecord
    inputs_loaded: bool
    status_mapping_records: list[StatusMappingRemediationRecord] = Field(default_factory=list)
    quarantine_records: list[StatusQuarantineRecord] = Field(default_factory=list)
    test_hardening_plan: list[TestHardeningPlanItem] = Field(default_factory=list)
    test_hardening_results: TestHardeningResults = Field(default_factory=TestHardeningResults)
    claim_remediation_records: list[ClaimLeakageRemediationRecord] = Field(default_factory=list)
    metric_remediation_records: list[MetricIntegrityRemediationRecord] = Field(default_factory=list)
    residual_debt: list[AcceptedResidualAuditDebt] = Field(default_factory=list)
    delta: PostRemediationAuditDelta | None = None
    continuation_gate: ContinuationGate | None = None
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
