"""Generate Markdown reports for v4.0 benchmark construction."""

from __future__ import annotations

from pathlib import Path

from phyng.benchmark_construction.schemas import BenchmarkConstructionCampaignResult
from phyng.core.report_contract import append_canonical_status_section, build_report_contract


def write_benchmark_construction_reports(
    result: BenchmarkConstructionCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    bc_dir = root / "benchmark_construction"
    campaigns_dir = root / "campaigns"

    bc_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "manifest": bc_dir / "phi_gradient_benchmark_dataset_manifest_v4_0.md",
        "observable_alignment": bc_dir / "phi_gradient_observable_alignment_v4_0.md",
        "benchmark_rows": bc_dir / "phi_gradient_benchmark_rows_v4_0.md",
        "negative_control_plan": bc_dir / "phi_gradient_negative_control_plan_v4_0.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-DEBT-AWARE-BENCHMARK-v4_0.md",
    }

    renderers = {
        "manifest": _render_manifest,
        "observable_alignment": _render_alignment,
        "benchmark_rows": _render_rows,
        "negative_control_plan": _render_controls,
    }

    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")

    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map

    # Write campaign report with all generated paths
    paths["campaign"].write_text(
        _canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8"
    )

    return path_map


def _canonical(
    markdown: str,
    result: BenchmarkConstructionCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Debt-Aware Benchmark Construction v4.0",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="benchmark_construction",
        reports_generated=reports_generated or [],
        next_actions=[
            "v4.1 — Benchmark Model Comparison Without Gradient Claim",
            "Targeted SLOT_4 resolution in parallel",
        ],
        discipline_note="Do not let benchmark progress launder mechanism debt.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_manifest(result: BenchmarkConstructionCampaignResult) -> str:
    gate = result.gate_result
    m = gate.manifest
    return "\n".join([
        "# PHI_GRADIENT Benchmark Dataset Manifest v4.0",
        "",
        f"- dataset_id: `{m.dataset_id}`",
        f"- status: `{m.status}`",
        f"- benchmark_row_count: `{m.benchmark_row_count}`",
        f"- observable_alignment_count: `{m.observable_alignment_count}`",
        f"- negative_control_count: `{m.negative_control_count}`",
        f"- source_pressure_ref: `{m.source_pressure_ref}`",
        f"- validation_pack_ref: `{m.validation_pack_ref}`",
        f"- debt_registry_ref: `{m.debt_registry_ref}`",
        "",
        "## Excluded Claims",
        "",
        *[f"- {claim}" for claim in m.excluded_claims],
        "",
        "## Allowed Usage",
        "",
        *[f"- {use}" for use in m.allowed_usage],
        "",
        "## Blocked Usage",
        "",
        *[f"- {use}" for use in m.blocked_usage],
    ]) + "\n"


def _render_alignment(result: BenchmarkConstructionCampaignResult) -> str:
    gate = result.gate_result
    alignments = gate.observable_alignment
    lines = [
        "# PHI_GRADIENT Observable Alignment v4.0",
        "",
        f"- alignment_count: `{len(alignments)}`",
        "",
    ]
    for a in alignments[:40]:
        lines.extend([
            f"### {a.alignment_id} ({a.source_id})",
            "",
            f"- extract_id: `{a.extract_id}`",
            f"- observable: `{a.observable}`",
            f"- status: `{a.alignment_status}`",
            f"- source text: *\"{a.source_observable_text}\"*",
            f"- baseline mapping: `{a.baseline_model_mapping}`",
            f"- candidate mapping: `{a.candidate_model_mapping}`",
            "",
        ])
    return "\n".join(lines)


def _render_rows(result: BenchmarkConstructionCampaignResult) -> str:
    gate = result.gate_result
    rows = gate.rows
    lines = [
        "# PHI_GRADIENT Benchmark Rows v4.0",
        "",
        f"- row_count: `{len(rows)}`",
        "",
    ]
    for r in rows[:40]:
        lines.extend([
            f"### {r.benchmark_id} ({r.source_id})",
            "",
            f"- extract_id: `{r.extract_id}`",
            f"- type: `{r.observable_type}`",
            f"- mass_range: `{r.mass_range or 'None'}`",
            f"- time_range: `{r.time_range or 'None'}`",
            f"- length/separation: `{r.length_or_separation_range or 'None'}`",
            f"- temperature/pressure: `{r.temperature_or_pressure or 'None'}`",
            f"- benchmark_use: `{r.benchmark_use}`",
            f"- allowed_model_comparison: `{r.allowed_model_comparison}`",
            f"- gradient_claim_allowed: `{r.gradient_claim_allowed}`",
            f"- observable_text: *\"{r.observable_text}\"*",
            "",
        ])
    return "\n".join(lines)


def _render_controls(result: BenchmarkConstructionCampaignResult) -> str:
    gate = result.gate_result
    p = gate.negative_control_plan
    lines = [
        "# PHI_GRADIENT Negative Control Plan v4.0",
        "",
        f"- plan_id: `{p.plan_id}`",
        f"- created_at: `{p.created_at}`",
        "",
        "## Controls",
        "",
    ]
    for c in p.controls:
        lines.extend([
            f"### {c.control_id} - {c.control_type}",
            "",
            f"- source: `{c.source_id}`",
            f"- slot: `{c.slot_id}`",
            f"- what it tests: {c.what_it_tests}",
            f"- failure condition: *{c.failure_condition}*",
            f"- expected if analogy: {c.expected_result_if_PHIGRADIENT_is_only_analogy}",
            f"- expected if signal: {c.expected_result_if_candidate_has_signal}",
            "",
        ])
    return "\n".join(lines)


def _render_campaign(result: BenchmarkConstructionCampaignResult) -> str:
    gate = result.gate_result
    m = gate.manifest
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-DEBT-AWARE-BENCHMARK-v4_0",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- row_count: `{m.benchmark_row_count}`",
        f"- alignment_count: `{m.observable_alignment_count}`",
        f"- control_count: `{m.negative_control_count}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
