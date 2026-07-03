"""Markdown reports for v4.4 manual data extraction."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.manual_data_extraction.schemas import ManualDataExtractionCampaignResult


def write_manual_data_extraction_reports(result: ManualDataExtractionCampaignResult, reports_dir: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "y_true_manual_extraction"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "review_records": report_dir / "phi_gradient_manual_extraction_review_records_v4_4.md",
        "accepted_y_true": report_dir / "phi_gradient_manual_extraction_accepted_y_true_v4_4.md",
        "rejected": report_dir / "phi_gradient_manual_extraction_rejected_v4_4.md",
        "audit_trail": report_dir / "phi_gradient_manual_extraction_audit_trail_v4_4.md",
        "assembled_dataset": report_dir / "phi_gradient_assembled_y_true_dataset_v4_4.md",
        "quality_report": report_dir / "phi_gradient_dataset_quality_report_v4_4.md",
        "next_predictive_gain_inputs": report_dir / "phi_gradient_next_predictive_gain_inputs_v4_4.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-MANUAL-DATA-EXTRACTION-v4_4.md",
    }
    renderers = {
        "review_records": _render_reviews,
        "accepted_y_true": _render_accepted,
        "rejected": _render_rejected,
        "audit_trail": _render_audit,
        "assembled_dataset": _render_dataset,
        "quality_report": _render_quality,
        "next_predictive_gain_inputs": _render_next,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: ManualDataExtractionCampaignResult, reports_generated: list[str] | None = None) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Manual Data Extraction v4.4",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="manual_data_extraction",
        reports_generated=reports_generated or [],
        next_actions=gate.next_actions,
        discipline_note="No table/page/value/unit/hash, no y_true. No y_true threshold, no PredictiveGain.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_reviews(result: ManualDataExtractionCampaignResult) -> str:
    gate = result.gate_result
    lines = ["# PHI_GRADIENT Manual Extraction Review Records v4.4", "", f"- reviewed_count: `{gate.reviewed_count}`", ""]
    for record in gate.review_records[:40]:
        lines.extend([
            f"### `{record.review_id}`",
            "",
            f"- target_id: `{record.target_id}`",
            f"- source_id: `{record.source_id}`",
            f"- observable_class: `{record.observable_class}`",
            f"- decision: `{record.reviewer_decision}`",
            f"- qc_status: `{record.qc_status}`",
            f"- blockers: `{', '.join(record.blockers) if record.blockers else 'None'}`",
            "",
        ])
    return "\n".join(lines)


def _render_accepted(result: ManualDataExtractionCampaignResult) -> str:
    accepted = result.gate_result.accepted_y_true_records
    lines = ["# PHI_GRADIENT Accepted Manual y_true v4.4", "", f"- accepted_count: `{len(accepted)}`", ""]
    if not accepted:
        lines.append("No manual extraction record met the QC threshold for y_true.")
    for record in accepted:
        lines.append(f"- `{record.y_true_id}`: target=`{record.target_id}`, value=`{record.value}` `{record.unit}`")
    return "\n".join(lines) + "\n"


def _render_rejected(result: ManualDataExtractionCampaignResult) -> str:
    rejected = result.gate_result.rejected_records
    return "\n".join(["# PHI_GRADIENT Rejected Manual Extraction v4.4", "", f"- rejected_count: `{len(rejected)}`", "", *[f"- `{item.review_id}`: `{item.rejection_reason}`" for item in rejected[:80]]]) + "\n"


def _render_audit(result: ManualDataExtractionCampaignResult) -> str:
    audit = result.gate_result.audit_trail
    return "\n".join(["# PHI_GRADIENT Manual Extraction Audit Trail v4.4", "", f"- audit_event_count: `{len(audit)}`", "", *[f"- `{item.audit_id}`: `{item.decision}`, target=`{item.target_id}`" for item in audit[:80]]]) + "\n"


def _render_dataset(result: ManualDataExtractionCampaignResult) -> str:
    dataset = result.gate_result.assembled_dataset
    return "\n".join([
        "# PHI_GRADIENT Assembled y_true Dataset v4.4",
        "",
        f"- total_y_true_count: `{dataset.total_y_true_count}`",
        f"- new_y_true_count: `{dataset.new_y_true_count}`",
        f"- matched_prediction_count: `{dataset.matched_prediction_count}`",
        f"- ready_for_predictive_gain: `{dataset.ready_for_predictive_gain}`",
        f"- predictive_gain_status: `{dataset.predictive_gain_status}`",
        f"- slot4_debt_status: `{dataset.slot4_debt_status}`",
        f"- physical_claim_permission: `{dataset.physical_claim_permission}`",
    ]) + "\n"


def _render_quality(result: ManualDataExtractionCampaignResult) -> str:
    q = result.gate_result.quality_report
    return "\n".join([
        "# PHI_GRADIENT Dataset Quality Report v4.4",
        "",
        f"- manual_queue_count: `{q.manual_queue_count}`",
        f"- reviewed_count: `{q.reviewed_count}`",
        f"- accepted_count: `{q.accepted_count}`",
        f"- rejected_count: `{q.rejected_count}`",
        f"- rerouted_count: `{q.rerouted_count}`",
        f"- unit_issues: `{q.unit_issues}`",
        f"- location_issues: `{q.location_issues}`",
        f"- hash_issues: `{q.hash_issues}`",
        f"- ready_for_predictive_gain: `{q.ready_for_predictive_gain}`",
    ]) + "\n"


def _render_next(result: ManualDataExtractionCampaignResult) -> str:
    nxt = result.gate_result.next_predictive_gain_inputs
    return "\n".join([
        "# PHI_GRADIENT Next PredictiveGain Inputs v4.4",
        "",
        f"- ready_for_predictive_gain: `{nxt.ready_for_predictive_gain}`",
        f"- accepted_y_true_count: `{nxt.accepted_y_true_count}`",
        f"- matched_prediction_count: `{nxt.matched_prediction_count}`",
        f"- predictive_gain_status: `{nxt.predictive_gain_status}`",
        f"- recommended_next_phase: `{nxt.recommended_next_phase}`",
    ]) + "\n"


def _render_campaign(result: ManualDataExtractionCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-MANUAL-DATA-EXTRACTION-v4_4",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- manual_queue_count: `{gate.manual_queue_count}`",
        f"- reviewed_count: `{gate.reviewed_count}`",
        f"- accepted_y_true_count: `{gate.accepted_y_true_count}`",
        f"- rejected_count: `{gate.rejected_count}`",
        f"- rerouted_count: `{gate.rerouted_count}`",
        f"- matched_prediction_count: `{gate.matched_prediction_count}`",
        f"- ready_for_predictive_gain: `{gate.ready_for_predictive_gain}`",
        f"- predictive_gain_status: `{gate.predictive_gain_status}`",
        f"- slot4_debt_status: `{gate.slot4_debt_status}`",
        f"- physical_claim_permission: `{gate.physical_claim_permission}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
