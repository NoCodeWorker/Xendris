"""Report generation for the v0.4.3 expanded freeze."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .freeze_validator import ROOT, validate_expanded_freeze
from .hash_utils import load_json


OUTDIR = Path("runs/finitexo_code_matrix_v0_4_3_expanded_freeze")


def _task_paths(root: Path) -> list[Path]:
    return sorted((root / "tasks").glob("frozen_task_*.json"))


def build_expanded_freeze_summary(root: Path = ROOT) -> dict[str, Any]:
    manifest = load_json(root / "frozen_dataset_manifest.json")
    hashes = load_json(root / "frozen_dataset_hashes.json")
    tasks = [load_json(path) for path in _task_paths(root)]
    validation = validate_expanded_freeze(root)
    inherited = [task for task in tasks if task["promotion_decision"] == "INHERITED_FROM_V0_4"]
    human_review = [task for task in tasks if task["human_review_status"] == "APPROVED_FOR_FREEZE"]
    promoted = [task for task in tasks if task["promotion_decision"].startswith("PROMOTED_FROM_EXPANSION")]
    return {
        "benchmark_name": manifest["benchmark_name"],
        "benchmark_version": manifest["benchmark_version"],
        "dataset_name": manifest["dataset_name"],
        "dataset_version": manifest["dataset_version"],
        "frozen_task_count": len(tasks),
        "inherited_v0_4_tasks_count": len(inherited),
        "expansion_candidates_promoted_count": len(promoted),
        "human_review_promoted_count": len(human_review),
        "excluded_candidate_count": 6,
        "counts_by_source_origin": dict(Counter(task["source_origin"] for task in tasks)),
        "counts_by_adaptation_type": dict(Counter(task["adaptation_type"] for task in tasks)),
        "counts_by_difficulty": dict(Counter(task["difficulty_estimate"] for task in tasks)),
        "counts_by_contamination_risk": dict(Counter(task["contamination_risk"] for task in tasks)),
        "counts_by_leakage_risk": dict(Counter(task["leakage_risk"] for task in tasks)),
        "dataset_hash": hashes["dataset_hash"],
        "manifest_hash": hashes["manifest_hash"],
        "provider_execution_allowed": manifest["provider_execution_allowed"],
        "model_comparison_allowed": manifest["model_comparison_allowed"],
        "external_superiority_claim_authorized": manifest["external_superiority_claim_authorized"],
        "statistical_claim_authorized": manifest["statistical_claim_authorized"],
        "providers_executed": False,
        "model_comparison_run": False,
        "network_required": False,
        "env_read": False,
        "secrets_printed": False,
        "authorized_claims": manifest["authorized_claims"],
        "blocked_claims": manifest["blocked_claims"],
        "validation_decision": validation["decision"],
        "validation_error_count": validation["error_count"],
        "final_decision": "EXPLICIT_EXPANDED_FREEZE_N10_CREATED_NO_PROVIDER_EXECUTION",
    }


def build_expanded_freeze_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.4.3 - Explicit Expanded Freeze n=10",
            "",
            f"- Frozen task count: {summary['frozen_task_count']}",
            f"- Inherited v0.4 tasks: {summary['inherited_v0_4_tasks_count']}",
            f"- Expansion candidates promoted: {summary['expansion_candidates_promoted_count']}",
            f"- Human-review promoted: {summary['human_review_promoted_count']}",
            f"- Excluded candidates: {summary['excluded_candidate_count']}",
            f"- Dataset hash: `{summary['dataset_hash']}`",
            f"- Manifest hash: `{summary['manifest_hash']}`",
            f"- Validation decision: `{summary['validation_decision']}`",
            "",
            "## Boundary",
            "",
            "- No providers were executed.",
            "- No model comparison was run.",
            "- No network access was required.",
            "- No .env file was read.",
            "- No secrets were printed.",
            "- Original v0.4 frozen dataset was not modified.",
            "- No external superiority claim is authorized.",
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
        ]
    )


def write_expanded_freeze_artifacts(outdir: Path = OUTDIR, root: Path = ROOT) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    summary = build_expanded_freeze_summary(root)
    (outdir / "expanded_freeze_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (outdir / "expanded_freeze_report.md").write_text(build_expanded_freeze_report(summary), encoding="utf-8")
    return summary
