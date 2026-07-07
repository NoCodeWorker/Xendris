"""Markdown report builder for v0.3.1 external dataset intake."""

from __future__ import annotations

from typing import Any, Mapping


def build_intake_report(summary: Mapping[str, Any]) -> str:
    phase = summary.get("benchmark_version", "v0.3.1")
    decisions = summary.get("decisions", [])
    if phase == "v0.3.2":
        title = "# Finitexo Code Matrix v0.3.2 - External Adapted Candidate Acquisition"
        extra_sections = [
            "## Why This Exists",
            "",
            "This phase adds honestly documented adapted candidates to reduce dependence on internally authored tasks.",
            "",
            "## Candidate Pool Before",
            "",
            "- v0.3.1 candidate_count: `5`",
            "- v0.3.1 external_adapted: `0`",
            "- v0.3.1 mean_externality_score: `0.468`",
            "",
            "## New Candidate Sources",
            "",
            f"- new_candidate_count: `{summary.get('new_candidate_count', 0)}`",
            f"- external_adapted_count: `{summary.get('new_external_adapted_count', 0)}`",
            "",
            "## New Candidate Tasks",
            "",
            "\n".join(f"- `{item.get('task_id')}` ({item.get('origin')})" for item in decisions if str(item.get("task_id", "")).startswith("fcm_v0_3_2_")) or "- None",
            "",
            "## Target Check",
            "",
            f"- target_mean_externality_score: `{summary.get('target_mean_externality_score', 0.60)}`",
            f"- target_met: `{summary.get('target_met', False)}`",
            "",
        ]
    else:
        title = "# Finitexo Code Matrix v0.3.1 - External Dataset Intake"
        extra_sections = []
    accepted = [item for item in decisions if item.get("intake_decision") == "ACCEPTED"]
    rejected = [item for item in decisions if item.get("intake_decision") == "REJECTED"]
    warnings = [item for item in decisions if item.get("warnings")]
    return "\n".join(
        [
            title,
            "",
            "## Scope",
            "",
            "This intake run validates source traceability and candidate task metadata. It does not execute providers or measure performance.",
            "",
            *extra_sections,
            "## Source Registry",
            "",
            f"- registry_issues: `{summary.get('source_registry_issues', [])}`",
            "",
            "## Candidate Tasks",
            "",
            f"- candidate_count: `{summary.get('candidate_count', 0)}`",
            f"- accepted_count: `{summary.get('accepted_count', 0)}`",
            f"- warnings_count: `{summary.get('warnings_count', 0)}`",
            f"- rejected_count: `{summary.get('rejected_count', 0)}`",
            "",
            "## Origin Distribution",
            "",
            f"`{summary.get('origin_distribution', {})}`",
            "",
            "## Externality Score",
            "",
            f"- mean_externality_score: `{summary.get('mean_externality_score', 0.0)}`",
            "",
            "Externality is diagnostic and does not authorize performance claims.",
            "",
            "## Accepted Candidates",
            "",
            "\n".join(f"- `{item.get('task_id')}` ({item.get('origin')})" for item in accepted) or "- None",
            "",
            "## Rejected Candidates",
            "",
            "\n".join(f"- `{item.get('task_id')}`: {item.get('blocking_issues')}" for item in rejected) or "- None",
            "",
            "## Warnings",
            "",
            "\n".join(f"- `{item.get('task_id')}`: {item.get('warnings')}" for item in warnings) or "- None",
            "",
            "## Limitations",
            "",
            "- Candidate pool does not modify the frozen seed dataset.",
            "- No real provider execution was performed.",
            "- No externality score is performance evidence.",
            "",
            "## Claims Explicitly Not Authorized",
            "",
            "- Universal superiority.",
            "- General coding superiority.",
            "- Production readiness.",
            "- Provider superiority.",
            "- Performance claims from dataset origin alone.",
            "",
            "## Conclusion",
            "",
            f"`{summary.get('phase_decision', summary.get('intake_decision', 'REJECTED'))}`",
            "",
            "No real provider execution was performed.",
            "",
        ]
    )
