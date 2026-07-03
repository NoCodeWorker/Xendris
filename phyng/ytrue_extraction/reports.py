"""Generate Markdown reports for v4.3 y_true extraction and dataset assembly."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.ytrue_extraction.schemas import ExtractionCampaignResult


def write_ytrue_reports(
    result: ExtractionCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    y_dir = root / "y_true"
    campaigns_dir = root / "campaigns"

    y_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "audit": y_dir / "phi_gradient_source_coverage_audit_v4_3.md",
        "candidates": y_dir / "phi_gradient_y_true_extraction_candidates_v4_3.md",
        "table_q": y_dir / "phi_gradient_manual_table_extraction_queue_v4_3.md",
        "fig_q": y_dir / "phi_gradient_figure_digitization_queue_v4_3.md",
        "pub_q": y_dir / "phi_gradient_public_dataset_lookup_queue_v4_3.md",
        "supp_q": y_dir / "phi_gradient_supplementary_lookup_queue_v4_3.md",
        "assembled": y_dir / "phi_gradient_assembled_y_true_dataset_v4_3.md",
        "blocked": y_dir / "phi_gradient_blocked_y_true_targets_v4_3.md",
        "quality": y_dir / "phi_gradient_dataset_quality_report_v4_3.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-REAL-YTRUE-EXTRACTION-v4_3.md",
    }

    renderers = {
        "audit": _render_audit,
        "candidates": _render_candidates,
        "table_q": lambda res: _render_queue(res.gate_result.manual_table_extraction_queue, "Manual Table Extraction Queue"),
        "fig_q": lambda res: _render_queue(res.gate_result.figure_digitization_queue, "Figure Digitization Queue"),
        "pub_q": lambda res: _render_queue(res.gate_result.public_dataset_lookup_queue, "Public Dataset Lookup Queue"),
        "supp_q": lambda res: _render_queue(res.gate_result.supplementary_lookup_queue, "Supplementary Lookup Queue"),
        "assembled": _render_assembled,
        "blocked": _render_blocked,
        "quality": _render_quality,
    }

    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")

    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map

    # Write campaign report
    paths["campaign"].write_text(
        _canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8"
    )

    return path_map


def _canonical(
    markdown: str,
    result: ExtractionCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    contract = build_report_contract(
        title="PHI_GRADIENT Real y_true Extraction & Assembly v4.3",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="observable_dataset",
        reports_generated=reports_generated or [],
        next_actions=[
            "v4.4 — PredictiveGain Smoke Test & Error Comparison"
            if result.gate_result.assembled_y_true_dataset.ready_for_predictive_gain
            else "v4.4 — Manual Data Extraction Sprint",
            "v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review",
        ],
        discipline_note="No provenance, no y_true. No y_true, no PredictiveGain.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_audit(result: ExtractionCampaignResult) -> str:
    gate = result.gate_result
    audit = gate.source_coverage_audit
    lines = [
        "# PHI_GRADIENT Source Coverage Audit v4.3",
        "",
        f"- total_targets_audited: `{len(audit)}`",
        "",
        "## Audit Log",
        "",
    ]
    for r in audit[:30]:
        lines.extend([
            f"### Target: `{r.target_id}` (Benchmark: `{r.benchmark_id}`)",
            "",
            f"- source: `{r.source_id}`",
            f"- hash_present: `{r.source_hash_present}`",
            f"- local_pdf_present: `{r.local_pdf_present}`",
            f"- page_ref_present: `{r.page_reference_present}`",
            f"- table_ref_present: `{r.table_reference_present}`",
            f"- figure_ref_present: `{r.figure_reference_present}`",
            f"- status: **{r.source_coverage_status}**",
            f"- next_action: {r.next_action}",
            f"- blockers: `{', '.join(r.blockers) if r.blockers else 'None'}`",
            "",
        ])
    return "\n".join(lines)


def _render_candidates(result: ExtractionCampaignResult) -> str:
    gate = result.gate_result
    candidates = gate.extraction_candidates
    lines = [
        "# PHI_GRADIENT y_true Extraction Candidates v4.3",
        "",
        f"- candidate_count: `{len(candidates)}`",
        "",
    ]
    for c in candidates[:30]:
        lines.extend([
            f"### Candidate: `{c.candidate_id}` (Target: `{c.target_id}`)",
            "",
            f"- observable_class: `{c.observable_class}`",
            f"- value_text: *\"{c.candidate_value_text}\"*",
            f"- parsed_numeric: `{c.numeric_value or 'None'}`",
            f"- unit: `{c.unit or 'None'}`",
            f"- provenance_status: `{c.provenance_status}`",
            f"- qc_status: **{c.qc_status}**",
            f"- can_enter_dataset: `{c.can_enter_dataset}`",
            f"- blockers: `{', '.join(c.blockers) if c.blockers else 'None'}`",
            "",
        ])
    return "\n".join(lines)


def _render_queue(queue: list, title: str) -> str:
    lines = [
        f"# PHI_GRADIENT {title} v4.3",
        "",
        f"- queue_item_count: `{len(queue)}`",
        "",
    ]
    for item in queue[:30]:
        lines.extend([
            f"### Actionable Target: `{item.target_id}`",
            "",
            f"- source: `{item.source_id}`",
            f"- class: `{item.observable_class}`",
            f"- expected_measurement: {item.expected_measurement}",
            f"- location_hint: *\"{item.source_location_hint}\"*",
            f"- required_action: **{item.required_action}**",
            f"- priority: **{item.priority}**",
            f"- blocking_reason: {item.blocking_reason}",
            "",
        ])
    return "\n".join(lines)


def _render_assembled(result: ExtractionCampaignResult) -> str:
    gate = result.gate_result
    ds = gate.assembled_y_true_dataset
    lines = [
        "# PHI_GRADIENT Assembled y_true Dataset v4.3",
        "",
        f"- dataset_id: `{ds.dataset_id}`",
        f"- created_at: `{ds.created_at}`",
        f"- ready_for_predictive_gain: `{ds.ready_for_predictive_gain}`",
        f"- y_true_record_count: `{ds.y_true_record_count}`",
        f"- slot4_debt_status: `{ds.slot4_debt_status}`",
        "",
        "## Assembled Records",
        "",
    ]
    if not ds.records:
        lines.append("*No records met the QC criteria for dataset entry. Dataset is empty.*")
    else:
        for r in ds.records:
            lines.extend([
                f"### Record: `{r.y_true_id}` (Target: `{r.target_id}`)",
                "",
                f"- class: `{r.observable_class}`",
                f"- value: `{r.value}` {r.unit or ''}",
                f"- uncertainty: `{r.uncertainty or 'None'}`",
                f"- source: `{r.source_id}`",
                f"- source_hash: `{r.source_hash}`",
                f"- location: `{r.source_location_type}` = `{r.source_location_value}`",
                f"- matched_predictions: `{', '.join(r.matched_prediction_ids) if r.matched_prediction_ids else 'None'}`",
                "",
            ])
    return "\n".join(lines)


def _render_blocked(result: ExtractionCampaignResult) -> str:
    gate = result.gate_result
    blocked = gate.blocked_y_true_targets
    lines = [
        "# PHI_GRADIENT Blocked y_true Targets v4.3",
        "",
        f"- blocked_target_count: `{len(blocked)}`",
        "",
    ]
    for b in blocked[:30]:
        lines.extend([
            f"### Blocked Target: `{b.target_id}`",
            "",
            f"- benchmark: `{b.benchmark_id}`",
            f"- source: `{b.source_id}`",
            f"- class: `{b.observable_class}`",
            f"- reason: **{b.blocked_reason}**",
            f"- required_action: {b.required_action}",
            f"- priority: **{b.priority}**",
            f"- can_be_unblocked: `{b.can_be_unblocked}`",
            "",
        ])
    return "\n".join(lines)


def _render_quality(result: ExtractionCampaignResult) -> str:
    gate = result.gate_result
    q = gate.dataset_quality_report
    return "\n".join([
        "# PHI_GRADIENT Dataset Quality Report v4.3",
        "",
        f"- target_count: `{q.target_count}`",
        f"- candidate_count: `{q.candidate_count}`",
        f"- accepted_y_true_count: `{q.accepted_y_true_count}`",
        f"- blocked_count: `{q.blocked_count}`",
        f"- qc_pass_count: `{q.qc_pass_count}`",
        f"- qc_fail_count: `{q.qc_fail_count}`",
        f"- unit_normalization_issues: `{q.unit_normalization_issues}`",
        f"- source_coverage_issues: `{q.source_coverage_issues}`",
        f"- prediction_matching_issues: `{q.prediction_matching_issues}`",
        f"- readiness_status: **{q.readiness_status}**",
        "",
        "## Recommendations",
        "",
        *[f"- {rec}" for rec in q.recommendations],
    ]) + "\n"


def _render_campaign(result: ExtractionCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-REAL-YTRUE-EXTRACTION-v4_3",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- total_targets: `{len(gate.source_coverage_audit)}`",
        f"- accepted_y_true_records: `{gate.assembled_y_true_dataset.y_true_record_count}`",
        f"- ready_for_predictive_gain: `{gate.assembled_y_true_dataset.ready_for_predictive_gain}`",
        f"- PredictiveGain status: `UNDEFINED`",
        f"- SLOT_4 debt status: `{gate.assembled_y_true_dataset.slot4_debt_status}`",
        f"- physical_claim_permission: `{gate.assembled_y_true_dataset.physical_claim_permission}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
