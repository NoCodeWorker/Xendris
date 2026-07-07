import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_4.expansion_intake import (
    ExpansionCandidate,
    build_expansion_summary,
    load_expansion_candidates,
    validate_expansion_batch,
    validate_expansion_candidate,
    write_expansion_intake_artifacts,
)
from benchmarks.finitexo_code_matrix_v0_4.expansion_intake.expansion_scoring import score_expansion_candidate
from benchmarks.finitexo_code_matrix_v0_4.expansion_intake.expansion_types import (
    ExpansionReadiness,
    FreezeRecommendation,
)


ROOT = Path("benchmarks/finitexo_code_matrix_v0_4")
MANIFEST_PATH = ROOT / "expansion_intake_manifest.json"
BASE_HASH_PATH = ROOT / "frozen_dataset_hashes.json"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _candidate(candidate_id: str) -> ExpansionCandidate:
    path = ROOT / "expansion_candidates" / f"expansion_candidate_{candidate_id}.json"
    return ExpansionCandidate.from_dict(_load_json(path))


def test_expansion_intake_package_and_manifest_exist():
    assert (ROOT / "expansion_intake").exists()
    assert MANIFEST_PATH.exists()


def test_manifest_preserves_base_frozen_dataset_identity():
    manifest = _load_json(MANIFEST_PATH)
    hashes = _load_json(BASE_HASH_PATH)
    assert manifest["base_frozen_dataset_hash"] == hashes["dataset_hash"]
    assert manifest["base_manifest_hash"] == hashes["manifest_hash"]
    assert manifest["base_frozen_task_count"] == 2


def test_manifest_blocks_runtime_and_claims():
    manifest = _load_json(MANIFEST_PATH)
    assert manifest["expansion_modifies_frozen_dataset"] is False
    assert manifest["provider_execution_allowed"] is False
    assert manifest["model_comparison_allowed"] is False
    assert manifest["external_superiority_claim_authorized"] is False
    assert manifest["statistical_claim_authorized"] is False


def test_expansion_candidates_directory_has_at_least_eight_examples():
    paths = sorted((ROOT / "expansion_candidates").glob("expansion_candidate_*.json"))
    assert len(paths) >= 8


def test_ready_candidates_pass_validation():
    for candidate_id in ("001", "002", "003"):
        candidate = validate_expansion_candidate(_candidate(candidate_id))
        assert candidate.expansion_readiness == ExpansionReadiness.READY_FOR_FUTURE_FREEZE
        assert candidate.freeze_recommendation == FreezeRecommendation.RECOMMEND_FOR_V0_4_X_FREEZE


def test_human_review_candidates_do_not_auto_freeze():
    for candidate_id in ("004", "005"):
        candidate = validate_expansion_candidate(_candidate(candidate_id))
        assert candidate.expansion_readiness == ExpansionReadiness.READY_WITH_HUMAN_REVIEW
        assert candidate.freeze_recommendation == FreezeRecommendation.RECOMMEND_WITH_HUMAN_REVIEW


def test_missing_provenance_prevents_ready_status():
    candidate = validate_expansion_candidate(_candidate("006"))
    assert candidate.expansion_readiness == ExpansionReadiness.DO_NOT_FREEZE
    assert "missing_provenance" in candidate.rejection_reasons


def test_high_leakage_risk_blocks_candidate():
    candidate = validate_expansion_candidate(_candidate("007"))
    assert candidate.expansion_readiness == ExpansionReadiness.BLOCKED
    assert "blocked_or_high_leakage_risk" in candidate.rejection_reasons


def test_network_and_secret_required_candidate_is_blocked():
    candidate = validate_expansion_candidate(_candidate("008"))
    assert candidate.expansion_readiness == ExpansionReadiness.BLOCKED
    assert "provider_execution_required" in candidate.rejection_reasons
    assert "network_required" in candidate.rejection_reasons
    assert "secrets_required" in candidate.rejection_reasons


def test_mutated_fixture_cannot_be_presented_as_external():
    candidate = validate_expansion_candidate(_candidate("009"))
    assert candidate.expansion_readiness == ExpansionReadiness.DO_NOT_FREEZE
    assert "mutated_fixture_cannot_be_presented_as_external" in candidate.rejection_reasons


def test_synthetic_local_candidate_cannot_be_presented_as_external():
    candidate = validate_expansion_candidate(_candidate("010"))
    assert candidate.expansion_readiness == ExpansionReadiness.DO_NOT_FREEZE
    assert "synthetic_local_cannot_be_presented_as_external" in candidate.rejection_reasons


def test_expansion_score_is_diagnostic_only():
    candidate = validate_expansion_candidate(_candidate("001"))
    score = score_expansion_candidate(candidate)
    assert 0.0 <= score <= 1.0
    assert candidate.freeze_recommendation == FreezeRecommendation.RECOMMEND_FOR_V0_4_X_FREEZE
    assert "dataset promotion" not in str(score).lower()


def test_batch_summary_counts_are_conservative():
    batch = validate_expansion_batch(load_expansion_candidates())
    assert batch["ready_for_future_freeze"] == 7
    assert batch["ready_with_human_review"] == 3
    assert batch["blocked_or_rejected"] == 6
    assert batch["batch_decision"] == "EXPANSION_POOL_READY_FOR_REVIEW"


def test_report_builder_produces_json_summary_and_markdown_report(tmp_path):
    summary = write_expansion_intake_artifacts(tmp_path, ROOT)
    assert summary["final_decision"] == "FROZEN_DATASET_EXPANSION_INTAKE_IMPLEMENTED_NO_PROVIDER_EXECUTION"
    assert summary["providers_executed"] is False
    assert (tmp_path / "expansion_intake_summary.json").exists()
    assert (tmp_path / "expansion_intake_report.md").exists()
    report = (tmp_path / "expansion_intake_report.md").read_text(encoding="utf-8")
    assert "v0.4 frozen dataset was not modified" in report


def test_v0_4_frozen_task_files_are_not_modified():
    hashes = _load_json(BASE_HASH_PATH)
    assert hashes["dataset_hash"] == "0ed903b013bff8650ce30030863d069a6cdd745d42964ba85082389d836cdb17"
    assert hashes["manifest_hash"] == "981406f6aa7a736cb64e698742075c4f05fbafcdf7e79e96a97c781224984298"


def test_expansion_summary_preserves_no_provider_execution_boundary():
    summary = build_expansion_summary(ROOT)
    assert summary["expansion_modifies_frozen_dataset"] is False
    assert summary["provider_execution_allowed"] is False
    assert summary["model_comparison_allowed"] is False
    assert summary["external_superiority_claim_authorized"] is False
    assert summary["providers_executed"] is False
    assert summary["network_required"] is False
    assert summary["env_read"] is False
    assert summary["secrets_printed"] is False


def test_status_document_exists_and_blocks_overclaims():
    path = Path("docs/status/FINITEXO_CODE_MATRIX_V0_4_1_FROZEN_DATASET_EXPANSION_INTAKE.md")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "FROZEN_DATASET_EXPANSION_INTAKE_IMPLEMENTED_NO_PROVIDER_EXECUTION" in text
    assert "v0.4 frozen dataset was expanded" in text
