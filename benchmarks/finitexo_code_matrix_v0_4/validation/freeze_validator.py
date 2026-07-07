"""Deterministic frozen dataset validation for Finitexo Code Matrix v0.4."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .freeze_types import FreezeDecision, FreezeIssue, FreezeIssueSeverity
from .hash_utils import hash_manifest, hash_provenance, hash_task, load_json, stable_json_hash
from .manifest_validator import validate_manifest
from .provenance_validator import validate_provenance


ROOT = Path("benchmarks/finitexo_code_matrix_v0_4")


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
    "provider_execution_required",
    "network_required",
    "secrets_required",
    "external_superiority_claim_authorized",
)


def _task_paths(root: Path) -> list[Path]:
    return sorted((root / "tasks").glob("frozen_task_*.json"))


def _provenance_path(root: Path, task: dict[str, Any]) -> Path:
    return root / task["provenance_ref"]


def recompute_dataset_hashes(root: Path = ROOT) -> dict[str, Any]:
    manifest = load_json(root / "frozen_dataset_manifest.json")
    task_hashes: dict[str, str] = {}
    provenance_hashes: dict[str, str] = {}

    for task_path in _task_paths(root):
        task = load_json(task_path)
        task_hashes[task_path.name] = hash_task(task)
        provenance_path = _provenance_path(root, task)
        provenance_hashes[provenance_path.name] = hash_provenance(load_json(provenance_path))

    manifest_hash = hash_manifest(manifest)
    dataset_hash = stable_json_hash(
        {
            "benchmark_version": manifest["benchmark_version"],
            "dataset_version": manifest["dataset_version"],
            "manifest_hash": manifest_hash,
            "task_hashes": task_hashes,
            "provenance_hashes": provenance_hashes,
        }
    )
    return {
        "dataset_hash": dataset_hash,
        "manifest_hash": manifest_hash,
        "task_hashes": task_hashes,
        "provenance_hashes": provenance_hashes,
    }


def validate_frozen_dataset(root: Path = ROOT) -> dict[str, Any]:
    issues: list[FreezeIssue] = []
    manifest = load_json(root / "frozen_dataset_manifest.json")
    recorded_hashes = load_json(root / "frozen_dataset_hashes.json")
    recomputed = recompute_dataset_hashes(root)

    issues.extend(validate_manifest(manifest))

    for task_path in _task_paths(root):
        task = load_json(task_path)
        for field in REQUIRED_TASK_FIELDS:
            if field not in task:
                issues.append(
                    FreezeIssue(
                        code=f"task_missing_{field}",
                        severity=FreezeIssueSeverity.BLOCKER,
                        message=f"{task_path.name} is missing {field!r}.",
                    )
                )
        current_task_hash = hash_task(task)
        if task.get("content_hash") != current_task_hash:
            issues.append(
                FreezeIssue(
                    code="task_content_hash_mismatch",
                    severity=FreezeIssueSeverity.BLOCKER,
                    message=f"{task_path.name} content_hash does not match current content.",
                )
            )
        if task.get("provider_execution_required") is not False:
            issues.append(FreezeIssue("task_requires_provider_execution", FreezeIssueSeverity.BLOCKER, task_path.name))
        if task.get("network_required") is not False:
            issues.append(FreezeIssue("task_requires_network", FreezeIssueSeverity.BLOCKER, task_path.name))
        if task.get("secrets_required") is not False:
            issues.append(FreezeIssue("task_requires_secrets", FreezeIssueSeverity.BLOCKER, task_path.name))
        if task.get("external_superiority_claim_authorized") is not False:
            issues.append(FreezeIssue("task_authorizes_external_superiority", FreezeIssueSeverity.BLOCKER, task_path.name))
        if task.get("contamination_risk") == "BLOCKED":
            issues.append(FreezeIssue("task_blocked_contamination_risk", FreezeIssueSeverity.BLOCKER, task_path.name))
        if task.get("leakage_risk") == "BLOCKED":
            issues.append(FreezeIssue("task_blocked_leakage_risk", FreezeIssueSeverity.BLOCKER, task_path.name))

        provenance_path = _provenance_path(root, task)
        if not provenance_path.exists():
            issues.append(
                FreezeIssue(
                    code="task_missing_provenance_record",
                    severity=FreezeIssueSeverity.BLOCKER,
                    message=f"{task_path.name} points to missing provenance record.",
                )
            )
        else:
            issues.extend(validate_provenance(load_json(provenance_path), current_task_hash))

    for key in ("dataset_hash", "manifest_hash", "task_hashes", "provenance_hashes"):
        if recorded_hashes.get(key) != recomputed.get(key):
            issues.append(
                FreezeIssue(
                    code=f"frozen_hash_mismatch_{key}",
                    severity=FreezeIssueSeverity.BLOCKER,
                    message=f"Recorded {key} does not match recomputed frozen dataset content.",
                )
            )

    blockers = [issue for issue in issues if issue.severity == FreezeIssueSeverity.BLOCKER]
    return {
        "decision": FreezeDecision.BLOCKED.value if blockers else FreezeDecision.READY.value,
        "issues": [issue.to_dict() for issue in issues],
        "blocker_count": len(blockers),
        "task_count": len(_task_paths(root)),
        **recomputed,
    }
