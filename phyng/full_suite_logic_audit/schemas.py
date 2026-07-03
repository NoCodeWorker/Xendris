"""Schemas for v4.4.1 full-suite logic audit."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


class AuditArtifact(BaseModel):
    path: str
    artifact_type: str
    exists: bool = True


class AuditIssue(BaseModel):
    issue_id: str
    severity: str
    category: str
    path: str
    message: str
    evidence: str | None = None
    remediation: str


class ArtifactScanResult(BaseModel):
    scanned_paths: list[str] = Field(default_factory=list)
    missing_scope_paths: list[str] = Field(default_factory=list)
    artifacts: list[AuditArtifact] = Field(default_factory=list)


class StatusPermissionMatrixEntry(BaseModel):
    domain_status: str
    domain: str
    canonical_permission: str
    evidence_level: str
    support_level: str
    risk_level: str | None = None
    mapped: bool = True


class StatusPermissionAuditResult(BaseModel):
    entries: list[StatusPermissionMatrixEntry] = Field(default_factory=list)
    unmapped_statuses: list[str] = Field(default_factory=list)
    issues: list[AuditIssue] = Field(default_factory=list)


class ClaimLeakageReport(BaseModel):
    issues: list[AuditIssue] = Field(default_factory=list)
    scanned_artifact_count: int = 0


class TestLogicAuditResult(BaseModel):
    issues: list[AuditIssue] = Field(default_factory=list)
    scanned_test_count: int = 0


class DebtBoundaryAuditResult(BaseModel):
    slot4_debt_open: bool = True
    issues: list[AuditIssue] = Field(default_factory=list)


class MetricIntegrityAuditResult(BaseModel):
    predictive_gain_issues: list[AuditIssue] = Field(default_factory=list)
    ytrue_issues: list[AuditIssue] = Field(default_factory=list)
    source_support_issues: list[AuditIssue] = Field(default_factory=list)
    negative_control_issues: list[AuditIssue] = Field(default_factory=list)

    @property
    def issues(self) -> list[AuditIssue]:
        return [
            *self.predictive_gain_issues,
            *self.ytrue_issues,
            *self.source_support_issues,
            *self.negative_control_issues,
        ]


class RemediationItem(BaseModel):
    remediation_id: str
    issue_id: str
    severity: str
    required_action: str
    gate_effect: str


class RemediationPlan(BaseModel):
    items: list[RemediationItem] = Field(default_factory=list)
    can_continue_pipeline: bool = False
    gate_status: str = "STOP"


class FullSuiteLogicAuditResult(BaseModel):
    campaign_id: str = "PHYGN-FULL-SUITE-LOGIC-AUDIT-v4_4_1"
    status: str
    canonical_status: CanonicalStatusRecord
    artifact_scan: ArtifactScanResult
    status_permission_audit: StatusPermissionAuditResult
    claim_leakage_report: ClaimLeakageReport
    test_logic_audit: TestLogicAuditResult
    debt_boundary_audit: DebtBoundaryAuditResult
    metric_integrity_audit: MetricIntegrityAuditResult
    remediation_plan: RemediationPlan
    blocker_count: int = 0
    nonblocking_issue_count: int = 0
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
