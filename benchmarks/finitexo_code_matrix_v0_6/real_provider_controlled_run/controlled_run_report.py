"""Report builder for v0.6.0 controlled run n=30."""

from __future__ import annotations

from typing import Any


def build_controlled_run_report(summary: dict[str, Any]) -> str:
    decision = summary.get("final_decision", "UNKNOWN")
    lines = [
        "# Finitexo Code Matrix v0.6.0 — Real Provider Controlled Run n=30",
        "",
        "## Summary",
        "",
        f"- Run ID: `{summary.get('run_id', 'unknown')}`",
        f"- Final decision: `{decision}`",
        f"- Dataset: {summary.get('dataset_name', 'unknown')} v{summary.get('dataset_version', '?')}",
        f"- Dataset size: {summary.get('dataset_size', 0)}",
        f"- Provider mode: {summary.get('provider_mode', 'unknown')}",
        f"- Providers: {', '.join(summary.get('providers', []))}",
        "",
        "## Attempts",
        "",
        f"- Total expected: {summary.get('total_expected', 0)}",
        f"- Attempted: {summary.get('total_attempted', 0)}",
        f"- Completed: {summary.get('total_completed', 0)}",
        f"- Failed: {summary.get('total_failed', 0)}",
        f"- Budget blocked: {summary.get('total_budget_blocked', 0)}",
        "",
        "## Cost",
        "",
        f"- Total estimated cost: ${summary.get('total_cost_usd', 0):.8f}",
        f"- Budget cap: ${summary.get('budget_cap_usd', 0):.2f}",
        f"- Budget decision: `{summary.get('budget_decision', 'UNKNOWN')}`",
        "",
        "## Scores",
        "",
        f"- Overall mean score: {summary.get('mean_score_overall', 'N/A')}",
        "",
    ]

    # Per-provider table
    providers = summary.get("providers", [])
    if providers:
        lines.append("### Provider Scores")
        lines.append("")
        lines.append("| Provider | Task Count | Mean Score | Min | Max | Verified |")
        lines.append("|---|---|---|---|---|---|")
        agg = summary.get("aggregates", {})
        if isinstance(agg, list):
            prov_map = {a.get("provider_name"): a for a in agg}
        else:
            prov_map = agg
        for p in providers:
            a = prov_map.get(p, {}) if isinstance(prov_map, dict) else {}
            tc = a.get("task_count", 0)
            ms = a.get("mean_score", "N/A")
            mn = a.get("min_score", "N/A")
            mx = a.get("max_score", "N/A")
            vc = a.get("verified_count", 0)
            lines.append(f"| {p} | {tc} | {ms} | {mn} | {mx} | {vc} |")
        lines.append("")

        # Component means per provider
        lines.append("### Component Means by Provider")
        lines.append("")
        all_comps: set[str] = set()
        if isinstance(agg, list):
            for a in agg:
                all_comps.update(a.get("component_means", {}).keys())
        elif isinstance(agg, dict):
            for a in agg.values():
                all_comps.update(a.get("component_means", {}).keys())

        if all_comps:
            header = "| Provider | " + " | ".join(sorted(all_comps)) + " |"
            sep = "|" + "---|" * (len(all_comps) + 1)
            lines.append(header)
            lines.append(sep)
            for p in providers:
                a = prov_map.get(p, {}) if isinstance(prov_map, dict) else {}
                cm = a.get("component_means", {}) if isinstance(a, dict) else {}
                vals = [str(cm.get(c, "N/A")) for c in sorted(all_comps)]
                lines.append(f"| {p} | " + " | ".join(vals) + " |")
            lines.append("")

    # Claims
    lines.append("## Authorized Claims")
    lines.append("")
    for claim in summary.get("authorized_claims", []):
        lines.append(f"- {claim}")
    lines.append("")

    lines.append("## Prohibited Claims")
    lines.append("")
    for claim in summary.get("prohibited_claims", []):
        lines.append(f"- {claim}")
    lines.append("")

    # Cost by provider
    cost_by_provider = summary.get("cost_by_provider", {})
    if cost_by_provider:
        lines.append("## Cost by Provider")
        lines.append("")
        for p, c in sorted(cost_by_provider.items()):
            lines.append(f"- {p}: ${c:.8f}")
        lines.append("")

    # Warnings
    warnings = summary.get("warnings", [])
    if warnings:
        lines.append("## Warnings")
        lines.append("")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    # Errors
    errors = summary.get("errors", [])
    if errors:
        lines.append("## Provider Errors")
        lines.append("")
        for e in errors:
            lines.append(f"- {e}")
        lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("This is a **controlled diagnostic real-provider run**. "
                  "It does not prove model superiority. Results are limited to the "
                  "Finitexo Code Matrix v0.6.0 controlled diagnostic n=30 dataset. "
                  "No statistical, general coding, production-readiness, or universal "
                  "benchmark claim is authorized.")
    lines.append("")
    lines.append("### Relation to v0.5.x Chain")
    lines.append("")
    lines.append("This phase extends the v0.5.4–v0.5.7 diagnostic chain into a "
                  "controlled real-provider execution with n=30. The v0.5.7 report "
                  "admissibility gate confirmed readiness for this phase. All v0.5.x "
                  "safety boundaries (no mock fallback, diagnostic-only scoring, "
                  "no superiority claims) are preserved.")
    lines.append("")

    return "\n".join(lines)
