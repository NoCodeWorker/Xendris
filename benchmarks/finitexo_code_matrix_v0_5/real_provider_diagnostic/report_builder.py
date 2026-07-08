"""Markdown report builder for v0.5.3 diagnostic execution."""

from __future__ import annotations

from typing import Any


def build_real_provider_diagnostic_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.5.3 - Real Provider Diagnostic Execution",
            "",
            "## Scope",
            "",
            "This is diagnostic-only real-provider execution infrastructure.",
            "No statistical claim is authorized.",
            "No provider superiority claim is authorized.",
            "No Xendris superiority claim is authorized.",
            "",
            "## Dataset",
            "",
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
            f"- Task attempts expected: {summary['task_attempts_expected']}",
            f"- Task attempts attempted: {summary['task_attempts_attempted']}",
            f"- Task attempts completed: {summary['task_attempts_completed']}",
            f"- Task attempts failed: {summary['task_attempts_failed']}",
            f"- Task attempts skipped: {summary['task_attempts_skipped']}",
            "",
            "## Budget",
            "",
            f"- Total estimated cost: ${summary['total_estimated_cost_usd']:.8f}",
            f"- Budget decision: `{summary['budget_decision']}`",
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
        ]
    )
