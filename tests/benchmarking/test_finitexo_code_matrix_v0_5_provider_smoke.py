import json
from pathlib import Path

import pytest

from benchmarks.finitexo_code_matrix_v0_5.provider_smoke import (
    SmokeConfig,
    load_frozen_dataset,
    run_provider_smoke,
    write_smoke_artifacts,
)
from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.budget_guard import BudgetDecision, BudgetGuard
from benchmarks.finitexo_code_matrix_v0_5.scoring import score_provider_responses


ROOT = Path("benchmarks/finitexo_code_matrix_v0_5")
DATASET_ROOT = Path("benchmarks/finitexo_code_matrix_v0_4_3")
EXPECTED_DATASET_HASH = "a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4"
EXPECTED_MANIFEST_HASH = "6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_v0_5_package_and_manifest_exist():
    assert ROOT.exists()
    assert (ROOT / "provider_smoke_manifest.json").exists()


def test_manifest_points_to_v0_4_3_and_blocks_overclaims():
    manifest = _load_json(ROOT / "provider_smoke_manifest.json")
    assert manifest["input_dataset_version"] == "v0.4.3"
    assert manifest["expected_dataset_hash"] == EXPECTED_DATASET_HASH
    assert manifest["expected_manifest_hash"] == EXPECTED_MANIFEST_HASH
    assert manifest["statistical_claim_authorized"] is False
    assert manifest["provider_superiority_claim_authorized"] is False
    assert manifest["xendris_superiority_claim_authorized"] is False


def test_frozen_dataset_loader_loads_exactly_10_tasks_and_hashes():
    dataset = load_frozen_dataset(DATASET_ROOT)
    assert len(dataset.tasks) == 10
    assert dataset.dataset_hash == EXPECTED_DATASET_HASH
    assert dataset.manifest_hash == EXPECTED_MANIFEST_HASH


def test_loader_refuses_corrupted_hashes(tmp_path):
    source = DATASET_ROOT
    target = tmp_path / "dataset"
    import shutil

    shutil.copytree(source, target)
    hashes = _load_json(target / "frozen_dataset_hashes.json")
    hashes["dataset_hash"] = "bad"
    (target / "frozen_dataset_hashes.json").write_text(json.dumps(hashes), encoding="utf-8")
    with pytest.raises(ValueError):
        load_frozen_dataset(target)


def test_loader_does_not_modify_frozen_dataset_files():
    before = _load_json(DATASET_ROOT / "frozen_dataset_hashes.json")
    load_frozen_dataset(DATASET_ROOT)
    after = _load_json(DATASET_ROOT / "frozen_dataset_hashes.json")
    assert before == after


def test_mock_provider_mode_runs_without_network(tmp_path):
    config = SmokeConfig(output_dir=tmp_path)
    result = run_provider_smoke(config)
    assert len(result["records"]) == 10
    assert result["provider_errors"] == []
    assert result["total_estimated_cost_usd"] == 0.0001


def test_real_provider_mode_requires_explicit_configuration():
    config = SmokeConfig(provider_mode="real")
    with pytest.raises(ValueError):
        run_provider_smoke(config)


def test_missing_provider_keys_do_not_print_secrets():
    config = SmokeConfig(provider_mode="real")
    with pytest.raises(ValueError) as excinfo:
        run_provider_smoke(config)
    assert "sk-" not in str(excinfo.value)


def test_provider_failures_are_captured_not_hidden(tmp_path):
    config = SmokeConfig(output_dir=tmp_path, provider_mode="mock", budget_cap_usd=0.0)
    result = run_provider_smoke(config)
    summary = write_smoke_artifacts(result)
    assert summary["task_attempts_total"] == 0
    assert result["provider_errors"]


def test_budget_guard_blocks_over_budget_runs():
    guard = BudgetGuard(budget_cap_usd=0.01, total_estimated_cost_usd=0.009)
    assert guard.check_before_task(0.002) == BudgetDecision.WOULD_EXCEED_BUDGET


def test_artifacts_are_generated(tmp_path):
    result = run_provider_smoke(SmokeConfig(output_dir=tmp_path))
    summary = write_smoke_artifacts(result)
    assert (tmp_path / "provider_smoke_summary.json").exists()
    assert (tmp_path / "provider_smoke_report.md").exists()
    assert (tmp_path / "provider_responses.jsonl").exists()
    assert (tmp_path / "provider_scores.jsonl").exists()
    assert (tmp_path / "provider_costs.json").exists()
    assert (tmp_path / "provider_errors.jsonl").exists()
    assert summary["final_decision"] == "PROVIDER_SMOKE_DRY_RUN_COMPLETED_NO_REAL_PROVIDER_CLAIM"


def test_scoring_summary_is_diagnostic_only():
    result = run_provider_smoke(SmokeConfig())
    scores = score_provider_responses(result["records"])
    assert scores
    assert all(score.statistical_claim_authorized is False for score in scores)
    assert all(score.provider_superiority_claim_authorized is False for score in scores)
    assert all(score.external_benchmark_validation_claim_authorized is False for score in scores)
    assert all(score.scoring_confidence == "LOW_DIAGNOSTIC_ONLY" for score in scores)


def test_original_v0_4_3_dataset_remains_unchanged():
    hashes = _load_json(DATASET_ROOT / "frozen_dataset_hashes.json")
    assert hashes["dataset_hash"] == EXPECTED_DATASET_HASH
    assert hashes["manifest_hash"] == EXPECTED_MANIFEST_HASH


def test_status_document_exists_and_blocks_claims():
    path = Path("docs/status/FINITEXO_CODE_MATRIX_V0_5_PROVIDER_SMOKE_FROZEN_N10.md")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "PROVIDER_SMOKE_DRY_RUN_COMPLETED_NO_REAL_PROVIDER_CLAIM" in text
    assert "provider superiority demonstrated" in text
