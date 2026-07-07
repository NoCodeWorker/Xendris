import copy
import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_4.validation.freeze_validator import (
    recompute_dataset_hashes,
    validate_frozen_dataset,
)
from benchmarks.finitexo_code_matrix_v0_4.validation.hash_utils import hash_task
from benchmarks.finitexo_code_matrix_v0_4.validation.report_builder import (
    build_frozen_dataset_summary,
    write_frozen_dataset_artifacts,
)


ROOT = Path("benchmarks/finitexo_code_matrix_v0_4")
V03_ROOT = Path("benchmarks/finitexo_code_matrix_v0_3")


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _task_paths():
    return sorted((ROOT / "tasks").glob("frozen_task_*.json"))


def test_v0_4_manifest_exists_and_declares_frozen_dataset():
    manifest = _load_json(ROOT / "frozen_dataset_manifest.json")
    assert manifest["benchmark_version"] == "v0.4"
    assert manifest["dataset_status"] == "FROZEN"
    assert manifest["dataset_type"] == "EXTERNAL_ADAPTED"


def test_manifest_blocks_provider_execution_model_comparison_and_superiority_claims():
    manifest = _load_json(ROOT / "frozen_dataset_manifest.json")
    assert manifest["provider_execution_allowed"] is False
    assert manifest["model_comparison_allowed"] is False
    assert manifest["external_superiority_claim_authorized"] is False
    assert manifest["statistical_claim_authorized"] is False


def test_frozen_tasks_directory_exists_and_records_minimum_target_limitation():
    paths = _task_paths()
    manifest = _load_json(ROOT / "frozen_dataset_manifest.json")
    assert (ROOT / "tasks").exists()
    assert len(paths) == 2
    assert manifest["minimum_task_target"] == 3
    assert manifest["minimum_task_target_met"] is False
    assert "Only two v0.3.3 records were eligible" in manifest["minimum_task_target_notes"]


def test_every_frozen_task_has_required_contract_fields():
    required = {
        "task_id",
        "prompt",
        "expected_behavior",
        "validation_oracle",
        "allowed_files",
        "forbidden_files",
        "content_hash",
        "provenance_ref",
    }
    for path in _task_paths():
        task = _load_json(path)
        assert required.issubset(task)
        assert task["allowed_files"]
        assert task["forbidden_files"]


def test_every_frozen_task_blocks_runtime_sensitive_requirements_and_claims():
    for path in _task_paths():
        task = _load_json(path)
        assert task["provider_execution_required"] is False
        assert task["network_required"] is False
        assert task["secrets_required"] is False
        assert task["external_superiority_claim_authorized"] is False


def test_every_frozen_task_has_provenance_record():
    for path in _task_paths():
        task = _load_json(path)
        provenance_path = ROOT / task["provenance_ref"]
        assert provenance_path.exists()
        provenance = _load_json(provenance_path)
        assert provenance["task_id"] == task["task_id"]


def test_no_frozen_task_has_blocked_contamination_or_leakage_risk():
    for path in _task_paths():
        task = _load_json(path)
        assert task["contamination_risk"] != "BLOCKED"
        assert task["leakage_risk"] != "BLOCKED"


def test_frozen_dataset_hashes_exist_and_match_current_content():
    recorded = _load_json(ROOT / "frozen_dataset_hashes.json")
    recomputed = recompute_dataset_hashes(ROOT)
    assert recorded["hash_algorithm"] == "sha256"
    assert recorded["dataset_hash"] == recomputed["dataset_hash"]
    assert recorded["manifest_hash"] == recomputed["manifest_hash"]
    assert recorded["task_hashes"] == recomputed["task_hashes"]
    assert recorded["provenance_hashes"] == recomputed["provenance_hashes"]


def test_task_hashes_match_current_task_content():
    recorded = _load_json(ROOT / "frozen_dataset_hashes.json")
    for path in _task_paths():
        task = _load_json(path)
        assert task["content_hash"] == hash_task(task)
        assert recorded["task_hashes"][path.name] == hash_task(task)


def test_dataset_hash_is_stable():
    first = recompute_dataset_hashes(ROOT)["dataset_hash"]
    second = recompute_dataset_hashes(ROOT)["dataset_hash"]
    assert first == second


def test_modifying_task_in_memory_changes_computed_hash():
    task = _load_json(_task_paths()[0])
    original_hash = hash_task(task)
    mutated = copy.deepcopy(task)
    mutated["prompt"] = mutated["prompt"] + " Mutated in memory."
    assert hash_task(mutated) != original_hash


def test_validator_accepts_current_frozen_dataset():
    result = validate_frozen_dataset(ROOT)
    assert result["decision"] == "READY"
    assert result["blocker_count"] == 0
    assert result["task_count"] == 2


def test_report_builder_produces_summary_and_markdown(tmp_path):
    summary = write_frozen_dataset_artifacts(tmp_path, ROOT)
    assert summary["final_decision"] == "FROZEN_EXTERNAL_ADAPTED_DATASET_CREATED_NO_PROVIDER_EXECUTION"
    assert summary["providers_executed"] is False
    assert (tmp_path / "frozen_dataset_summary.json").exists()
    assert (tmp_path / "frozen_dataset_report.md").exists()
    report = (tmp_path / "frozen_dataset_report.md").read_text(encoding="utf-8")
    assert "Providers executed: false" in report


def test_summary_records_external_adapted_candidate_boundary():
    summary = build_frozen_dataset_summary(ROOT)
    assert summary["dataset_externality_label"] == "EXTERNAL_ADAPTED_CANDIDATE_FREEZE"
    assert summary["minimum_task_target_met"] is False
    assert "candidate_pool != frozen_benchmark_dataset" in summary["policy_boundaries"]


def test_docs_status_v0_4_document_exists():
    path = Path("docs/status/FINITEXO_CODE_MATRIX_V0_4_FROZEN_EXTERNAL_ADAPTED_DATASET.md")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "FROZEN_EXTERNAL_ADAPTED_DATASET_CREATED_NO_PROVIDER_EXECUTION" in text
    assert "provider superiority demonstrated" in text


def test_v0_3_frozen_dataset_is_not_modified():
    manifest = _load_json(V03_ROOT / "external_dataset_manifest.json")
    assert manifest["dataset_hash"] == "a1b03f0da1c4e051c4b54df46baae8eef65a8c401f7da7ed5c520f9bf2c29907"
    assert manifest["dataset_size"] == 10
    assert len(manifest["task_hashes"]) == 10


def test_no_provider_execution_is_required():
    summary = build_frozen_dataset_summary(ROOT)
    assert summary["provider_execution_allowed"] is False
    assert summary["model_comparison_allowed"] is False
    assert summary["network_required"] is False
    assert summary["secrets_required"] is False
