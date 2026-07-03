"""Campaign orchestration for v4.4.2 audit remediation."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.audit_remediation.claim_remediation import build_claim_remediation_records
from phyng.audit_remediation.continuation_gate import compute_continuation_gate
from phyng.audit_remediation.delta import build_post_remediation_delta
from phyng.audit_remediation.loader import load_audit_remediation_inputs
from phyng.audit_remediation.metric_remediation import build_metric_remediation_records
from phyng.audit_remediation.reports import write_audit_remediation_reports
from phyng.audit_remediation.residual_debt import build_residual_debt
from phyng.audit_remediation.schemas import AuditRemediationCampaignResult, TestHardeningResults
from phyng.audit_remediation.status_remediation import classify_unmapped_statuses, critical_unmapped_after_remediation
from phyng.audit_remediation.test_hardening import build_test_hardening_plan, build_test_hardening_results
from phyng.core.compatibility import normalize_status


def run_phygn_audit_remediation_campaign(root: str | Path = ".") -> AuditRemediationCampaignResult:
    repo_root = Path(root)
    inputs = load_audit_remediation_inputs(repo_root)
    if inputs.missing_files:
        status = "PHYGN_AUDIT_REMEDIATION_BLOCKED_MISSING_AUDIT"
        gate = compute_continuation_gate(1, 0, 0, [])
        result = AuditRemediationCampaignResult(
            status=status,
            canonical_status=normalize_status(status, domain="audit_remediation"),
            inputs_loaded=False,
            test_hardening_results=TestHardeningResults(),
            continuation_gate=gate,
        )
        result.output_paths = write_remediation_outputs(repo_root, result)
        result.report_paths = write_audit_remediation_reports(result, repo_root / "reports")
        write_result_doc(repo_root, result)
        return result

    status_records, quarantine = classify_unmapped_statuses(inputs.status_permission)
    test_plan = build_test_hardening_plan(inputs.test_logic)
    test_results = build_test_hardening_results(test_plan)
    claim_records = build_claim_remediation_records(inputs.claim_leakage)
    metric_records = build_metric_remediation_records(inputs.metric_integrity)
    residual = build_residual_debt(status_records, test_plan)
    critical_after = critical_unmapped_after_remediation(status_records)
    open_claim_blockers = sum(1 for record in claim_records if record.blocks_next_gate)
    blocker_count = int(inputs.full_suite.get("blocker_count", 0))
    gate = compute_continuation_gate(blocker_count, critical_after, open_claim_blockers, residual)
    delta = build_post_remediation_delta(
        full_suite_payload=inputs.full_suite,
        initial_unmapped=len(inputs.status_permission.get("unmapped_statuses", [])),
        initial_status_only=len(inputs.test_logic.get("issues", [])),
        critical_unmapped_after=critical_after,
        remaining_status_only=test_results.remaining_status_only_count,
        claims_rewritten=sum(1 for record in claim_records if record.remediation_action == "REWRITE_CLAIM"),
        metrics_relabelled=len(metric_records),
        debt_items_accepted=len(residual),
        continuation_gate=gate.gate_status,
    )
    status = _status(gate.gate_status, residual)
    result = AuditRemediationCampaignResult(
        status=status,
        canonical_status=normalize_status(status, domain="audit_remediation"),
        inputs_loaded=True,
        status_mapping_records=status_records,
        quarantine_records=quarantine,
        test_hardening_plan=test_plan,
        test_hardening_results=test_results,
        claim_remediation_records=claim_records,
        metric_remediation_records=metric_records,
        residual_debt=residual,
        delta=delta,
        continuation_gate=gate,
    )
    result.output_paths = write_remediation_outputs(repo_root, result)
    result.report_paths = write_audit_remediation_reports(result, repo_root / "reports")
    write_result_doc(repo_root, result)
    return result


def write_remediation_outputs(root: Path, result: AuditRemediationCampaignResult) -> dict[str, str]:
    output_dir = root / "data" / "audits" / "remediation"
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "status_mapping": output_dir / "phygn_status_mapping_remediation_v4_4_2.json",
        "quarantine": output_dir / "phygn_status_quarantine_register_v4_4_2.json",
        "test_plan": output_dir / "phygn_test_hardening_plan_v4_4_2.json",
        "test_results": output_dir / "phygn_test_hardening_results_v4_4_2.json",
        "claim": output_dir / "phygn_claim_leakage_remediation_v4_4_2.json",
        "metric": output_dir / "phygn_metric_integrity_remediation_v4_4_2.json",
        "residual": output_dir / "phygn_accepted_residual_audit_debt_v4_4_2.json",
        "delta": output_dir / "phygn_post_remediation_audit_delta_v4_4_2.json",
        "gate": output_dir / "phygn_v4_4_2_continuation_gate.json",
    }
    payloads = {
        "status_mapping": result.status_mapping_records,
        "quarantine": result.quarantine_records,
        "test_plan": result.test_hardening_plan,
        "test_results": result.test_hardening_results,
        "claim": result.claim_remediation_records,
        "metric": result.metric_remediation_records,
        "residual": result.residual_debt,
        "delta": result.delta,
        "gate": result.continuation_gate,
    }
    for key, payload in payloads.items():
        dumped = [item.model_dump() for item in payload] if isinstance(payload, list) else (payload.model_dump() if payload else {})
        paths[key].write_text(json.dumps(dumped, indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}


def write_result_doc(root: Path, result: AuditRemediationCampaignResult) -> None:
    docs_dir = root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    gate = result.continuation_gate
    lines = [
        "# Phygn v4.4.2 - Audit Remediation Results",
        "",
        "Date: 2026-07-01",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/290_PHYGN_CODEX_V4_4_2_AUDIT_REMEDIATION_PROMPT.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{result.status}`",
        f"Continuation gate: `{gate.gate_status if gate else 'None'}`",
        f"Can continue pipeline: `{gate.can_continue_pipeline if gate else False}`",
        "",
        "## Remediation Metrics",
        "",
        f"- status_mapping_records: `{len(result.status_mapping_records)}`",
        f"- quarantine_records: `{len(result.quarantine_records)}`",
        f"- status_only_tests_classified: `{len(result.test_hardening_plan)}`",
        f"- residual_debt_count: `{len(result.residual_debt)}`",
        "",
        "No y_true was created. No PredictiveGain was created. SLOT_4 debt remains open.",
    ]
    (docs_dir / "291_PHYGN_V4_4_2_AUDIT_REMEDIATION_RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _status(gate_status: str, residual: list) -> str:
    if gate_status.startswith("RESUME_BLOCKED_PENDING_STATUS"):
        return "PHYGN_AUDIT_REMEDIATION_BLOCKED_UNRESOLVED_PERMISSIONS"
    if gate_status.startswith("RESUME_BLOCKED"):
        return "PHYGN_AUDIT_REMEDIATION_REQUIRES_MORE_HARDENING"
    if gate_status == "RESUME_ALLOWED":
        return "PHYGN_AUDIT_REMEDIATION_READY_TO_RESUME_PIPELINE"
    if residual:
        return "PHYGN_AUDIT_REMEDIATION_PARTIAL"
    return "PHYGN_AUDIT_REMEDIATION_COMPLETED"
