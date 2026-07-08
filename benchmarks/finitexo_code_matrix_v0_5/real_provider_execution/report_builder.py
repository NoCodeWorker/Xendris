"""Markdown reporting for v0.5.2 real-provider execution."""

from __future__ import annotations

from typing import Any


def build_real_provider_execution_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.5.2 - Real Provider Execution on Frozen n=10",
            "",
            "## Scope",
            "",
            "This is a diagnostic-only real-provider smoke execution layer.",
            "It does not authorize statistical, provider superiority, Xendris superiority, external validation, or production-readiness claims.",
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
            f"- Providers configured: `{summary['providers_configured']}`",
            f"- Providers attempted: `{summary['providers_attempted']}`",
            f"- Providers completed: `{summary['providers_completed']}`",
            f"- Providers failed: `{summary['providers_failed']}`",
            f"- Task attempts skipped: {summary['task_attempts_skipped']}",
            f"- Task attempts completed: {summary['task_attempts_completed']}",
            f"- Task attempts failed: {summary['task_attempts_failed']}",
            "",
            "## Budget",
            "",
            f"- Total estimated cost: ${summary['total_estimated_cost_usd']:.8f}",
            f"- Budget decision: `{summary['budget_decision']}`",
            "",
            "## Blocked Claims",
            "",
            "- No statistical claim is authorized.",
            "- No provider superiority claim is authorized.",
            "- No Xendris superiority claim is authorized.",
            "- No external benchmark validation claim is authorized.",
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
        ]
    )
