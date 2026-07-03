"""Markdown reports for v4.4.1 full-suite logic audit."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.full_suite_logic_audit.schemas import AuditIssue, FullSuiteLogicAuditResult


def write_full_suite_logic_audit_reports(result: FullSuiteLogicAuditResult, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    audit_dir = root / "audits"
    campaign_dir = root / "campaigns"
    audit_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "full_suite": audit_dir / "phygn_full_suite_logic_audit_v4_4_1.md",
        "status_permission": audit_dir / "phygn_status_permission_matrix_v4_4_1.md",
        "claim_leakage": audit_dir / "phygn_claim_leakage_report_v4_4_1.md",
        "test_logic": audit_dir / "phygn_test_logic_audit_v4_4_1.md",
        "debt_boundary": audit_dir / "phygn_debt_boundary_audit_v4_4_1.md",
        "metric_integrity": audit_dir / "phygn_metric_integrity_audit_v4_4_1.md",
        "remediation": audit_dir / "phygn_remediation_plan_v4_4_1.md",
        "campaign": campaign_dir / "PHYGN-FULL-SUITE-LOGIC-AUDIT-v4_4_1.md",
    }
    renderers = {
        "full_suite": _render_full,
        "status_permission": _render_status,
        "claim_leakage": _render_claims,
        "test_logic": _render_tests,
        "debt_boundary": _render_debt,
        "metric_integrity": _render_metrics,
        "remediation": _render_remediation,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: FullSuiteLogicAuditResult, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="PHYGN Full Suite Logic Audit v4.4.1",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="full_suite_logic_audit",
        reports_generated=reports_generated or [],
        next_actions=_next_actions(result),
        discipline_note="The audit checks logical consistency only. It does not validate PHI_GRADIENT, Frontera C, or PredictiveGain.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_full(result: FullSuiteLogicAuditResult) -> str:
    return "\n".join([
        "# PHYGN Full Suite Logic Audit v4.4.1",
        "",
        f"- status: `{result.status}`",
        f"- scanned_artifact_count: `{len(result.artifact_scan.artifacts)}`",
        f"- missing_scope_paths: `{len(result.artifact_scan.missing_scope_paths)}`",
        f"- blocker_count: `{result.blocker_count}`",
        f"- nonblocking_issue_count: `{result.nonblocking_issue_count}`",
        f"- can_continue_pipeline: `{result.remediation_plan.can_continue_pipeline}`",
        f"- gate_status: `{result.remediation_plan.gate_status}`",
    ]) + "\n"


def _render_status(result: FullSuiteLogicAuditResult) -> str:
    lines = ["# PHYGN Status Permission Matrix v4.4.1", "", f"- mapped_status_count: `{len(result.status_permission_audit.entries)}`", f"- unmapped_status_count: `{len(result.status_permission_audit.unmapped_statuses)}`", ""]
    for entry in result.status_permission_audit.entries[-80:]:
        lines.append(f"- `{entry.domain_status}`: `{entry.canonical_permission}`, evidence=`{entry.evidence_level}`, support=`{entry.support_level}`")
    if result.status_permission_audit.unmapped_statuses:
        lines.extend(["", "## Unmapped Statuses", "", *[f"- `{status}`" for status in result.status_permission_audit.unmapped_statuses[:80]]])
    return "\n".join(lines) + "\n"


def _render_claims(result: FullSuiteLogicAuditResult) -> str:
    return _render_issue_report("PHYGN Claim Leakage Report v4.4.1", result.claim_leakage_report.issues)


def _render_tests(result: FullSuiteLogicAuditResult) -> str:
    return _render_issue_report("PHYGN Test Logic Audit v4.4.1", result.test_logic_audit.issues)


def _render_debt(result: FullSuiteLogicAuditResult) -> str:
    lines = ["# PHYGN Debt Boundary Audit v4.4.1", "", f"- slot4_debt_open: `{result.debt_boundary_audit.slot4_debt_open}`", ""]
    lines.append(_render_issues(result.debt_boundary_audit.issues))
    return "\n".join(lines) + "\n"


def _render_metrics(result: FullSuiteLogicAuditResult) -> str:
    issues = result.metric_integrity_audit.issues
    return _render_issue_report("PHYGN Metric Integrity Audit v4.4.1", issues)


def _render_remediation(result: FullSuiteLogicAuditResult) -> str:
    lines = [
        "# PHYGN Remediation Plan v4.4.1",
        "",
        f"- can_continue_pipeline: `{result.remediation_plan.can_continue_pipeline}`",
        f"- gate_status: `{result.remediation_plan.gate_status}`",
        f"- remediation_item_count: `{len(result.remediation_plan.items)}`",
        "",
    ]
    for item in result.remediation_plan.items[:120]:
        lines.append(f"- `{item.remediation_id}`: issue=`{item.issue_id}`, severity=`{item.severity}`, gate=`{item.gate_effect}`")
    return "\n".join(lines) + "\n"


def _render_campaign(result: FullSuiteLogicAuditResult) -> str:
    return "\n".join([
        "# Campaign Report - PHYGN-FULL-SUITE-LOGIC-AUDIT-v4_4_1",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- blocker_count: `{result.blocker_count}`",
        f"- nonblocking_issue_count: `{result.nonblocking_issue_count}`",
        f"- can_continue_pipeline: `{result.remediation_plan.can_continue_pipeline}`",
        f"- gate_status: `{result.remediation_plan.gate_status}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"


def _render_issue_report(title: str, issues: list[AuditIssue]) -> str:
    return "\n".join([f"# {title}", "", f"- issue_count: `{len(issues)}`", "", _render_issues(issues)]) + "\n"


def _render_issues(issues: list[AuditIssue]) -> str:
    if not issues:
        return "No issues detected."
    lines = []
    for issue in issues[:120]:
        lines.extend([
            f"### `{issue.issue_id}`",
            "",
            f"- severity: `{issue.severity}`",
            f"- category: `{issue.category}`",
            f"- path: `{issue.path}`",
            f"- message: {issue.message}",
            f"- remediation: {issue.remediation}",
            "",
        ])
    return "\n".join(lines)


def _next_actions(result: FullSuiteLogicAuditResult) -> list[str]:
    if result.blocker_count:
        return ["Resolve BLOCKER audit issues before continuing to v4.5."]
    if result.nonblocking_issue_count:
        return ["Review nonblocking audit issues before using v4.5 outputs in claims."]
    return ["Proceed to the next gate while preserving source/y_true/PredictiveGain boundaries."]
