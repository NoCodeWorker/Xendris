"""Generate Markdown reports for v4.2 observable dataset and y_true plan."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.observable_dataset.schemas import ObservableYTrueCampaignResult


def write_observable_ytrue_reports(
    result: ObservableYTrueCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    obs_dir = root / "observables"
    campaigns_dir = root / "campaigns"

    obs_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "schema": obs_dir / "phi_gradient_observable_schema_v4_2.md",
        "targets": obs_dir / "phi_gradient_normalized_observable_targets_v4_2.md",
        "plan": obs_dir / "phi_gradient_y_true_acquisition_plan_v4_2.md",
        "registry": obs_dir / "phi_gradient_dataset_source_registry_v4_2.md",
        "readiness": obs_dir / "phi_gradient_measurement_readiness_matrix_v4_2.md",
        "qc": obs_dir / "phi_gradient_quality_control_rules_v4_2.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-OBSERVABLE-DATASET-YTRUE-PLAN-v4_2.md",
    }

    renderers = {
        "schema": _render_schema,
        "targets": _render_targets,
        "plan": _render_plan,
        "registry": _render_registry,
        "readiness": _render_readiness,
        "qc": _render_qc,
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
    result: ObservableYTrueCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    contract = build_report_contract(
        title="PHI_GRADIENT Observable Dataset Normalization & y_true Plan v4.2",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="observable_dataset",
        reports_generated=reports_generated or [],
        next_actions=[
            "v4.3 — Real y_true Extraction & Dataset Assembly",
            "v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review",
        ],
        discipline_note="No y_true, no PredictiveGain.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_schema(result: ObservableYTrueCampaignResult) -> str:
    gate = result.gate_result
    records = gate.schema_records
    lines = [
        "# PHI_GRADIENT Observable Schema v4.2",
        "",
        f"- observable_class_count: `{len(records)}`",
        "",
    ]
    for r in records:
        lines.extend([
            f"## Class: `{r.observable_class}`",
            "",
            f"- canonical_name: **{r.canonical_name}**",
            f"- allowed_units: `{', '.join(r.allowed_units)}`",
            f"- expected_data_type: `{r.expected_data_type}`",
            f"- valid_range: {r.valid_range_description}",
            f"- source_slots: `{', '.join(r.source_slots)}`",
            f"- measurement_requirement: {r.measurement_requirement}",
            f"- y_true_definition: {r.y_true_definition}",
            "",
        ])
    return "\n".join(lines)


def _render_targets(result: ObservableYTrueCampaignResult) -> str:
    gate = result.gate_result
    targets = gate.normalized_targets
    lines = [
        "# PHI_GRADIENT Normalized Observable Targets v4.2",
        "",
        f"- normalized_target_count: `{len(targets)}`",
        "",
    ]
    for t in targets[:40]:
        lines.extend([
            f"### Target: `{t.target_id}` (Row: `{t.benchmark_id}`)",
            "",
            f"- source: `{t.source_id}`",
            f"- extract: `{t.extract_id}`",
            f"- observable_class: `{t.observable_class}`",
            f"- normalized_variable: `{t.normalized_variable_name}`",
            f"- unit: `{t.unit or 'None'}`",
            f"- expected_dtype: `{t.expected_dtype}`",
            f"- y_true_required: `{t.y_true_required}`",
            f"- y_true_status: `{t.y_true_status}`",
            f"- slot4_debt_status: `{t.slot4_debt_status}`",
            f"- predictive_gain_allowed: `{t.predictive_gain_allowed}`",
            f"- source text: *\"{t.source_observable_text}\"*",
            "",
        ])
    return "\n".join(lines)


def _render_plan(result: ObservableYTrueCampaignResult) -> str:
    gate = result.gate_result
    plan = gate.y_true_acquisition_plan
    lines = [
        "# PHI_GRADIENT y_true Acquisition Plan v4.2",
        "",
        f"- acquisition_item_count: `{len(plan)}`",
        "",
    ]
    for p in plan[:40]:
        lines.extend([
            f"### Item: `{p.acquisition_id}` (Target: `{p.target_id}`)",
            "",
            f"- class: `{p.observable_class}`",
            f"- status: `{p.y_true_status}`",
            f"- priority: **{p.priority}**",
            f"- acquisition_method: `{p.acquisition_method}`",
            f"- required_measurement: {p.required_measurement}",
            f"- candidate_sources: `{', '.join(p.candidate_data_sources)}`",
            f"- manual_extraction: `{p.manual_extraction_required}`",
            f"- experimental_required: `{p.experimental_required}`",
            f"- expected_unit: `{p.expected_unit or 'None'}`",
            f"- quality_requirements: `{', '.join(p.quality_requirements)}`",
            f"- blockers: `{', '.join(p.blockers) if p.blockers else 'None'}`",
            "",
        ])
    return "\n".join(lines)


def _render_registry(result: ObservableYTrueCampaignResult) -> str:
    gate = result.gate_result
    registry = gate.source_registry
    lines = [
        "# PHI_GRADIENT Dataset Source Registry v4.2",
        "",
        f"- registered_sources_count: `{len(registry)}`",
        "",
    ]
    for r in registry:
        lines.extend([
            f"### Dataset Source: `{r.dataset_source_id}`",
            "",
            f"- related_source_id: `{r.related_source_id}`",
            f"- type: `{r.source_type}`",
            f"- access_status: `{r.access_status}`",
            f"- expected_observables: `{', '.join(r.expected_observables)}`",
            f"- acquisition_method: `{r.acquisition_method}`",
            f"- requires_manual_review: `{r.requires_manual_review}`",
            "",
        ])
    return "\n".join(lines)


def _render_readiness(result: ObservableYTrueCampaignResult) -> str:
    gate = result.gate_result
    readiness = gate.readiness_matrix
    lines = [
        "# PHI_GRADIENT Measurement Readiness Matrix v4.2",
        "",
        "## Readiness Table",
        "",
        "| Observable Class | Targets | y_true Available | Public Data Acquirable | Manual Extraction | Experiment Required | Blocked | Status |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in readiness:
        lines.append(
            f"| `{r.observable_class}` | {r.target_count} | {r.y_true_available_count} | {r.public_data_acquirable_count} | {r.manual_extraction_count} | {r.experiment_required_count} | {r.blocked_count} | **{r.readiness_status}** |"
        )
    return "\n".join(lines) + "\n"


def _render_qc(result: ObservableYTrueCampaignResult) -> str:
    gate = result.gate_result
    qc = gate.qc_rules
    return "\n".join([
        "# PHI_GRADIENT Quality Control Rules v4.2",
        "",
        f"- rules_id: `{qc.rules_id}`",
        "",
        "## QC Rules List",
        "",
        *[f"- **{rule}**" for rule in qc.rules],
    ]) + "\n"


def _render_campaign(result: ObservableYTrueCampaignResult) -> str:
    gate = result.gate_result
    plan = gate.y_true_acquisition_plan
    target_count = len(gate.normalized_targets)
    acq_count = len(plan)

    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-OBSERVABLE-DATASET-YTRUE-PLAN-v4_2",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- normalized_targets: `{target_count}`",
        f"- acquisition_items: `{acq_count}`",
        f"- PredictiveGain status: `UNDEFINED` (no real y_true acquired yet)",
        f"- SLOT_4 debt status: `OPEN_BLOCKING_FOR_GRADIENT_CLAIMS`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
