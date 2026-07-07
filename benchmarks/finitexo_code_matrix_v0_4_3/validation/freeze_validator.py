"""Expanded freeze validator for Finitexo Code Matrix v0.4.3."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .hash_utils import (
    hash_human_review,
    hash_manifest,
    hash_provenance,
    hash_task,
    load_json,
    stable_json_hash,
)
from .manifest_validator import validate_manifest
from .provenance_validator import validate_provenance


ROOT = Path("benchmarks/finitexo_code_matrix_v0_4_3")


REQUIRED_TASK_FIELDS = (
    "task_id",
    "task_version",
    "title",
    "prompt",
    "expected_behavior",
    "visible_tests_description",
    "hidden_tests_description",
    "validation_oracle",
    "allowed_files",
    "forbidden_files",
    "difficulty_estimate",
    "source_origin",
    "adaptation_type",
    "expansion_candidate_ref",
    "acquisition_record_ref",
    "adaptation_record_ref",
    "provenance_ref",
    "contamination_risk",
    "leakage_risk",
    "semantic_preservation_score",
    "structural_change_score",
    "difficulty_shift_score",
    "frozen_at",
    "content_hash",
    "promotion_decision",
    "promotion_notes",
    "human_review_status",
    "provider_execution_required",
    "network_required",
    "secrets_required",
    "external_superiority_claim_authorized",
)


def _task_paths(root: Path) -> list[Path]:
    return sorted((root / "tasks").glob("frozen_task_*.json"))


def recompute_hashes(root: Path = ROOT) -> dict[str, Any]:
    manifest = load_json(root / "frozen_dataset_manifest.json")
    task_hashes: dict[str, str] = {}
    provenance_hashes: dict[str, str] = {}
    human_review_hashes: dict[str, str] = {}
    for task_path in _task_paths(root):
        task = load_json(task_path)
        task_hashes[task_path.name] = hash_task(task)
        provenance_hashes[Path(task["provenance_ref"]).name] = hash_provenance(load_json(root / task["provenance_ref"]))
    for review_path in sorted((root / "human_review").glob("*.json")):
        human_review_hashes[review_path.name] = hash_human_review(load_json(review_path))
    manifest_hash = hash_manifest(manifest)
    dataset_hash = stable_json_hash(
        {
            "benchmark_version": manifest["benchmark_version"],
            "dataset_version": manifest["dataset_version"],
            "human_review_hashes": human_review_hashes,
            "manifest_hash": manifest_hash,
            "provenance_hashes": provenance_hashes,
            "task_hashes": task_hashes,
        }
    )
    return {
        "dataset_hash": dataset_hash,
        "human_review_hashes": human_review_hashes,
        "manifest_hash": manifest_hash,
        "provenance_hashes": provenance_hashes,
        "task_hashes": task_hashes,
    }


def validate_expanded_freeze(root: Path = ROOT) -> dict[str, Any]:
    errors: list[str] = []
    manifest = load_json(root / "frozen_dataset_manifest.json")
    recorded = load_json(root / "frozen_dataset_hashes.json")
    recomputed = recompute_hashes(root)
    task_paths = _task_paths(root)

    errors.extend(validate_manifest(manifest))
    if len(task_paths) != 10:
        errors.append("task_count_not_10")

    for task_path in task_paths:
        task = load_json(task_path)
        for field in REQUIRED_TASK_FIELDS:
            if field not in task:
                errors.append(f"{task_path.name}:missing_{field}")
        task_hash = hash_task(task)
        if task.get("content_hash") != task_hash:
            errors.append(f"{task_path.name}:content_hash_mismatch")
        if task.get("provider_execution_required") is not False:
            errors.append(f"{task_path.name}:provider_execution_required")
        if task.get("network_required") is not False:
            errors.append(f"{task_path.name}:network_required")
        if task.get("secrets_required") is not False:
            errors.append(f"{task_path.name}:secrets_required")
        if task.get("external_superiority_claim_authorized") is not False:
            errors.append(f"{task_path.name}:external_superiority_claim_authorized")
        if task.get("contamination_risk") == "BLOCKED":
            errors.append(f"{task_path.name}:blocked_contamination")
        if task.get("leakage_risk") == "BLOCKED":
            errors.append(f"{task_path.name}:blocked_leakage")
        provenance_path = root / task["provenance_ref"]
        if not provenance_path.exists():
            errors.append(f"{task_path.name}:missing_provenance")
        else:
            provenance = load_json(provenance_path)
            errors.extend([f"{task_path.name}:{error}" for error in validate_provenance(provenance, task_hash)])
            review_ref = provenance.get("human_review_ref")
            if task.get("human_review_status") == "APPROVED_FOR_FREEZE" and not review_ref:
                errors.append(f"{task_path.name}:missing_human_review_ref")
            if review_ref and not (root / review_ref).exists():
                errors.append(f"{task_path.name}:missing_human_review_record")

    for key in ("dataset_hash", "manifest_hash", "task_hashes", "provenance_hashes", "human_review_hashes"):
        if recorded.get(key) != recomputed.get(key):
            errors.append(f"hash_mismatch_{key}")

    return {
        "decision": "READY" if not errors else "BLOCKED",
        "errors": errors,
        "error_count": len(errors),
        "task_count": len(task_paths),
        **recomputed,
    }
