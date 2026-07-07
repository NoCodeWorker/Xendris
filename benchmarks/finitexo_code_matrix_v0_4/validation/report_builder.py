"""Report generation for the v0.4 frozen external/adapted dataset."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .freeze_validator import ROOT, validate_frozen_dataset
from .hash_utils import load_json


def _task_paths(root: Path) -> list[Path]:
    return sorted((root / "tasks").glob("frozen_task_*.json"))


def build_frozen_dataset_summary(root: Path = ROOT) -> dict[str, Any]:
    manifest = load_json(root / "frozen_dataset_manifest.json")
    hashes = load_json(root / "frozen_dataset_hashes.json")
    tasks = [load_json(path) for path in _task_paths(root)]
    validation = validate_frozen_dataset(root)

    return {
        "benchmark_name": manifest["benchmark_name"],
        "benchmark_version": manifest["benchmark_version"],
        "dataset_name": manifest["dataset_name"],
        "dataset_version": manifest["dataset_version"],
        "dataset_status": manifest["dataset_status"],
        "dataset_type": manifest["dataset_type"],
        "dataset_externality_label": manifest.get("dataset_externality_label"),
        "frozen_task_count": len(tasks),
        "minimum_task_target": manifest.get("minimum_task_target"),
        "minimum_task_target_met": len(tasks) >= int(manifest.get("minimum_task_target", 0)),
        "minimum_task_target_notes": manifest.get("minimum_task_target_notes"),
        "counts_by_source_origin": dict(Counter(task["source_origin"] for task in tasks)),
        "counts_by_adaptation_type": dict(Counter(task["adaptation_type"] for task in tasks)),
        "counts_by_difficulty": dict(Counter(task["difficulty_estimate"] for task in tasks)),
        "counts_by_contamination_risk": dict(Counter(task["contamination_risk"] for task in tasks)),
        "counts_by_leakage_risk": dict(Counter(task["leakage_risk"] for task in tasks)),
        "provider_execution_allowed": manifest["provider_execution_allowed"],
        "model_comparison_allowed": manifest["model_comparison_allowed"],
        "network_required": any(task["network_required"] for task in tasks),
        "secrets_required": any(task["secrets_required"] for task in tasks),
        "dataset_hash": hashes["dataset_hash"],
        "manifest_hash": hashes["manifest_hash"],
        "policy_boundaries": manifest["policy_boundaries"],
        "authorized_claims": manifest["authorized_claims"],
        "blocked_claims": manifest["blocked_claims"],
        "validation_decision": validation["decision"],
        "validation_blocker_count": validation["blocker_count"],
        "providers_executed": False,
        "env_read": False,
        "secrets_printed": False,
        "final_decision": "FROZEN_EXTERNAL_ADAPTED_DATASET_CREATED_NO_PROVIDER_EXECUTION",
    }


def build_frozen_dataset_report(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.4 - Frozen External/Adapted Dataset",
            "",
            "## Summary",
            "",
            f"- Dataset: {summary['dataset_name']}",
            f"- Version: {summary['dataset_version']}",
            f"- Frozen task count: {summary['frozen_task_count']}",
            f"- Dataset hash: `{summary['dataset_hash']}`",
            f"- Manifest hash: `{summary['manifest_hash']}`",
            f"- Validation decision: `{summary['validation_decision']}`",
            "",
            "## Counts",
            "",
            f"- Source origin: `{summary['counts_by_source_origin']}`",
            f"- Adaptation type: `{summary['counts_by_adaptation_type']}`",
            f"- Difficulty: `{summary['counts_by_difficulty']}`",
            f"- Contamination risk: `{summary['counts_by_contamination_risk']}`",
            f"- Leakage risk: `{summary['counts_by_leakage_risk']}`",
            "",
            "## Execution Boundary",
            "",
            "- Providers executed: false",
            f"- Provider execution allowed: {str(summary['provider_execution_allowed']).lower()}",
            f"- Model comparison allowed: {str(summary['model_comparison_allowed']).lower()}",
            f"- Network required: {str(summary['network_required']).lower()}",
            f"- Secrets required: {str(summary['secrets_required']).lower()}",
            "",
            "## Minimum Task Target",
            "",
            f"- Target: {summary['minimum_task_target']}",
            f"- Met: {str(summary['minimum_task_target_met']).lower()}",
            f"- Notes: {summary['minimum_task_target_notes']}",
            "",
            "## Authorized Claims",
            "",
            *[f"- {claim}" for claim in summary["authorized_claims"]],
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in summary["blocked_claims"]],
            "",
            "## Policy Boundaries",
            "",
            "```txt",
            *summary["policy_boundaries"],
            "```",
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
        ]
    )


def write_frozen_dataset_artifacts(
    outdir: Path = Path("runs/finitexo_code_matrix_v0_4_freeze"),
    root: Path = ROOT,
) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    summary = build_frozen_dataset_summary(root)
    (outdir / "frozen_dataset_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (outdir / "frozen_dataset_report.md").write_text(build_frozen_dataset_report(summary), encoding="utf-8")
    return summary
