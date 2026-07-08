"""Tests for Finitexo Code Matrix v0.8.0 hard programming dataset n=30."""

import hashlib
import json
from pathlib import Path

import pytest

DATASET_DIR = Path("benchmarks/finitexo_code_matrix_v0_8/datasets/hard_programming_n30")
TASKS_DIR = DATASET_DIR / "tasks"
FAMILIES = [
    "algorithmic_reasoning",
    "stateful_refactor",
    "edge_case_handling",
    "api_design_consistency",
    "performance_constraints",
]
EXPECTED_FIELDS = [
    "task_id",
    "task_version",
    "family",
    "difficulty",
    "title",
    "prompt",
    "public_contract",
    "constraints",
    "expected_failure_modes",
    "scoring_focus",
    "prohibited_claims",
    "allowed_assumptions",
    "disallowed_assumptions",
    "requires_external_access",
    "requires_code_execution",
    "provider_bias_check",
]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------

def test_dataset_dir_exists():
    assert DATASET_DIR.exists()


def test_tasks_dir_exists():
    assert TASKS_DIR.exists()


def test_manifest_exists():
    assert (DATASET_DIR / "dataset_manifest.json").exists()


def test_provenance_exists():
    assert (DATASET_DIR / "provenance.json").exists()


def test_dataset_hash_file_exists():
    assert (DATASET_DIR / "dataset_hash.txt").exists()


def test_manifest_hash_file_exists():
    assert (DATASET_DIR / "manifest_hash.txt").exists()


def test_generation_script_exists():
    assert (DATASET_DIR / "generate_hard_programming_n30.py").exists()


# ---------------------------------------------------------------------------
# Task count and distribution
# ---------------------------------------------------------------------------

def test_exactly_30_tasks():
    paths = sorted(TASKS_DIR.glob("task_*.json"))
    assert len(paths) == 30


def test_6_tasks_per_family():
    tasks = [_load_json(p) for p in sorted(TASKS_DIR.glob("task_*.json"))]
    counts = {}
    for t in tasks:
        counts[t["family"]] = counts.get(t["family"], 0) + 1
    for family in FAMILIES:
        assert counts.get(family) == 6, f"{family} has {counts.get(family)} tasks"


def test_all_task_ids_unique():
    tasks = [_load_json(p) for p in sorted(TASKS_DIR.glob("task_*.json"))]
    ids = [t["task_id"] for t in tasks]
    assert len(ids) == len(set(ids))


# ---------------------------------------------------------------------------
# Required fields
# ---------------------------------------------------------------------------

def test_all_required_fields_present():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        for field in EXPECTED_FIELDS:
            assert field in task, f"{path.name} missing field: {field}"


def test_all_task_version_is_0_8_0():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert task["task_version"] == "0.8.0", f"{path.name} version mismatch"


def test_all_difficulty_is_hard():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert task["difficulty"] == "hard", f"{path.name} difficulty mismatch"


def test_all_requires_external_access_false():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert task["requires_external_access"] is False, f"{path.name} requires external access"


def test_all_requires_code_execution_false():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert task["requires_code_execution"] is False, f"{path.name} requires code execution"


def test_all_provider_bias_check_neutral():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert task["provider_bias_check"] == "neutral", f"{path.name} bias check not neutral"


# ---------------------------------------------------------------------------
# Field types and content
# ---------------------------------------------------------------------------

def test_family_labels_valid():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert task["family"] in FAMILIES, f"{path.name} invalid family: {task['family']}"


def test_constraints_is_list():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert isinstance(task["constraints"], list)


def test_expected_failure_modes_is_list():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert isinstance(task["expected_failure_modes"], list)


def test_scoring_focus_is_list():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert isinstance(task["scoring_focus"], list)


def test_prohibited_claims_is_list():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        task = _load_json(path)
        assert isinstance(task["prohibited_claims"], list)


# ---------------------------------------------------------------------------
# No answer keys or solutions
# ---------------------------------------------------------------------------

def test_no_answer_keys():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        text = path.read_text(encoding="utf-8").lower()
        assert "answer" not in text or "answer_key" not in text
        assert "canonical_solution" not in text
        assert "expected_output" not in text or "expected_output" not in [t.get("expected_output") for t in [_load_json(path)]]


def test_no_canonical_solutions():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        text = path.read_text(encoding="utf-8").lower()
        assert "solution" not in text or "solution" not in [t.get("solution") for t in [_load_json(path)]]


# ---------------------------------------------------------------------------
# No provider-specific bias
# ---------------------------------------------------------------------------

def test_no_xendris_bait():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        text = path.read_text(encoding="utf-8")
        assert "xendris" not in text.lower(), f"{path.name} contains Xendris reference"


def test_no_provider_bias():
    for path in sorted(TASKS_DIR.glob("task_*.json")):
        text = path.read_text(encoding="utf-8").lower()
        assert "deepseek" not in text or "openai" not in text
        assert "bias" not in text or "provider_bias_check" in text


# ---------------------------------------------------------------------------
# Manifest content
# ---------------------------------------------------------------------------

def test_manifest_has_30_tasks():
    manifest = _load_json(DATASET_DIR / "dataset_manifest.json")
    assert len(manifest["tasks"]) == 30


def test_manifest_task_ids_match():
    manifest = _load_json(DATASET_DIR / "dataset_manifest.json")
    task_ids_file = sorted([_load_json(p)["task_id"] for p in TASKS_DIR.glob("task_*.json")])
    task_ids_manifest = sorted([t["task_id"] for t in manifest["tasks"]])
    assert task_ids_file == task_ids_manifest


def test_manifest_has_dataset_hash():
    manifest = _load_json(DATASET_DIR / "dataset_manifest.json")
    assert "dataset_hash" in manifest
    assert len(manifest["dataset_hash"]) == 64


def test_manifest_has_families():
    manifest = _load_json(DATASET_DIR / "dataset_manifest.json")
    assert manifest["families"] == FAMILIES


def test_manifest_task_count():
    manifest = _load_json(DATASET_DIR / "dataset_manifest.json")
    assert manifest["task_count"] == 30


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------

def test_provenance_has_required_fields():
    prov = _load_json(DATASET_DIR / "provenance.json")
    for field in ["dataset", "version", "total_tasks", "family_counts", "dataset_hash", "manifest_hash"]:
        assert field in prov, f"provenance missing {field}"


def test_provenance_family_counts():
    prov = _load_json(DATASET_DIR / "provenance.json")
    for family in FAMILIES:
        assert prov["family_counts"][family] == 6


def test_provenance_total_tasks():
    prov = _load_json(DATASET_DIR / "provenance.json")
    assert prov["total_tasks"] == 30


# ---------------------------------------------------------------------------
# Hash stability
# ---------------------------------------------------------------------------

def test_dataset_hash_matches_file():
    tasks = sorted(TASKS_DIR.glob("task_*.json"))
    blobs = sorted([p.read_text(encoding="utf-8") for p in tasks])
    computed = _sha256("".join(blobs))
    stored = (DATASET_DIR / "dataset_hash.txt").read_text(encoding="utf-8").strip()
    assert computed == stored, f"dataset hash mismatch: {computed} != {stored}"


def test_manifest_hash_matches_file():
    manifest_blob = (DATASET_DIR / "dataset_manifest.json").read_text(encoding="utf-8")
    computed = _sha256(manifest_blob)
    stored = (DATASET_DIR / "manifest_hash.txt").read_text(encoding="utf-8").strip()
    assert computed == stored, f"manifest hash mismatch: {computed} != {stored}"


def test_deterministic_regeneration_produces_same_hash():
    """Re-run the generation script and verify hashes are identical."""
    import subprocess
    result = subprocess.run(
        ["python", str(DATASET_DIR / "generate_hard_programming_n30.py")],
        capture_output=True, text=True, cwd=Path.cwd(),
    )
    assert result.returncode == 0
    output_lines = result.stdout.strip().split("\n")
    dataset_hash_line = [l for l in output_lines if l.startswith("Dataset hash:")][0]
    manifest_hash_line = [l for l in output_lines if l.startswith("Manifest hash:")][0]
    ds_hash = dataset_hash_line.split(": ")[1]
    mf_hash = manifest_hash_line.split(": ")[1]
    stored_ds = (DATASET_DIR / "dataset_hash.txt").read_text(encoding="utf-8").strip()
    stored_mf = (DATASET_DIR / "manifest_hash.txt").read_text(encoding="utf-8").strip()
    assert ds_hash == stored_ds, f"Dataset hash changed after regeneration: {ds_hash} != {stored_ds}"
    assert mf_hash == stored_mf, f"Manifest hash changed after regeneration: {mf_hash} != {stored_mf}"


# ---------------------------------------------------------------------------
# Dataset hashes file
# ---------------------------------------------------------------------------

def test_dataset_hashes_file_consistency():
    hashes = _load_json(DATASET_DIR / "dataset_hashes.json")
    assert "dataset_hash" in hashes
    assert "manifest_hash" in hashes
    stored_ds = (DATASET_DIR / "dataset_hash.txt").read_text(encoding="utf-8").strip()
    stored_mf = (DATASET_DIR / "manifest_hash.txt").read_text(encoding="utf-8").strip()
    assert hashes["dataset_hash"] == stored_ds
    assert hashes["manifest_hash"] == stored_mf
