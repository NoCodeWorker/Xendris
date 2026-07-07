import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_4.expansion_completion import (
    build_completion_summary,
    evaluate_completion_policy,
    write_completion_artifacts,
)
from benchmarks.finitexo_code_matrix_v0_4.expansion_intake import (
    ExpansionCandidate,
    validate_expansion_candidate,
)
from benchmarks.finitexo_code_matrix_v0_4.expansion_intake.expansion_types import ExpansionReadiness


ROOT = Path("benchmarks/finitexo_code_matrix_v0_4")
MANIFEST_PATH = ROOT / "expansion_completion_manifest.json"
HASHES_PATH = ROOT / "frozen_dataset_hashes.json"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _candidate(index: str) -> ExpansionCandidate:
    return ExpansionCandidate.from_dict(_load_json(ROOT / "expansion_candidates" / f"expansion_candidate_{index}.json"))


def test_expansion_completion_package_and_manifest_exist():
    assert (ROOT / "expansion_completion").exists()
    assert MANIFEST_PATH.exists()


def test_manifest_declares_v0_4_2_and_no_dataset_modification():
    manifest = _load_json(MANIFEST_PATH)
    assert manifest["expansion_completion_version"] == "v0.4.2"
    assert manifest["modifies_frozen_dataset"] is False
    assert manifest["future_freeze_requires_explicit_version_bump"] is True


def test_manifest_blocks_runtime_and_claims():
    manifest = _load_json(MANIFEST_PATH)
    assert manifest["provider_execution_allowed"] is False
    assert manifest["model_comparison_allowed"] is False
    assert manifest["network_required"] is False
    assert manifest["external_superiority_claim_authorized"] is False
    assert manifest["statistical_claim_authorized"] is False


def test_base_frozen_hashes_match_v0_4_known_hashes():
    manifest = _load_json(MANIFEST_PATH)
    hashes = _load_json(HASHES_PATH)
    assert manifest["base_frozen_dataset_hash"] == hashes["dataset_hash"]
    assert manifest["base_manifest_hash"] == hashes["manifest_hash"]
    assert manifest["base_frozen_dataset_hash"] == "0ed903b013bff8650ce30030863d069a6cdd745d42964ba85082389d836cdb17"
    assert manifest["base_manifest_hash"] == "981406f6aa7a736cb64e698742075c4f05fbafcdf7e79e96a97c781224984298"


def test_expansion_candidate_pool_includes_previous_and_new_candidates():
    paths = sorted((ROOT / "expansion_candidates").glob("expansion_candidate_*.json"))
    names = {path.name for path in paths}
    assert "expansion_candidate_001.json" in names
    assert "expansion_candidate_010.json" in names
    assert "expansion_candidate_011.json" in names
    assert "expansion_candidate_016.json" in names
    assert len(paths) == 16


def test_new_ready_candidates_pass_v0_4_1_validation_rules():
    for index in ("011", "012", "013", "014"):
        candidate = validate_expansion_candidate(_candidate(index))
        assert candidate.expansion_readiness == ExpansionReadiness.READY_FOR_FUTURE_FREEZE


def test_human_review_candidate_does_not_auto_freeze():
    candidate = validate_expansion_candidate(_candidate("015"))
    assert candidate.expansion_readiness == ExpansionReadiness.READY_WITH_HUMAN_REVIEW


def test_blocked_or_rejected_candidates_are_excluded_from_readiness_count():
    result = evaluate_completion_policy(ROOT)
    excluded = set(result["excluded_from_readiness_count"])
    assert "fcm_v0_4_1_candidate_006" in excluded
    assert "fcm_v0_4_1_candidate_007" in excluded
    assert "fcm_v0_4_1_candidate_008" in excluded
    assert "fcm_v0_4_1_candidate_009" in excluded
    assert "fcm_v0_4_1_candidate_010" in excluded
    assert "fcm_v0_4_2_candidate_016" in excluded


def test_network_secret_and_provider_candidates_are_excluded():
    candidate = validate_expansion_candidate(_candidate("008"))
    assert candidate.expansion_readiness == ExpansionReadiness.BLOCKED
    assert "network_required" in candidate.rejection_reasons
    assert "secrets_required" in candidate.rejection_reasons
    assert "provider_execution_required" in candidate.rejection_reasons


def test_missing_provenance_and_hash_candidates_are_excluded():
    missing_provenance = validate_expansion_candidate(_candidate("006"))
    missing_hash = validate_expansion_candidate(_candidate("016"))
    assert missing_provenance.expansion_readiness == ExpansionReadiness.DO_NOT_FREEZE
    assert "missing_provenance" in missing_provenance.rejection_reasons
    assert missing_hash.expansion_readiness == ExpansionReadiness.DO_NOT_FREEZE
    assert "missing_proposed_task_hash" in missing_hash.rejection_reasons


def test_mutated_and_synthetic_candidates_cannot_count_as_external_ready():
    mutated = validate_expansion_candidate(_candidate("009"))
    synthetic = validate_expansion_candidate(_candidate("010"))
    assert mutated.expansion_readiness == ExpansionReadiness.DO_NOT_FREEZE
    assert synthetic.expansion_readiness == ExpansionReadiness.DO_NOT_FREEZE
    assert "mutated_fixture_cannot_be_presented_as_external" in mutated.rejection_reasons
    assert "synthetic_local_cannot_be_presented_as_external" in synthetic.rejection_reasons


def test_strict_and_mixed_completion_conditions_are_evaluated():
    summary = build_completion_summary(ROOT)
    assert summary["ready_for_future_freeze"] == 7
    assert summary["ready_with_human_review"] == 3
    assert summary["strict_ready_condition_passed"] is False
    assert summary["mixed_conservative_condition_passed"] is True
    assert summary["future_explicit_freeze_recommended"] is True


def test_completion_report_builder_produces_json_and_markdown(tmp_path):
    summary = write_completion_artifacts(tmp_path, ROOT)
    assert summary["final_decision"] == "EXPANSION_POOL_COMPLETED_READY_FOR_EXPLICIT_FREEZE"
    assert (tmp_path / "expansion_completion_summary.json").exists()
    assert (tmp_path / "expansion_completion_report.md").exists()
    report = (tmp_path / "expansion_completion_report.md").read_text(encoding="utf-8")
    assert "v0.4 frozen dataset was not modified" in report
    assert "No providers were executed" in report


def test_v0_4_tasks_provenance_and_hashes_remain_unchanged():
    hashes = _load_json(HASHES_PATH)
    assert hashes["dataset_hash"] == "0ed903b013bff8650ce30030863d069a6cdd745d42964ba85082389d836cdb17"
    assert len(sorted((ROOT / "tasks").glob("frozen_task_*.json"))) == 2
    assert len(sorted((ROOT / "provenance").glob("provenance_frozen_task_*.json"))) == 2


def test_no_provider_execution_is_required():
    summary = build_completion_summary(ROOT)
    assert summary["providers_executed"] is False
    assert summary["model_comparison_run"] is False
    assert summary["network_required"] is False
    assert summary["env_read"] is False
    assert summary["secrets_printed"] is False
    assert summary["external_superiority_claim_authorized"] is False


def test_status_document_exists_and_blocks_overclaims():
    path = Path("docs/status/FINITEXO_CODE_MATRIX_V0_4_2_EXPANSION_POOL_COMPLETION.md")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "EXPANSION_POOL_COMPLETED_READY_FOR_EXPLICIT_FREEZE" in text
    assert "v0.4 frozen dataset was expanded" in text
