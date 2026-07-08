"""Markdown report builder for v0.5.1 real-provider smoke artifacts."""

from __future__ import annotations

from typing import Any


def build_real_provider_smoke_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.5.1 - Real Provider Smoke on Frozen n=10",
            "",
            "## Purpose",
            "",
            "Run a bounded real-provider smoke test on the explicitly frozen v0.4.3 n=10 dataset.",
            "",
            "## Dataset",
            "",
            f"- Dataset version: `{summary['dataset_version']}`",
            f"- Dataset hash: `{summary['dataset_hash']}`",
            f"- Manifest hash: `{summary['manifest_hash']}`",
            f"- Frozen task count: {summary['frozen_task_count']}",
            "",
            "## Execution",
            "",
            f"- Provider mode: `{summary['provider_mode']}`",
            f"- Providers attempted: `{summary['providers_attempted']}`",
            f"- Providers completed: `{summary['providers_completed']}`",
            f"- Providers failed: `{summary['providers_failed']}`",
            f"- Task attempts completed: {summary['task_attempts_completed']}",
            f"- Task attempts failed: {summary['task_attempts_failed']}",
            f"- Task attempts skipped: {summary['task_attempts_skipped']}",
            f"- Task attempts budget blocked: {summary['task_attempts_budget_blocked']}",
            "",
            "## Budget",
            "",
            f"- Total estimated cost: ${summary['total_estimated_cost_usd']:.8f}",
            f"- Budget cap: ${summary['budget_cap_usd']:.2f}",
            f"- Budget decision: `{summary['budget_decision']}`",
            "",
            "## Boundary",
            "",
            "- real_provider_smoke_completed != provider_superiority_demonstrated",
            "- n10_real_smoke != statistical_significance",
            "- provider_failure != benchmark_failure",
            "- diagnostic_score != external_benchmark_validation",
            "- real_execution != production_readiness",
            "- Mock fallback was not used.",
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
        ]
    )
