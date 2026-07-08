"""Deterministic loader for the v0.4.3 frozen n=10 dataset."""

from __future__ import annotations

from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_4_3.validation.freeze_validator import validate_expanded_freeze
from benchmarks.finitexo_code_matrix_v0_4_3.validation.hash_utils import load_json

from .smoke_types import LoadedFrozenDataset


EXPECTED_DATASET_HASH = "a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4"
EXPECTED_MANIFEST_HASH = "6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e"


def load_frozen_dataset(dataset_path: Path = Path("benchmarks/finitexo_code_matrix_v0_4_3")) -> LoadedFrozenDataset:
    validation = validate_expanded_freeze(dataset_path)
    if validation["decision"] != "READY":
        raise ValueError(f"frozen dataset validation failed: {validation['errors']}")
    hashes = load_json(dataset_path / "frozen_dataset_hashes.json")
    if hashes["dataset_hash"] != EXPECTED_DATASET_HASH:
        raise ValueError("dataset hash mismatch")
    if hashes["manifest_hash"] != EXPECTED_MANIFEST_HASH:
        raise ValueError("manifest hash mismatch")
    task_paths = sorted((dataset_path / "tasks").glob("frozen_task_*.json"))
    if len(task_paths) != 10:
        raise ValueError("expected exactly 10 frozen tasks")
    return LoadedFrozenDataset(
        dataset_path=str(dataset_path),
        dataset_version="v0.4.3",
        dataset_hash=hashes["dataset_hash"],
        manifest_hash=hashes["manifest_hash"],
        manifest=load_json(dataset_path / "frozen_dataset_manifest.json"),
        tasks=tuple(load_json(path) for path in task_paths),
        hashes=hashes,
    )
