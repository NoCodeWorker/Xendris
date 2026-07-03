"""Remediation plan builder for v4.4.1 audit issues."""

from __future__ import annotations

from phyng.full_suite_logic_audit.schemas import AuditIssue, RemediationItem, RemediationPlan


def build_remediation_plan(issues: list[AuditIssue]) -> RemediationPlan:
    blocking = [issue for issue in issues if issue.severity == "BLOCKER"]
    items = [
        RemediationItem(
            remediation_id=f"REMEDIATE-{index:03d}",
            issue_id=issue.issue_id,
            severity=issue.severity,
            required_action=issue.remediation,
            gate_effect="STOP_PIPELINE" if issue.severity == "BLOCKER" else "REVIEW_BEFORE_CONTINUATION",
        )
        for index, issue in enumerate(issues, start=1)
        if issue.severity in {"BLOCKER", "HIGH", "MEDIUM"}
    ]
    if blocking:
        return RemediationPlan(items=items, can_continue_pipeline=False, gate_status="STOP_BLOCKERS_PRESENT")
    if items:
        return RemediationPlan(items=items, can_continue_pipeline=True, gate_status="CONDITIONAL_CONTINUE_AFTER_REVIEW")
    return RemediationPlan(items=[], can_continue_pipeline=True, gate_status="CONTINUE")
