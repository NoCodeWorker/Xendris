"""Report builder for v0.7.0 paired Xendris lift."""

from __future__ import annotations

from typing import Any


def build_paired_lift_report(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    _add = lines.append

    _add(f"# Paired Xendris Lift Report — {summary.get('run_id', 'unknown')}")
    _add("")
    _add(f"**Benchmark:** {summary.get('benchmark_name', '')} v{summary.get('benchmark_version', '')}")
    _add(f"**Experiment:** {summary.get('experiment_type', 'paired_xendris_lift')}")
    _add(f"**Dataset:** {summary.get('dataset_name', '')} v{summary.get('dataset_version', '')} ({summary.get('dataset_size', 0)} tasks)")
    _add(f"**Final Decision:** {summary.get('final_decision', 'unknown')}")
    _add("")

    lift = summary.get("paired_lift", {})

    _add("## Paired Lift Summary")
    _add("")
    _add(f"| Metric | DeepSeek | OpenAI |")
    _add(f"|---|---|---|")
    _add(f"| Xendris lift (mean) | {lift.get('deepseek_xendris_minus_base', 'N/A')} | {lift.get('openai_xendris_minus_base', 'N/A')} |")
    _add(f"| Cost delta (Xendris − base) | ${lift.get('cost_delta_xendris_vs_base_deepseek', 'N/A')} | ${lift.get('cost_delta_xendris_vs_base_openai', 'N/A')} |")
    cpl_ds = lift.get("cost_per_lift_point_deepseek")
    cpl_oa = lift.get("cost_per_lift_point_openai")
    _add(f"| Cost per lift point | ${cpl_ds if cpl_ds is not None else 'N/A'} | ${cpl_oa if cpl_oa is not None else 'N/A'} |")
    _add("")

    _add("## Variant Aggregates")
    _add("")
    _add("| Variant | Mean Score | Min | Max | Verified | Cost |")
    _add("|---|---|---|---|---|---|")
    for agg in summary.get("aggregates", []):
        _add(
            f"| {agg['variant_name']} "
            f"| {agg['mean_score']:.4f} "
            f"| {agg['min_score']:.4f} "
            f"| {agg['max_score']:.4f} "
            f"| {agg['verified_count']}/{agg['task_count']} "
            f"| ${agg['total_cost_usd']:.6f} |"
        )
    _add("")

    _add("## Xendris Lift by Component")
    _add("")

    ds_comp = lift.get("xendris_lift_by_component_deepseek", {})
    oa_comp = lift.get("xendris_lift_by_component_openai", {})
    all_comps = sorted(set(list(ds_comp.keys()) + list(oa_comp.keys())))
    if all_comps:
        _add(f"| Component | DeepSeek Lift | OpenAI Lift |")
        _add(f"|---|---|---|")
        for comp in all_comps:
            _add(f"| {comp} | {ds_comp.get(comp, 'N/A')} | {oa_comp.get(comp, 'N/A')} |")
        _add("")

    _add("## Execution Summary")
    _add("")
    _add(f"- Total expected attempts: {summary.get('total_expected', 0)}")
    _add(f"- Total attempted: {summary.get('total_attempted', 0)}")
    _add(f"- Total completed: {summary.get('total_completed', 0)}")
    _add(f"- Total failed: {summary.get('total_failed', 0)}")
    _add(f"- Total cost: ${summary.get('total_cost_usd', 0):.6f}")
    _add(f"- Budget cap: ${summary.get('budget_cap_usd', 0):.2f}")
    _add(f"- Budget decision: {summary.get('budget_decision', 'unknown')}")
    _add("")

    _add("## Claims")
    _add("")
    _add("### Authorized")
    for c in summary.get("authorized_claims", []):
        _add(f"- {c}")
    _add("")
    _add("### Prohibited")
    for c in summary.get("prohibited_claims", []):
        _add(f"- {c}")
    _add("")

    _add("---")
    _add("*This is a diagnostic-only controlled paired lift experiment. No universal superiority claim is authorized.*")

    return "\n".join(lines)
