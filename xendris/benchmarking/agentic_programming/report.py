from __future__ import annotations

import datetime


def generate_markdown_report(
    scores: dict[str, dict[str, float]],
    summary: dict,
    excellence_decisions: dict[str, str],
    output_path: str,
) -> str:
    lines: list[str] = []
    lines.append("# Xendris — Agentic Programming Benchmark Report")
    lines.append("")
    lines.append(f"**Date:** {datetime.date.today().isoformat()}")
    bv = summary.get('benchmark_version', '0.1')
    if bv.startswith('v'):
        bv = bv[1:]
    lines.append(f"**Benchmark:** {summary.get('benchmark_name', 'Agentic Programming Reliability')} v{bv}")
    lines.append(f"**Execution Mode:** {summary.get('execution_mode', 'N/A')}")
    lines.append(f"**Provider Mode:** {summary.get('provider_mode', 'N/A')}")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total tasks: {summary.get('dataset_size', summary.get('total_tasks', 'N/A'))}")
    lines.append(f"- Total results: {summary.get('total_results', 'N/A')}")
    lines.append(f"- Agents evaluated: {len(summary.get('variants', summary.get('agents', [])))}")
    lines.append(f"- Execution mode: {summary.get('execution_mode', 'N/A')}")
    lines.append(f"- Provider mode: {summary.get('provider_mode', 'N/A')}")
    if summary.get("benchmark_level_decision"):
        lines.append(f"- Benchmark-level decision: {summary.get('benchmark_level_decision')}")
    if summary.get("comparison_mode"):
        lines.append("- Comparison mode: enabled")
    lines.append("")

    lines.append("## Scores by Agent Variant")
    lines.append("")
    lines.append("| Variant | Total Score | Tasks Passed | Total Tasks | Pass Rate |")
    lines.append("|---------|-------------|--------------|-------------|-----------|")
    for variant, data in scores.items():
        lines.append(
            f"| {variant} | {data['total_score']} | "
            f"{data['tasks_passed']} | {data['tasks_total']} | "
            f"{data['pass_rate']} |"
        )
    lines.append("")

    lines.append("## Excellence Gate Decisions")
    lines.append("")
    lines.append("| Variant | Decision |")
    lines.append("|---------|----------|")
    for variant, decision in excellence_decisions.items():
        lines.append(f"| {variant} | {decision} |")
    lines.append("")

    blocked_variants = summary.get("blocked_variants", [])
    if blocked_variants:
        lines.append("## Blocked Variant Handling")
        lines.append("")
        lines.append(
            "Blocked variants are included for comparison only and are not admitted as positive evidence."
        )
        lines.append("")
        lines.append("| Variant | Reason |")
        lines.append("|---------|--------|")
        reasons = summary.get("blocked_variant_reasons", {})
        for variant in blocked_variants:
            lines.append(f"| {variant} | {reasons.get(variant, 'Blocked by variant-level interpretation gate.')} |")
        lines.append("")
        if "deepseek_base_agent" in blocked_variants:
            lines.append(
                "On this run, the baseline variant was blocked by the interpretation gate, while Xendris variants may be ready. This permits a bounded comparison of observed benchmark behavior, but the blocked baseline must not be treated as admitted positive evidence."
            )
            lines.append("")

    if summary.get("comparison_interpretation_scope"):
        lines.append("## Conservative Comparison Interpretation")
        lines.append("")
        lines.append(summary["comparison_interpretation_scope"])
        lines.append("")

    lines.append("## Forbidden Interpretations")
    lines.append("")
    lines.append("- Universal superiority over any other model or agent framework.")
    lines.append("- General coding superiority.")
    lines.append("- Production readiness.")
    lines.append("- Treating blocked variants as admitted positive evidence.")
    lines.append("")

    limitations = summary.get("limitations", [])
    if limitations:
        lines.append("## Limitations")
        lines.append("")
        for lim in limitations:
            lines.append(f"- {lim}")
        lines.append("")

    if summary.get("no_real_provider_performance_warning"):
        lines.append("## Warning: No Real Provider Called")
        lines.append("")
        lines.append(summary["no_real_provider_performance_warning"])
        lines.append("")

    if summary.get("no_universal_superiority_warning"):
        lines.append("## Warning: No Superiority Claim")
        lines.append("")
        lines.append(summary["no_universal_superiority_warning"])
        lines.append("")

    if summary.get("no_general_coding_superiority_warning"):
        lines.append("## Warning: No General Coding Superiority Claim")
        lines.append("")
        lines.append(summary["no_general_coding_superiority_warning"])
        lines.append("")

    commercial = summary.get("commercial_metrics")
    if commercial:
        lines.append("## Commercial Metrics")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        for key, val in commercial.items():
            lines.append(f"| {key} | {val} |")
        lines.append("")

    lines.append("## Legend")
    lines.append("")
    lines.append("- **Total Score:** Weighted composite (0-1 scale)")
    lines.append("- **Tasks Passed:** Visible + hidden tests both green")
    lines.append("- **Excellence Gate:** READY_FOR_INTERPRETATION | WARNINGS_PRESENT | BLOCKED_FOR_INTERPRETATION")
    lines.append("")

    report = "\n".join(lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return report
