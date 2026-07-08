from __future__ import annotations

from typing import Any


def build_cost_frontier_report(
    summary: dict[str, Any],
    cost_frontier: dict[str, Any],
) -> str:
    lines: list[str] = []
    _add = lines.append

    _add(f"# Cost Frontier Model-Step Report — {summary.get('run_id', 'unknown')}")
    _add("")
    _add(f"**Benchmark:** {summary.get('benchmark_name', '')} v{summary.get('benchmark_version', '')}")
    _add(f"**Experiment:** {summary.get('experiment_type', 'cost_frontier_model_step')}")
    _add(f"**Dataset:** {summary.get('dataset_name', '')} v{summary.get('dataset_version', '')} ({summary.get('dataset_size', 0)} tasks)")
    _add(f"**Final Decision:** {summary.get('final_decision', 'unknown')}")
    _add("")

    _add("## Methodology")
    _add("")
    _add("This benchmark compares whether a cheaper model plus Xendris Calibrated Runtime is more cost-effective than the immediately superior model without Xendris.")
    _add("")
    _add("### DeepSeek Comparisons")
    _add("- A: deepseek_v4_flash_calibrated_runtime vs deepseek_v4_flash_base (calibrated gain on same model)")
    _add("- B: deepseek_v4_pro_base vs deepseek_v4_flash_base (next model step, no Xendris)")
    _add("- C: deepseek_v4_flash_calibrated_runtime vs deepseek_v4_pro_base (cheap calibrated vs next model)")
    _add("")
    _add("### OpenAI Comparisons")
    _add("- A: gpt_4_1_nano_calibrated_runtime vs gpt_4_1_nano_base (calibrated gain on same model)")
    _add("- B: gpt_4_1_mini_base vs gpt_4_1_nano_base (next model step, no Xendris)")
    _add("- C: gpt_4_1_nano_calibrated_runtime vs gpt_4_1_mini_base (cheap calibrated vs next model)")
    _add("")

    _add("## Score Absolute Table")
    _add("")
    _add("| Variant | Mean Score | Min | Max | Cost | Cost per Score Point |")
    _add("|---|---|---|---|---|---|")
    for agg in summary.get("aggregates", []):
        _add(
            f"| {agg.get('variant_name', '')} "
            f"| {agg.get('mean_score', 0):.6f} "
            f"| {agg.get('min_score', 0):.4f} "
            f"| {agg.get('max_score', 0):.4f} "
            f"| ${agg.get('total_cost_usd', 0):.6f} "
            f"| ${agg.get('cost_per_mean_score_point', 0):.8f} |"
        )
    _add("")

    comparisons = cost_frontier.get("comparisons", [])
    if comparisons:
        _add("## Cost Frontier Comparisons")
        _add("")
        for comp in comparisons:
            if "error" in comp:
                _add(f"### {comp.get('comparison_name', '?')} — ERROR: {comp['error']}")
                _add("")
                continue
            _add(f"### {comp.get('comparison_name', '?')}")
            _add("")
            _add(f"| Metric | Control ({comp.get('control_variant', '')}) | Treatment ({comp.get('treatment_variant', '')}) |")
            _add(f"|---|---|---|")
            _add(f"| Mean score | {comp.get('control_mean', 0):.6f} | {comp.get('treatment_mean', 0):.6f} |")
            _add(f"| Mean delta | | {comp.get('mean_delta', 0):.6f} |")
            _add(f"| Median delta | | {comp.get('median_delta', 0):.6f} |")
            _add(f"| Wins / Losses / Ties | | {comp.get('wins', 0)} / {comp.get('losses', 0)} / {comp.get('ties', 0)} |")
            _add(f"| Win rate (ex ties) | | {comp.get('win_rate_excluding_ties', 0):.4f} |")
            _add(f"| Total cost | ${comp.get('cost_a', 0):.6f} | ${comp.get('cost_b', 0):.6f} |")
            _add(f"| Cost delta | | ${comp.get('cost_delta', 0):.6f} |")
            _add(f"| Cost ratio | | {comp.get('cost_ratio', 0):.4f}x |")
            _add(f"| Cost per task | ${comp.get('cost_per_task_a', 0):.8f} | ${comp.get('cost_per_task_b', 0):.8f} |")
            _add(f"| Cost per score point | ${comp.get('cost_per_mean_score_point_a', 0):.8f} | ${comp.get('cost_per_mean_score_point_b', 0):.8f} |")
            cpl = comp.get('cost_per_lift_point')
            if cpl is not None:
                _add(f"| Cost per lift point | | ${cpl:.8f} |")
            _add(f"| **Efficient Frontier Decision** | | **{comp.get('efficient_frontier_decision', '?')}** |")
            _add("")

    _add("## Execution Summary")
    _add("")
    _add(f"- Total expected attempts: {summary.get('total_expected', 0)}")
    _add(f"- Total completed: {summary.get('total_completed', 0)}")
    _add(f"- Total failed: {summary.get('total_failed', 0)}")
    _add(f"- Total cost: ${summary.get('total_cost_usd', 0):.8f}")
    _add(f"- Budget cap: ${summary.get('budget_cap_usd', 0):.2f}")
    _add(f"- Budget decision: {summary.get('budget_decision', 'unknown')}")
    _add(f"- Runtime variant traces: {summary.get('runtime_variant_trace_count', 0)}")
    _add(f"- Calibration traces: {summary.get('calibration_trace_count', 0)}")
    _add("")

    fl = summary.get("family_lift", {})
    if fl:
        _add("## Family Score Summary")
        _add("")
        for family, variants in fl.items():
            _add(f"**{family}:**")
            for vn, mean in variants.items():
                _add(f"- {vn}: {mean:.6f}")
            _add("")

    _add("## Authorized Claims")
    _add("")
    for c in summary.get("authorized_claims", []):
        _add(f"- {c}")
    _add("")

    _add("## Prohibited Claims")
    _add("")
    for c in summary.get("prohibited_claims", []):
        _add(f"- {c}")
    _add("")

    _add("---")
    _add("*This is a diagnostic-only cost frontier comparison. No universal or statistical superiority claim is authorized. Results apply to this controlled n=30 dataset only.*")

    return "\n".join(lines)
