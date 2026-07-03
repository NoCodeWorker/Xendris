"""Reports for v4.4.2 audit remediation."""

from __future__ import annotations

from pathlib import Path

from phyng.audit_remediation.schemas import AuditRemediationCampaignResult
from phyng.core.report_contract import append_canonical_status_section, build_report_contract


def write_audit_remediation_reports(result: AuditRemediationCampaignResult, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    report_dir = root / "audits" / "remediation"
    campaign_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "status_mapping": report_dir / "phygn_status_mapping_remediation_v4_4_2.md",
        "quarantine": report_dir / "phygn_status_quarantine_register_v4_4_2.md",
        "test_plan": report_dir / "phygn_test_hardening_plan_v4_4_2.md",
        "test_results": report_dir / "phygn_test_hardening_results_v4_4_2.md",
        "claim": report_dir / "phygn_claim_leakage_remediation_v4_4_2.md",
        "metric": report_dir / "phygn_metric_integrity_remediation_v4_4_2.md",
        "residual": report_dir / "phygn_accepted_residual_audit_debt_v4_4_2.md",
        "delta": report_dir / "phygn_post_remediation_audit_delta_v4_4_2.md",
        "gate": report_dir / "phygn_v4_4_2_continuation_gate.md",
        "campaign": campaign_dir / "PHYGN-AUDIT-REMEDIATION-v4_4_2.md",
    }
    renderers = {
        "status_mapping": _render_status_mapping,
        "quarantine": _render_quarantine,
        "test_plan": _render_test_plan,
        "test_results": _render_test_results,
        "claim": _render_claim,
        "metric": _render_metric,
        "residual": _render_residual,
        "delta": _render_delta,
        "gate": _render_gate,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: AuditRemediationCampaignResult, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="PHYGN Audit Remediation v4.4.2",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="audit_remediation",
        reports_generated=reports_generated or [],
        next_actions=result.continuation_gate.required_before_v4_5 if result.continuation_gate else [],
        discipline_note="Remediation is permission infrastructure. It does not create y_true, PredictiveGain, SLOT_4 resolution, or physical validation.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_status_mapping(result: AuditRemediationCampaignResult) -> str:
    lines = ["# PHYGN Status Mapping Remediation v4.4.2", "", f"- record_count: `{len(result.status_mapping_records)}`", f"- quarantined_count: `{len(result.quarantine_records)}`", ""]
    for record in result.status_mapping_records[:120]:
        lines.append(f"- `{record.status}`: action=`{record.proposed_mapping_action}`, permission=`{record.canonical_permission}`, remediation=`{record.remediation_status}`")
    return "\n".join(lines) + "\n"


def _render_quarantine(result: AuditRemediationCampaignResult) -> str:
    lines = ["# PHYGN Status Quarantine Register v4.4.2", "", f"- quarantine_count: `{len(result.quarantine_records)}`", ""]
    for record in result.quarantine_records[:120]:
        lines.append(f"- `{record.status}`: may_gate_claims=`{record.may_gate_claims}`, may_unlock_next_phase=`{record.may_unlock_next_phase}`")
    return "\n".join(lines) + "\n"


def _render_test_plan(result: AuditRemediationCampaignResult) -> str:
    lines = ["# PHYGN Test Hardening Plan v4.4.2", "", f"- plan_item_count: `{len(result.test_hardening_plan)}`", ""]
    for item in result.test_hardening_plan[:120]:
        lines.append(f"- `{item.test_file}` / `{item.test_name}`: fixture=`{item.required_negative_fixture}`, priority=`{item.priority}`")
    return "\n".join(lines) + "\n"


def _render_test_results(result: AuditRemediationCampaignResult) -> str:
    r = result.test_hardening_results
    return "\n".join([
        "# PHYGN Test Hardening Results v4.4.2",
        "",
        f"- initial_status_only_count: `{r.initial_status_only_count}`",
        f"- hardened_test_count: `{r.hardened_test_count}`",
        f"- remaining_status_only_count: `{r.remaining_status_only_count}`",
        f"- negative_fixture_count_added: `{r.negative_fixture_count_added}`",
        f"- debt_bypass_fixture_count_added: `{r.debt_bypass_fixture_count_added}`",
        f"- metric_misuse_fixture_count_added: `{r.metric_misuse_fixture_count_added}`",
    ]) + "\n"


def _render_claim(result: AuditRemediationCampaignResult) -> str:
    lines = ["# PHYGN Claim Leakage Remediation v4.4.2", "", f"- record_count: `{len(result.claim_remediation_records)}`", ""]
    for record in result.claim_remediation_records[:80]:
        lines.append(f"- `{record.leakage_id}`: action=`{record.remediation_action}`, final=`{record.final_status}`")
    if not result.claim_remediation_records:
        lines.append("No open claim leakage records required rewriting.")
    return "\n".join(lines) + "\n"


def _render_metric(result: AuditRemediationCampaignResult) -> str:
    lines = ["# PHYGN Metric Integrity Remediation v4.4.2", "", f"- record_count: `{len(result.metric_remediation_records)}`", ""]
    for record in result.metric_remediation_records:
        lines.append(f"- `{record.metric_name}`: required=`{record.required_label}`, forbidden=`{record.forbidden_label}`")
    return "\n".join(lines) + "\n"


def _render_residual(result: AuditRemediationCampaignResult) -> str:
    lines = ["# PHYGN Accepted Residual Audit Debt v4.4.2", "", f"- debt_count: `{len(result.residual_debt)}`", ""]
    for debt in result.residual_debt:
        lines.append(f"- `{debt.debt_id}`: category=`{debt.category}`, next_review=`{debt.next_review_phase}`, may_continue=`{debt.may_continue_pipeline}`")
    return "\n".join(lines) + "\n"


def _render_delta(result: AuditRemediationCampaignResult) -> str:
    d = result.delta
    if d is None:
        return "# PHYGN Post-Remediation Audit Delta v4.4.2\n\nNo delta generated.\n"
    return "\n".join([
        "# PHYGN Post-Remediation Audit Delta v4.4.2",
        "",
        f"- initial_nonblocking_issue_count: `{d.initial_nonblocking_issue_count}`",
        f"- remaining_nonblocking_issue_count: `{d.remaining_nonblocking_issue_count}`",
        f"- initial_unmapped_status_count: `{d.initial_unmapped_status_count}`",
        f"- remaining_unmapped_status_count: `{d.remaining_unmapped_status_count}`",
        f"- critical_unmapped_status_count: `{d.critical_unmapped_status_count}`",
        f"- initial_status_only_test_issue_count: `{d.initial_status_only_test_issue_count}`",
        f"- remaining_status_only_test_issue_count: `{d.remaining_status_only_test_issue_count}`",
        f"- continuation_gate: `{d.continuation_gate}`",
    ]) + "\n"


def _render_gate(result: AuditRemediationCampaignResult) -> str:
    gate = result.continuation_gate
    if gate is None:
        return "# PHYGN v4.4.2 Continuation Gate\n\nNo gate generated.\n"
    return "\n".join([
        "# PHYGN v4.4.2 Continuation Gate",
        "",
        f"- gate_status: `{gate.gate_status}`",
        f"- can_continue_pipeline: `{gate.can_continue_pipeline}`",
        f"- recommended_next_phase: `{gate.recommended_next_phase}`",
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in gate.blocked_claims],
    ]) + "\n"


def _render_campaign(result: AuditRemediationCampaignResult) -> str:
    gate = result.continuation_gate
    return "\n".join([
        "# Campaign Report - PHYGN-AUDIT-REMEDIATION-v4_4_2",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- inputs_loaded: `{result.inputs_loaded}`",
        f"- status_mapping_records: `{len(result.status_mapping_records)}`",
        f"- quarantine_records: `{len(result.quarantine_records)}`",
        f"- residual_debt_count: `{len(result.residual_debt)}`",
        f"- continuation_gate: `{gate.gate_status if gate else 'None'}`",
        f"- can_continue_pipeline: `{gate.can_continue_pipeline if gate else False}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
