from __future__ import annotations

import json
import os
from pathlib import Path

from xendris.benchmarking.agentic_programming.types import TaskSample


DATASET_MANIFEST = "dataset.json"
FIXTURES_DIR = "fixtures"


def _resolve_fixture_dir(dataset_path: str, sample_id: str) -> str:
    """Resolve fixture directory from sample_id (e.g. AP-002 -> task_002)."""
    num_part = sample_id.split("-")[1]
    return os.path.join(dataset_path, FIXTURES_DIR, f"task_{num_part}")


def load_dataset(dataset_path: str) -> list[TaskSample]:
    manifest_path = os.path.join(dataset_path, DATASET_MANIFEST)
    if not os.path.isfile(manifest_path):
        manifest_path = os.path.join(dataset_path, "..", DATASET_MANIFEST)

    if not os.path.isfile(manifest_path):
        manifest_path = os.path.join(dataset_path, "v0_1", DATASET_MANIFEST)

    if not os.path.isfile(manifest_path):
        raise FileNotFoundError(
            f"dataset.json not found under {dataset_path}. "
            f"Searched at: {os.path.join(dataset_path, DATASET_MANIFEST)}"
        )

    with open(manifest_path, encoding="utf-8") as f:
        raw = json.load(f)

    items: list[TaskSample] = []
    for entry in raw.get("samples", raw if isinstance(raw, list) else []):
        sample_id = entry["sample_id"]
        fixture_dir = _resolve_fixture_dir(dataset_path, sample_id)

        items.append(
            TaskSample(
                sample_id=sample_id,
                task_type=entry["task_type"],
                category=entry["category"],
                issue_description=entry["issue_description"],
                allowed_files=tuple(entry["allowed_files"]),
                forbidden_files=tuple(entry["forbidden_files"]),
                visible_test_command=entry["visible_test_command"],
                hidden_test_command=entry["hidden_test_command"],
                success_criteria=entry["success_criteria"],
                risk_level=entry["risk_level"],
                max_iterations=entry["max_iterations"],
                expected_public_api=tuple(entry["expected_public_api"]),
                disallowed_dependencies=tuple(entry["disallowed_dependencies"]),
                fixture_dir=fixture_dir,
            )
        )

    return items


def get_repo_path(task: TaskSample) -> str:
    return os.path.join(task.fixture_dir, "repo")


def get_manifest_path(task: TaskSample) -> str:
    return os.path.join(task.fixture_dir, "manifest.json")


def validate_fixture(task: TaskSample) -> list[str]:
    errors: list[str] = []
    repo_path = get_repo_path(task)
    if not os.path.isdir(repo_path):
        errors.append(f"Missing repo directory: {repo_path}")
        return errors

    manifest_path = get_manifest_path(task)
    if not os.path.isfile(manifest_path):
        errors.append(f"Missing manifest: {manifest_path}")

    src_dir = os.path.join(repo_path, "src")
    tests_dir = os.path.join(repo_path, "tests")
    if not os.path.isdir(src_dir):
        errors.append(f"Missing src directory: {src_dir}")
    if not os.path.isdir(tests_dir):
        errors.append(f"Missing tests directory: {tests_dir}")

    return errors
