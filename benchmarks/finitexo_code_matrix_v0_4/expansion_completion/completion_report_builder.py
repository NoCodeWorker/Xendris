"""Report generation for v0.4.2 expansion pool completion."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .completion_validator import ROOT, evaluate_completion_policy


OUTDIR = Path("runs/finitexo_code_matrix_v0_4_2_expansion_completion")


def build_completion_summary(root: Path = ROOT) -> dict[str, Any]:
    result = evaluate_completion_policy(root)
    manifest = result["manifest"]
    candidates = result["candidates"]
    readiness_counts = Counter(candidate["expansion_readiness"] for candidate in candidates)
    return {
        "benchmark_name": manifest["benchmark_name"],
        "base_benchmark_version": manifest["base_benchmark_version"],
        "expansion_intake_version": manifest["expansion_intake_version"],
        "expansion_completion_version": manifest["expansion_completion_version"],
        "current_frozen_task_count": manifest["base_frozen_task_count"],
        "target_frozen_task_count": manifest["target_frozen_task_count"],
        "additional_ready_candidates_required": manifest["additional_ready_candidates_required"],
        "total_expansion_candidates": len(candidates),
        "ready_for_future_freeze": result["ready_for_future_freeze"],
        "ready_with_human_review": result["ready_with_human_review"],
        "needs_more_provenance": readiness_counts["NEEDS_MORE_PROVENANCE"],
        "needs_more_validation": readiness_counts["NEEDS_MORE_VALIDATION"],
        "do_not_freeze": readiness_counts["DO_NOT_FREEZE"],
        "blocked": readiness_counts["BLOCKED"],
        "blocked_or_rejected": result["blocked_or_rejected"],
        "excluded_from_readiness_count": result["excluded_from_readiness_count"],
        "effective_ready_count": result["effective_ready_count"],
        "effective_mixed_ready_count": result["effective_mixed_ready_count"],
        "strict_ready_condition_passed": result["strict_ready_condition_passed"],
        "mixed_conservative_condition_passed": result["mixed_conservative_condition_passed"],
        "future_explicit_freeze_recommended": result["future_explicit_freeze_recommended"],
        "base_frozen_dataset_hash": manifest["base_frozen_dataset_hash"],
        "base_manifest_hash": manifest["base_manifest_hash"],
        "frozen_hashes_unchanged": result["frozen_hashes_unchanged"],
        "modifies_frozen_dataset": manifest["modifies_frozen_dataset"],
        "provider_execution_allowed": manifest["provider_execution_allowed"],
        "model_comparison_allowed": manifest["model_comparison_allowed"],
        "network_required": result["network_required"],
        "env_read": result["env_read"],
        "secrets_printed": result["secrets_printed"],
        "providers_executed": result["providers_executed"],
        "model_comparison_run": result["model_comparison_run"],
        "external_superiority_claim_authorized": manifest["external_superiority_claim_authorized"],
        "statistical_claim_authorized": manifest["statistical_claim_authorized"],
        "authorized_claim": "Finitexo Code Matrix v0.4.2 completes the expansion candidate pool required for a future explicit n>=10 freeze, without modifying the v0.4 frozen dataset.",
        "blocked_claims": [
            "v0.4 frozen dataset was expanded",
            "v0.4.2 created frozen tasks",
            "provider superiority demonstrated",
            "Xendris superiority demonstrated",
            "external benchmark performance validated",
            "statistical significance established",
            "production-readiness proven",
            "verified third-party external benchmark established",
        ],
        "final_decision": result["final_decision"],
    }


def build_completion_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.4.2 - Expansion Pool Completion",
            "",
            "## Summary",
            "",
            f"- Current frozen task count: {summary['current_frozen_task_count']}",
            f"- Target frozen task count: {summary['target_frozen_task_count']}",
            f"- Additional ready candidates required: {summary['additional_ready_candidates_required']}",
            f"- Total expansion candidates: {summary['total_expansion_candidates']}",
            f"- Ready for future freeze: {summary['ready_for_future_freeze']}",
            f"- Ready with human review: {summary['ready_with_human_review']}",
            f"- Blocked or rejected: {summary['blocked_or_rejected']}",
            f"- Effective ready count: {summary['effective_ready_count']}",
            f"- Effective mixed ready count: {summary['effective_mixed_ready_count']}",
            f"- Strict ready condition passed: {str(summary['strict_ready_condition_passed']).lower()}",
            f"- Mixed conservative condition passed: {str(summary['mixed_conservative_condition_passed']).lower()}",
            f"- Future explicit freeze recommended: {str(summary['future_explicit_freeze_recommended']).lower()}",
            "",
            "## Base Dataset",
            "",
            f"- Base v0.4 dataset hash: `{summary['base_frozen_dataset_hash']}`",
            f"- Base v0.4 manifest hash: `{summary['base_manifest_hash']}`",
            f"- Frozen hashes unchanged: {str(summary['frozen_hashes_unchanged']).lower()}",
            "",
            "## Boundary",
            "",
            "- v0.4 frozen dataset was not modified.",
            "- No providers were executed.",
            "- No model comparison was run.",
            "- No network access was required.",
            "- No .env file was read.",
            "- No secrets were printed.",
            "- No external superiority claim is authorized.",
            "",
            "## Authorized Claim",
            "",
            summary["authorized_claim"],
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in summary["blocked_claims"]],
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
        ]
    )


def write_completion_artifacts(outdir: Path = OUTDIR, root: Path = ROOT) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    summary = build_completion_summary(root)
    (outdir / "expansion_completion_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (outdir / "expansion_completion_report.md").write_text(build_completion_report(summary), encoding="utf-8")
    return summary
