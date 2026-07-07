"""Report artifacts for v0.4.1 expansion intake."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .expansion_batch import load_expansion_candidates, validate_expansion_batch


ROOT = Path("benchmarks/finitexo_code_matrix_v0_4")
OUTDIR = Path("runs/finitexo_code_matrix_v0_4_1_expansion_intake")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_expansion_summary(root: Path = ROOT) -> dict[str, Any]:
    manifest = _load_json(root / "expansion_intake_manifest.json")
    batch = validate_expansion_batch(load_expansion_candidates(root / "expansion_candidates"))
    candidates = batch["candidates"]
    readiness_counts = Counter(candidate["expansion_readiness"] for candidate in candidates)
    future_ready = batch["ready_for_future_freeze"] + batch["ready_with_human_review"]
    return {
        "benchmark_name": manifest["benchmark_name"],
        "base_benchmark_version": manifest["base_benchmark_version"],
        "expansion_intake_version": manifest["expansion_intake_version"],
        "base_frozen_dataset_hash": manifest["base_frozen_dataset_hash"],
        "base_manifest_hash": manifest["base_manifest_hash"],
        "current_frozen_task_count": manifest["base_frozen_task_count"],
        "target_frozen_task_count": manifest["target_frozen_task_count"],
        "additional_candidates_needed": manifest["target_frozen_task_count"] - manifest["base_frozen_task_count"],
        "total_expansion_candidates": len(candidates),
        "ready_for_future_freeze": batch["ready_for_future_freeze"],
        "ready_with_human_review": batch["ready_with_human_review"],
        "needs_more_provenance": readiness_counts["NEEDS_MORE_PROVENANCE"],
        "needs_more_validation": readiness_counts["NEEDS_MORE_VALIDATION"],
        "do_not_freeze": readiness_counts["DO_NOT_FREEZE"],
        "blocked": readiness_counts["BLOCKED"],
        "blocked_or_rejected": batch["blocked_or_rejected"],
        "counts_by_source_class": dict(Counter(candidate["source_origin"] for candidate in candidates)),
        "counts_by_contamination_risk": dict(Counter(candidate["contamination_risk"] for candidate in candidates)),
        "counts_by_leakage_risk": dict(Counter(candidate["leakage_risk"] for candidate in candidates)),
        "counts_by_difficulty_estimate": dict(Counter(candidate["difficulty_estimate"] for candidate in candidates)),
        "diagnostic_mean_expansion_score": batch["diagnostic_mean_expansion_score"],
        "future_v0_4_2_freeze_expansion_recommended": future_ready >= 8,
        "batch_decision": batch["batch_decision"],
        "expansion_modifies_frozen_dataset": manifest["expansion_modifies_frozen_dataset"],
        "provider_execution_allowed": manifest["provider_execution_allowed"],
        "model_comparison_allowed": manifest["model_comparison_allowed"],
        "external_superiority_claim_authorized": manifest["external_superiority_claim_authorized"],
        "statistical_claim_authorized": manifest["statistical_claim_authorized"],
        "providers_executed": False,
        "model_comparison_run": False,
        "network_required": False,
        "env_read": False,
        "secrets_printed": False,
        "authorized_claim": "Finitexo Code Matrix v0.4.1 implements a conservative intake layer for expanding the v0.4 frozen external/adapted candidate dataset.",
        "blocked_claims": [
            "v0.4 frozen dataset was expanded",
            "provider superiority demonstrated",
            "Xendris superiority demonstrated",
            "external benchmark performance validated",
            "statistical significance established",
            "production-readiness proven",
            "verified third-party external benchmark established",
        ],
        "final_decision": "FROZEN_DATASET_EXPANSION_INTAKE_IMPLEMENTED_NO_PROVIDER_EXECUTION",
    }


def build_expansion_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.4.1 - Frozen Dataset Expansion Intake",
            "",
            "## Summary",
            "",
            f"- Current frozen task count: {summary['current_frozen_task_count']}",
            f"- Target frozen task count: {summary['target_frozen_task_count']}",
            f"- Additional candidates needed: {summary['additional_candidates_needed']}",
            f"- Total expansion candidates: {summary['total_expansion_candidates']}",
            f"- Ready for future freeze: {summary['ready_for_future_freeze']}",
            f"- Ready with human review: {summary['ready_with_human_review']}",
            f"- Blocked or rejected: {summary['blocked_or_rejected']}",
            f"- Diagnostic mean expansion score: {summary['diagnostic_mean_expansion_score']}",
            f"- Future v0.4.2 freeze expansion recommended: {str(summary['future_v0_4_2_freeze_expansion_recommended']).lower()}",
            "",
            "## Boundary",
            "",
            "- v0.4 frozen dataset was not modified.",
            "- No providers were executed.",
            "- No model comparison was run.",
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


def write_expansion_intake_artifacts(outdir: Path = OUTDIR, root: Path = ROOT) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    summary = build_expansion_summary(root)
    (outdir / "expansion_intake_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (outdir / "expansion_intake_report.md").write_text(build_expansion_report(summary), encoding="utf-8")
    return summary
