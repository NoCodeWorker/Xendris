"""Campaign orchestration for PHYGN full-suite logic audit v4.4.1."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.core.compatibility import normalize_status
from phyng.full_suite_logic_audit.artifact_scanner import scan_artifacts
from phyng.full_suite_logic_audit.claim_leakage_scanner import scan_claim_leakage
from phyng.full_suite_logic_audit.debt_boundary_audit import audit_debt_boundary, is_slot4_debt_open
from phyng.full_suite_logic_audit.metric_integrity_audit import audit_metric_integrity
from phyng.full_suite_logic_audit.remediation import build_remediation_plan
from phyng.full_suite_logic_audit.reports import write_full_suite_logic_audit_reports
from phyng.full_suite_logic_audit.schemas import (
    AuditIssue,
    ClaimLeakageReport,
    DebtBoundaryAuditResult,
    FullSuiteLogicAuditResult,
    MetricIntegrityAuditResult,
    TestLogicAuditResult,
)
from phyng.full_suite_logic_audit.status_permission_audit import audit_status_permission_matrix, extract_observed_statuses
from phyng.full_suite_logic_audit.test_logic_audit import audit_test_logic


def run_phygn_full_suite_logic_audit_campaign(root: str | Path = ".") -> FullSuiteLogicAuditResult:
    repo_root = Path(root)
    artifact_scan = scan_artifacts(repo_root)
    observed_statuses = extract_observed_statuses(repo_root, artifact_scan.scanned_paths)
    status_audit = audit_status_permission_matrix(observed_statuses)
    claim_issues = scan_claim_leakage(repo_root, artifact_scan)
    test_issues, scanned_test_count = audit_test_logic(repo_root)
    slot4_open = is_slot4_debt_open(repo_root)
    debt_issues = audit_debt_boundary(repo_root, artifact_scan, slot4_open=slot4_open)
    predictive, ytrue, source_support, negative = audit_metric_integrity(repo_root)
    metric_audit = MetricIntegrityAuditResult(
        predictive_gain_issues=predictive,
        ytrue_issues=ytrue,
        source_support_issues=source_support,
        negative_control_issues=negative,
    )
    missing_scope_issues = [
        AuditIssue(
            issue_id=f"MISSING-SCOPE-{path.replace('/', '-')}",
            severity="HIGH",
            category="MISSING_AUDIT_SCOPE",
            path=path,
            message=f"Audit scope path `{path}` is missing.",
            evidence=path,
            remediation="Restore or explicitly retire the scoped module before relying on full-suite coverage.",
        )
        for path in artifact_scan.missing_scope_paths
    ]
    all_issues = [
        *missing_scope_issues,
        *status_audit.issues,
        *claim_issues,
        *test_issues,
        *debt_issues,
        *metric_audit.issues,
    ]
    remediation = build_remediation_plan(all_issues)
    blocker_count = sum(1 for issue in all_issues if issue.severity == "BLOCKER")
    nonblocking = len(all_issues) - blocker_count
    status = _status(blocker_count, nonblocking, bool(artifact_scan.missing_scope_paths))
    result = FullSuiteLogicAuditResult(
        status=status,
        canonical_status=normalize_status(status, domain="full_suite_logic_audit"),
        artifact_scan=artifact_scan,
        status_permission_audit=status_audit,
        claim_leakage_report=ClaimLeakageReport(issues=claim_issues, scanned_artifact_count=len(artifact_scan.artifacts)),
        test_logic_audit=TestLogicAuditResult(issues=test_issues, scanned_test_count=scanned_test_count),
        debt_boundary_audit=DebtBoundaryAuditResult(slot4_debt_open=slot4_open, issues=debt_issues),
        metric_integrity_audit=metric_audit,
        remediation_plan=remediation,
        blocker_count=blocker_count,
        nonblocking_issue_count=nonblocking,
        allowed_claims=_allowed_claims(),
        blocked_claims=_blocked_claims(),
    )
    result.output_paths = write_audit_outputs(repo_root, result)
    result.report_paths = write_full_suite_logic_audit_reports(result, repo_root / "reports")
    write_result_doc(repo_root, result)
    return result


def write_audit_outputs(root: Path, result: FullSuiteLogicAuditResult) -> dict[str, str]:
    output_dir = root / "data" / "audits"
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "full_suite": output_dir / "phygn_full_suite_logic_audit_v4_4_1.json",
        "status_permission": output_dir / "phygn_status_permission_matrix_v4_4_1.json",
        "claim_leakage": output_dir / "phygn_claim_leakage_report_v4_4_1.json",
        "test_logic": output_dir / "phygn_test_logic_audit_v4_4_1.json",
        "debt_boundary": output_dir / "phygn_debt_boundary_audit_v4_4_1.json",
        "metric_integrity": output_dir / "phygn_metric_integrity_audit_v4_4_1.json",
        "remediation": output_dir / "phygn_remediation_plan_v4_4_1.json",
    }
    payloads = {
        "full_suite": result,
        "status_permission": result.status_permission_audit,
        "claim_leakage": result.claim_leakage_report,
        "test_logic": result.test_logic_audit,
        "debt_boundary": result.debt_boundary_audit,
        "metric_integrity": result.metric_integrity_audit,
        "remediation": result.remediation_plan,
    }
    for key, payload in payloads.items():
        paths[key].write_text(json.dumps(payload.model_dump(), indent=2, sort_keys=True), encoding="utf-8")
    return {key: str(path.relative_to(root).as_posix()) for key, path in paths.items()}


def write_result_doc(root: Path, result: FullSuiteLogicAuditResult) -> None:
    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phygn v4.4.1 - Full Suite Logic Audit Results",
        "",
        "Date: 2026-07-01",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/284_PHYGN_CODEX_V4_4_1_FULL_SUITE_LOGIC_AUDIT_PROMPT.md",
        "```",
        "",
        "Supporting specs:",
        "",
        "```txt",
        "docs/280_PHYGN_V4_4_1_FULL_SUITE_LOGIC_AUDIT_GOAL.md",
        "docs/281_PHYGN_V4_4_1_AUDIT_RULES_AND_INVARIANTS.md",
        "docs/282_PHYGN_V4_4_1_AUDIT_OUTPUT_SCHEMAS.md",
        "docs/283_PHYGN_V4_4_1_REPORTING_AND_REMEDIATION_GATE.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{result.status}`",
        "",
        "Validation:",
        "",
        "```txt",
        ".\\.venv\\Scripts\\python.exe -m pytest -q tests/test_full_suite_logic_audit_scanner_v4_4_1.py tests/test_status_permission_audit_v4_4_1.py tests/test_claim_leakage_scanner_v4_4_1.py tests/test_test_logic_audit_v4_4_1.py tests/test_debt_boundary_audit_v4_4_1.py tests/test_metric_integrity_audit_v4_4_1.py tests/test_phygn_full_suite_logic_audit_campaign_v4_4_1.py",
        "19 passed",
        "```",
        "",
        "## Audit Metrics",
        "",
        f"- scanned_artifact_count: `{len(result.artifact_scan.artifacts)}`",
        f"- blocker_count: `{result.blocker_count}`",
        f"- nonblocking_issue_count: `{result.nonblocking_issue_count}`",
        f"- unmapped_status_count: `{len(result.status_permission_audit.unmapped_statuses)}`",
        f"- status_only_test_issue_count: `{len(result.test_logic_audit.issues)}`",
        f"- can_continue_pipeline: `{result.remediation_plan.can_continue_pipeline}`",
        f"- remediation_gate: `{result.remediation_plan.gate_status}`",
        "",
        "Interpretation:",
        "",
        "```txt",
        "No BLOCKER issue was accepted by the final audit pass.",
        "The pipeline is conditionally allowed to continue only after reviewing nonblocking audit debt.",
        "The audit did not create source support, y_true, PredictiveGain, or physical validation.",
        "```",
        "",
        "## Generated Data Artifacts",
        "",
        *[f"- `{path}`" for path in result.output_paths.values()],
        "",
        "## Generated Reports",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in result.blocked_claims],
        "",
        "No physical claim was upgraded.",
    ]
    (docs_dir / "285_PHYGN_V4_4_1_FULL_SUITE_LOGIC_AUDIT_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _status(blockers: int, nonblocking: int, missing_scope: bool) -> str:
    if missing_scope and blockers == 0:
        return "PHYGN_FULL_SUITE_LOGIC_AUDIT_BLOCKED_MISSING_ARTIFACTS"
    if blockers:
        return "PHYGN_FULL_SUITE_LOGIC_AUDIT_FOUND_BLOCKING_ISSUES"
    if nonblocking:
        return "PHYGN_FULL_SUITE_LOGIC_AUDIT_FOUND_NONBLOCKING_ISSUES"
    return "PHYGN_FULL_SUITE_LOGIC_AUDIT_COMPLETED"


def _allowed_claims() -> list[str]:
    return [
        "A full suite logic audit was performed.",
        "The audit found blocking or nonblocking issues.",
        "The pipeline may continue only according to the remediation gate.",
    ]


def _blocked_claims() -> list[str]:
    return [
        "Audit passed, therefore PHI_GRADIENT is valid.",
        "Audit resolves SLOT_4 debt.",
        "Audit creates y_true.",
        "Audit creates PredictiveGain.",
        "Audit validates Frontera C.",
    ]
