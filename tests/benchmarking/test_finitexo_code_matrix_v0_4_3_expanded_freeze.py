import copy
import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_4_3.validation.freeze_validator import (
    recompute_hashes,
    validate_expanded_freeze,
)
from benchmarks.finitexo_code_matrix_v0_4_3.validation.hash_utils import hash_provenance, hash_task
from benchmarks.finitexo_code_matrix_v0_4_3.validation.report_builder import write_expanded_freeze_artifacts


ROOT = Path("benchmarks/finitexo_code_matrix_v0_4_3")
V04_ROOT = Path("benchmarks/finitexo_code_matrix_v0_4")


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _task_paths():
    return sorted((ROOT / "tasks").glob("frozen_task_*.json"))


def test_v0_4_3_dataset_directory_and_manifest_exist():
    assert ROOT.exists()
    assert (ROOT / "frozen_dataset_manifest.json").exists()


def test_manifest_version_and_frozen_status():
    manifest = _load_json(ROOT / "frozen_dataset_manifest.json")
    assert manifest["benchmark_version"] == "v0.4.3"
    assert manifest["dataset_status"] == "FROZEN"
    assert manifest["frozen_task_count"] == 10


def test_exactly_10_frozen_tasks_exist():
    assert len(_task_paths()) == 10


def test_base_v0_4_hashes_are_referenced_and_original_files_unchanged():
    manifest = _load_json(ROOT / "frozen_dataset_manifest.json")
    v04_hashes = _load_json(V04_ROOT / "frozen_dataset_hashes.json")
    assert manifest["base_v0_4_dataset_hash"] == v04_hashes["dataset_hash"]
    assert manifest["base_v0_4_manifest_hash"] == v04_hashes["manifest_hash"]
    assert v04_hashes["dataset_hash"] == "0ed903b013bff8650ce30030863d069a6cdd745d42964ba85082389d836cdb17"
    assert len(sorted((V04_ROOT / "tasks").glob("frozen_task_*.json"))) == 2


def test_manifest_blocks_execution_comparison_and_claims():
    manifest = _load_json(ROOT / "frozen_dataset_manifest.json")
    assert manifest["provider_execution_allowed"] is False
    assert manifest["model_comparison_allowed"] is False
    assert manifest["external_superiority_claim_authorized"] is False
    assert manifest["statistical_claim_authorized"] is False


def test_every_frozen_task_has_required_fields_and_provenance():
    required = {
        "task_id",
        "task_version",
        "title",
        "prompt",
        "expected_behavior",
        "validation_oracle",
        "allowed_files",
        "forbidden_files",
        "content_hash",
        "provenance_ref",
        "human_review_status",
    }
    for path in _task_paths():
        task = _load_json(path)
        assert required.issubset(task)
        assert (ROOT / task["provenance_ref"]).exists()


def test_task_hashes_match_current_content():
    recorded = _load_json(ROOT / "frozen_dataset_hashes.json")
    for path in _task_paths():
        task = _load_json(path)
        assert task["content_hash"] == hash_task(task)
        assert recorded["task_hashes"][path.name] == hash_task(task)


def test_provenance_hashes_match_current_content():
    recorded = _load_json(ROOT / "frozen_dataset_hashes.json")
    for path in sorted((ROOT / "provenance").glob("provenance_frozen_task_*.json")):
        provenance = _load_json(path)
        assert recorded["provenance_hashes"][path.name] == hash_provenance(provenance)


def test_human_review_promoted_candidate_has_authorization_record():
    task = _load_json(ROOT / "tasks" / "frozen_task_010.json")
    provenance = _load_json(ROOT / task["provenance_ref"])
    assert task["human_review_status"] == "APPROVED_FOR_FREEZE"
    assert provenance["human_review_ref"] == "human_review/human_review_candidate_004.json"
    review = _load_json(ROOT / provenance["human_review_ref"])
    assert review["review_status"] == "APPROVED_FOR_FREEZE"
    assert review["does_not_authorize_provider_claims"] is True
    assert review["does_not_authorize_superiority_claims"] is True


def test_no_blocked_rejected_or_runtime_required_candidates_are_frozen():
    frozen_refs = {_load_json(path)["expansion_candidate_ref"] for path in _task_paths()}
    blocked_refs = {
        "benchmarks/finitexo_code_matrix_v0_4/expansion_candidates/expansion_candidate_006.json",
        "benchmarks/finitexo_code_matrix_v0_4/expansion_candidates/expansion_candidate_007.json",
        "benchmarks/finitexo_code_matrix_v0_4/expansion_candidates/expansion_candidate_008.json",
        "benchmarks/finitexo_code_matrix_v0_4/expansion_candidates/expansion_candidate_009.json",
        "benchmarks/finitexo_code_matrix_v0_4/expansion_candidates/expansion_candidate_010.json",
        "benchmarks/finitexo_code_matrix_v0_4/expansion_candidates/expansion_candidate_016.json",
    }
    assert frozen_refs.isdisjoint(blocked_refs)
    for path in _task_paths():
        task = _load_json(path)
        assert task["provider_execution_required"] is False
        assert task["network_required"] is False
        assert task["secrets_required"] is False
        assert task["contamination_risk"] != "BLOCKED"
        assert task["leakage_risk"] != "BLOCKED"


def test_dataset_hash_is_stable_and_memory_mutation_changes_task_hash():
    first = recompute_hashes(ROOT)["dataset_hash"]
    second = recompute_hashes(ROOT)["dataset_hash"]
    assert first == second
    task = _load_json(_task_paths()[0])
    mutated = copy.deepcopy(task)
    mutated["prompt"] = mutated["prompt"] + " mutated"
    assert hash_task(mutated) != hash_task(task)


def test_validator_accepts_current_dataset():
    result = validate_expanded_freeze(ROOT)
    assert result["decision"] == "READY"
    assert result["error_count"] == 0
    assert result["task_count"] == 10


def test_report_builder_produces_json_summary_and_markdown(tmp_path):
    summary = write_expanded_freeze_artifacts(tmp_path, ROOT)
    assert summary["final_decision"] == "EXPLICIT_EXPANDED_FREEZE_N10_CREATED_NO_PROVIDER_EXECUTION"
    assert summary["frozen_task_count"] == 10
    assert summary["human_review_promoted_count"] == 1
    assert (tmp_path / "expanded_freeze_summary.json").exists()
    assert (tmp_path / "expanded_freeze_report.md").exists()
    report = (tmp_path / "expanded_freeze_report.md").read_text(encoding="utf-8")
    assert "No providers were executed" in report


def test_no_provider_execution_is_required(tmp_path):
    summary = write_expanded_freeze_artifacts(tmp_path, ROOT)
    assert summary["providers_executed"] is False
    assert summary["model_comparison_run"] is False
    assert summary["network_required"] is False
    assert summary["env_read"] is False
    assert summary["secrets_printed"] is False
    assert summary["external_superiority_claim_authorized"] is False


def test_status_document_exists_and_blocks_claims():
    path = Path("docs/status/FINITEXO_CODE_MATRIX_V0_4_3_EXPLICIT_EXPANDED_FREEZE_N10.md")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "EXPLICIT_EXPANDED_FREEZE_N10_CREATED_NO_PROVIDER_EXECUTION" in text
    assert "provider superiority demonstrated" in text
