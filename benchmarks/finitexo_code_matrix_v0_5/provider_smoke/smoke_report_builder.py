"""Markdown report builder for provider smoke summaries."""

from __future__ import annotations

from typing import Any


def build_markdown_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.5 - Provider Smoke on Frozen n=10",
            "",
            "## Summary",
            "",
            f"- Run id: `{summary['run_id']}`",
            f"- Provider mode: `{summary['provider_mode']}`",
            f"- Dataset hash: `{summary['dataset_hash']}`",
            f"- Manifest hash: `{summary['manifest_hash']}`",
            f"- Frozen task count: {summary['frozen_task_count']}",
            f"- Providers attempted: `{summary['providers_attempted']}`",
            f"- Providers completed: `{summary['providers_completed']}`",
            f"- Providers failed: `{summary['providers_failed']}`",
            f"- Total estimated cost: ${summary['total_estimated_cost_usd']:.8f}",
            f"- Budget decision: `{summary['budget_decision']}`",
            "",
            "## Boundary",
            "",
            "- Smoke diagnostics are not benchmark validation.",
            "- No statistical claim is authorized.",
            "- No provider superiority claim is authorized.",
            "- No Xendris superiority claim is authorized.",
            "- Provider failures, if any, are reported.",
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
        ]
    )
