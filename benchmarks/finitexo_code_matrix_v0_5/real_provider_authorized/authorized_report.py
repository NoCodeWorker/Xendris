"""Markdown report for v0.5.4 authorized diagnostics."""

from __future__ import annotations

from typing import Any


def build_authorized_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.5.4 - Authorized Real Provider Diagnostic Execution",
            "",
            "## Scope",
            "",
            "This is diagnostic-only real-provider execution. It is not a conclusive benchmark.",
            "",
            "- No statistical claim is authorized.",
            "- No provider superiority claim is authorized.",
            "- No Xendris superiority claim is authorized.",
            "",
            "## Dataset",
            "",
            f"- Dataset hash: `{summary['dataset_hash']}`",
            f"- Manifest hash: `{summary['manifest_hash']}`",
            f"- Frozen task count: {summary['frozen_task_count']}",
            "",
            "## Execution",
            "",
            f"- Providers configured: `{summary['providers_configured']}`",
            f"- Providers attempted: `{summary['providers_attempted']}`",
            f"- Providers completed: `{summary['providers_completed']}`",
            f"- Providers failed: `{summary['providers_failed']}`",
            f"- Task attempts expected: {summary['task_attempts_expected']}",
            f"- Task attempts attempted: {summary['task_attempts_attempted']}",
            f"- Task attempts skipped: {summary['task_attempts_skipped']}",
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
