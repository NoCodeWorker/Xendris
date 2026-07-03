"""Reports for v3.9 source pressure decision gate."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.source_pressure_decision.schemas import SourcePressureCampaignResult


def write_source_pressure_reports(
    result: SourcePressureCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    sp_dir = root / "source_pressure"
    campaigns_dir = root / "campaigns"
    sp_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "decision": sp_dir / "phi_gradient_source_pressure_decision_v3_9.md",
        "extract_pressure_map": sp_dir / "phi_gradient_extract_pressure_map_v3_9.md",
        "slot_pressure_summary": sp_dir / "phi_gradient_slot_pressure_summary_v3_9.md",
        "benchmark_alignment": sp_dir / "phi_gradient_benchmark_alignment_v3_9.md",
        "contradiction_map": sp_dir / "phi_gradient_contradiction_and_limitation_map_v3_9.md",
        "recommendations": sp_dir / "phi_gradient_next_model_update_recommendations_v3_9.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-SOURCE-PRESSURE-DECISION-v3_9.md",
    }
    renderers = {
        "decision": _render_decision,
        "extract_pressure_map": _render_extract_map,
        "slot_pressure_summary": _render_slot_summary,
        "benchmark_alignment": _render_benchmark,
        "contradiction_map": _render_contradiction,
        "recommendations": _render_recommendations,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: SourcePressureCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Source Pressure Decision v3.9",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="source_pressure_decision",
        reports_generated=reports_generated or [],
        next_actions=gate.next_recommendations,
        discipline_note="A source-pressure gate that cannot contradict the hypothesis is not a gate.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_decision(result: SourcePressureCampaignResult) -> str:
    gate = result.gate_result
    dec = gate.decision
    return "\n".join([
        "# PHI_GRADIENT Source Pressure Decision v3.9",
        "",
        f"- status: `{gate.status}`",
        f"- primary_decision: `{dec.primary_decision}`",
        f"- confidence: `{dec.confidence}`",
        f"- gradient_component_support: `{dec.gradient_component_support}`",
        f"- validation_ready_count: `{dec.validation_ready_count}`",
        f"- physical_claim_permission: `{dec.physical_claim_permission}`",
        "",
        "## Global Decisions",
        "",
        *[f"- `{d}`" for d in dec.global_decisions],
        "",
        "## Allowed Claims",
        "",
        *[f"- {claim}" for claim in dec.allowed_claims],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in dec.blocked_claims],
        "",
        "## Next Recommendations",
        "",
        *[f"- {rec}" for rec in dec.next_recommendations],
    ]) + "\n"


def _render_extract_map(result: SourcePressureCampaignResult) -> str:
    records = result.gate_result.extract_pressure_records
    return "\n".join([
        "# PHI_GRADIENT Extract Pressure Map v3.9",
        "",
        f"- extract_count: `{len(records)}`",
        "",
        *[f"- `{r.extract_id}`: class=`{r.pressure_class}`, slot=`{r.assigned_slot}`, score=`{r.pressure_score}`, confidence=`{r.confidence}`"
          for r in records[:80]],
    ]) + "\n"


def _render_slot_summary(result: SourcePressureCampaignResult) -> str:
    slots = result.gate_result.slot_pressure_summary
    lines = [
        "# PHI_GRADIENT Slot Pressure Summary v3.9",
        "",
    ]
    for slot in slots:
        lines.extend([
            f"## {slot.slot_id}",
            "",
            f"- extract_count: `{slot.extract_count}`",
            f"- support_count: `{slot.support_count}`",
            f"- contradiction_count: `{slot.contradiction_count}`",
            f"- limitation_count: `{slot.limitation_count}`",
            f"- analogy_only_count: `{slot.analogy_only_count}`",
            f"- inconclusive_count: `{slot.inconclusive_count}`",
            f"- pressure_status: `{slot.pressure_status}`",
            f"- pressure_score: `{slot.pressure_score}`",
            "",
        ])
    return "\n".join(lines)


def _render_benchmark(result: SourcePressureCampaignResult) -> str:
    bm = result.gate_result.benchmark_alignment
    return "\n".join([
        "# PHI_GRADIENT Benchmark Alignment v3.9",
        "",
        f"- benchmark_decision: `{bm.benchmark_decision}`",
        f"- benchmark_extract_count: `{len(bm.benchmark_extracts)}`",
        f"- observable_alignment_count: `{len(bm.observable_alignment)}`",
        f"- range_alignment_count: `{len(bm.range_alignment)}`",
        "",
        "## Missing Benchmark Fields",
        "",
        *_or_none([f"- {field}" for field in bm.missing_benchmark_fields]),
        "",
        "## Limitations",
        "",
        *[f"- {limit}" for limit in bm.limitations],
    ]) + "\n"


def _render_contradiction(result: SourcePressureCampaignResult) -> str:
    cm = result.gate_result.contradiction_map
    return "\n".join([
        "# PHI_GRADIENT Contradiction and Limitation Map v3.9",
        "",
        f"- contradiction_count: `{len(cm.contradictions)}`",
        f"- limitation_count: `{len(cm.limitations)}`",
        "",
        "## Dominant Risks",
        "",
        *_or_none([f"- {risk}" for risk in cm.dominant_risks]),
        "",
        "## Required Model Changes",
        "",
        *_or_none([f"- {change}" for change in cm.required_model_changes]),
        "",
        "## Affected Slots",
        "",
        *_or_none([f"- `{slot}`" for slot in cm.affected_slots]),
    ]) + "\n"


def _render_recommendations(result: SourcePressureCampaignResult) -> str:
    dec = result.gate_result.decision
    return "\n".join([
        "# PHI_GRADIENT Next Model Update Recommendations v3.9",
        "",
        f"- primary_decision: `{dec.primary_decision}`",
        f"- gradient_component_support: `{dec.gradient_component_support}`",
        "",
        "## Recommendations",
        "",
        *_or_none([f"- {rec}" for rec in dec.next_recommendations]),
    ]) + "\n"


def _render_campaign(result: SourcePressureCampaignResult) -> str:
    gate = result.gate_result
    dec = gate.decision
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-SOURCE-PRESSURE-DECISION-v3_9",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- primary_decision: `{dec.primary_decision}`",
        f"- confidence: `{dec.confidence}`",
        f"- gradient_component_support: `{dec.gradient_component_support}`",
        f"- validation_ready_count: `{dec.validation_ready_count}`",
        f"- physical_claim_permission: `{dec.physical_claim_permission}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
