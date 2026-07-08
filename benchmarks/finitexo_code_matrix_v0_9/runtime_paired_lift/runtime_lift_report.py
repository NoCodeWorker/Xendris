"""Report builder for v0.9.0 runtime paired lift."""

from __future__ import annotations

from typing import Any


def build_runtime_lift_report(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    _add = lines.append

    _add(f"# Runtime Paired Lift Report — {summary.get('run_id', 'unknown')}")
    _add("")
    _add(f"**Benchmark:** {summary.get('benchmark_name', '')} v{summary.get('benchmark_version', '')}")
    _add(f"**Experiment:** {summary.get('experiment_type', 'runtime_paired_lift')}")
    _add(f"**Dataset:** {summary.get('dataset_name', '')} v{summary.get('dataset_version', '')} ({summary.get('dataset_size', 0)} tasks)")
    _add(f"**Final Decision:** {summary.get('final_decision', 'unknown')}")
    _add("")

    _add("## Methodology")
    _add("")
    _add("This is a full runtime paired lift experiment. Runtime variants use the Xendris runtime loop:")
    _add("- Initial provider generation")
    _add("- Deterministic audit (12 components)")
    _add("- Audit decision (ALLOW / ALLOW_WITH_LIMITATIONS / REPAIR_REQUIRED / BLOCK / HUMAN_REVIEW_REQUIRED)")
    _add("- Conditional repair pass")
    _add("- Final audit and controlled response")
    _add("")
    _add("Base and wrapper variants are included for comparison. This restores the foundational Xendris methodology after the v0.7.0/v0.8.1 wrapper-only deviations.")
    _add("")

    lift = summary.get("paired_lift", {})

    _add("## Lift Summary (Wrapper vs Base)")
    _add("")
    _add(f"| Metric | DeepSeek | OpenAI |")
    _add(f"|---|---|---|")
    _add(f"| Wrapper lift (mean) | {lift.get('deepseek_wrapper_vs_base_mean_lift', 'N/A')} | {lift.get('openai_wrapper_vs_base_mean_lift', 'N/A')} |")
    _add(f"| Cost delta | ${lift.get('deepseek_wrapper_vs_base_cost_delta', 'N/A')} | ${lift.get('openai_wrapper_vs_base_cost_delta', 'N/A')} |")
    _add("")

    _add("## Lift Summary (Runtime vs Base)")
    _add("")
    _add(f"| Metric | DeepSeek | OpenAI |")
    _add(f"|---|---|---|")
    _add(f"| Runtime lift (mean) | {lift.get('deepseek_runtime_vs_base_mean_lift', 'N/A')} | {lift.get('openai_runtime_vs_base_mean_lift', 'N/A')} |")
    _add(f"| Cost delta | ${lift.get('deepseek_runtime_vs_base_cost_delta', 'N/A')} | ${lift.get('openai_runtime_vs_base_cost_delta', 'N/A')} |")
    _add(f"| Cost per lift point | ${lift.get('deepseek_runtime_vs_base_cost_per_lift_point', 'N/A')} | ${lift.get('openai_runtime_vs_base_cost_per_lift_point', 'N/A')} |")
    _add("")

    _add("## Lift Summary (Runtime vs Wrapper)")
    _add("")
    _add(f"| Metric | DeepSeek | OpenAI |")
    _add(f"|---|---|---|")
    _add(f"| Runtime vs Wrapper lift | {lift.get('deepseek_runtime_vs_wrapper_mean_lift', 'N/A')} | {lift.get('openai_runtime_vs_wrapper_mean_lift', 'N/A')} |")
    _add(f"| Cost delta | ${lift.get('deepseek_runtime_vs_wrapper_cost_delta', 'N/A')} | ${lift.get('openai_runtime_vs_wrapper_cost_delta', 'N/A')} |")
    _add("")

    _add("## Lift Summary (Calibrated Runtime vs Base)")
    _add("")
    _add(f"| Metric | DeepSeek | OpenAI |")
    _add(f"|---|---|---|")
    _add(f"| Calibrated Runtime vs Base lift | {lift.get('deepseek_calibrated_runtime_vs_base_mean_lift', 'N/A')} | {lift.get('openai_calibrated_runtime_vs_base_mean_lift', 'N/A')} |")
    _add(f"| Cost delta | ${lift.get('deepseek_calibrated_runtime_vs_base_cost_delta', 'N/A')} | ${lift.get('openai_calibrated_runtime_vs_base_cost_delta', 'N/A')} |")
    _add("")

    _add("## Lift Summary (Calibrated Runtime vs Wrapper)")
    _add("")
    _add(f"| Metric | DeepSeek | OpenAI |")
    _add(f"|---|---|---|")
    _add(f"| Calibrated vs Wrapper lift | {lift.get('deepseek_calibrated_runtime_vs_wrapper_mean_lift', 'N/A')} | {lift.get('openai_calibrated_runtime_vs_wrapper_mean_lift', 'N/A')} |")
    _add("")

    _add("## Lift Summary (Calibrated Runtime vs Runtime)")
    _add("")
    _add(f"| Metric | DeepSeek | OpenAI |")
    _add(f"|---|---|---|")
    _add(f"| Calibrated vs Runtime lift | {lift.get('deepseek_calibrated_runtime_vs_runtime_mean_lift', 'N/A')} | {lift.get('openai_calibrated_runtime_vs_runtime_mean_lift', 'N/A')} |")
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

    fl = summary.get("family_lift", {})
    fl_families = fl.get("family_lift", {})
    if fl_families:
        _add("## Family Lift")
        _add("")
        _add("| Family | DS Base | DS Wrap | DS Runtime | DS Calibrated | OA Base | OA Wrap | OA Runtime | OA Calibrated | DS Wrap Lift | DS Runtime Lift | DS Calibrated Lift | OA Wrap Lift | OA Runtime Lift | OA Calibrated Lift |")
        _add("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for family, data in fl_families.items():
            _add(
                f"| {family} "
                f"| {data.get('deepseek_base_mean', 0):.4f} "
                f"| {data.get('deepseek_wrapper_mean', 0):.4f} "
                f"| {data.get('deepseek_runtime_mean', 0):.4f} "
                f"| {data.get('deepseek_calibrated_runtime_mean', 0):.4f} "
                f"| {data.get('openai_base_mean', 0):.4f} "
                f"| {data.get('openai_wrapper_mean', 0):.4f} "
                f"| {data.get('openai_runtime_mean', 0):.4f} "
                f"| {data.get('openai_calibrated_runtime_mean', 0):.4f} "
                f"| {data.get('deepseek_wrapper_lift_vs_base', 0):.6f} "
                f"| {data.get('deepseek_runtime_lift_vs_base', 0):.6f} "
                f"| {data.get('deepseek_calibrated_lift_vs_base', 0):.6f} "
                f"| {data.get('openai_wrapper_lift_vs_base', 0):.6f} "
                f"| {data.get('openai_runtime_lift_vs_base', 0):.6f} "
                f"| {data.get('openai_calibrated_lift_vs_base', 0):.6f} |"
            )
        _add("")

    repair = summary.get("repair_metrics", {})
    if repair:
        _add("## Repair Metrics")
        _add("")
        _add("| Provider | Repair Attempts | Repair Successes | Success Rate |")
        _add("|---|---|---|---|")
        for prov, data in repair.items():
            _add(f"| {prov} | {data['repair_attempts']} | {data['repair_successes']} | {data['repair_success_rate']:.2%} |")
        _add("")

    audit_dist = summary.get("audit_decision_distribution", {})
    if audit_dist:
        _add("## Audit Decision Distribution")
        _add("")
        for prov, decisions in audit_dist.items():
            _add(f"**{prov}:**")
            for dec, count in sorted(decisions.items()):
                _add(f"- {dec}: {count}")
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
    _add(f"- Runtime variant traces: {summary.get('runtime_variant_trace_count', 0)}")
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
    _add("*This is a diagnostic-only controlled runtime paired lift experiment. No universal superiority claim is authorized.*")

    return "\n".join(lines)
