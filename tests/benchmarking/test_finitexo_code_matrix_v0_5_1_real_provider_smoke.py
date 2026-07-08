import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.dataset_loader import load_frozen_dataset
from benchmarks.finitexo_code_matrix_v0_5.real_provider_smoke import (
    RealProviderCallResult,
    RealProviderSpec,
    RealSmokeConfig,
    evaluate_real_provider_gate,
    run_real_provider_smoke,
)
from benchmarks.finitexo_code_matrix_v0_5.real_provider_smoke.artifact_writer import (
    write_real_provider_smoke_artifacts,
)


ROOT = Path("benchmarks/finitexo_code_matrix_v0_5")
DATASET_ROOT = Path("benchmarks/finitexo_code_matrix_v0_4_3")
EXPECTED_DATASET_HASH = "a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4"
EXPECTED_MANIFEST_HASH = "6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _one_provider_config(tmp_path, **overrides):
    values = {
        "output_dir": tmp_path,
        "providers": (RealProviderSpec("stub", "stub-real-model", "STUB_API_KEY", 0.00001),),
        "real_provider_confirmation": True,
        "environ": {"STUB_API_KEY": "present-but-not-secret-shaped"},
    }
    values.update(overrides)
    return RealSmokeConfig(**values)


def _stub_adapter(provider, task, config):
    text = (
        f"Diagnostic smoke response for {task['task_id']}. "
        "Preserve the API contract and report limitations."
    )
    return RealProviderCallResult(
        response_text=text,
        prompt_tokens=10,
        completion_tokens=12,
        total_tokens=22,
        estimated_cost_usd=provider.estimated_cost_per_task_usd,
        provider_reported_model=provider.model_name,
    )


def test_v0_5_1_manifest_exists_and_targets_v0_4_3():
    manifest = _load_json(ROOT / "real_provider_smoke_manifest.json")
    assert manifest["benchmark_version"] == "v0.5.1"
    assert manifest["input_dataset_version"] == "v0.4.3"
    assert manifest["input_dataset_path"] == "benchmarks/finitexo_code_matrix_v0_4_3"
    assert manifest["expected_dataset_hash"] == EXPECTED_DATASET_HASH
    assert manifest["expected_manifest_hash"] == EXPECTED_MANIFEST_HASH


def test_manifest_uses_real_mode_and_blocks_claims():
    manifest = _load_json(ROOT / "real_provider_smoke_manifest.json")
    assert manifest["provider_mode"] == "real"
    assert manifest["mock_fallback_allowed"] is False
    assert manifest["statistical_claim_authorized"] is False
    assert manifest["provider_superiority_claim_authorized"] is False
    assert manifest["xendris_superiority_claim_authorized"] is False
    assert manifest["external_benchmark_validation_claim_authorized"] is False


def test_frozen_dataset_loader_still_loads_exactly_10_tasks_and_hashes():
    dataset = load_frozen_dataset(DATASET_ROOT)
    assert len(dataset.tasks) == 10
    assert dataset.dataset_hash == EXPECTED_DATASET_HASH
    assert dataset.manifest_hash == EXPECTED_MANIFEST_HASH


def test_gate_blocks_when_explicit_confirmation_is_missing(tmp_path):
    config = _one_provider_config(tmp_path, real_provider_confirmation=False)
    gate = evaluate_real_provider_gate(config)
    assert gate.can_execute is False
    assert gate.decision == "REAL_PROVIDER_SMOKE_READY_CONFIGURATION_MISSING_NO_EXECUTION"
    assert any("confirmation" in blocker for blocker in gate.blockers)


def test_gate_blocks_when_provider_keys_are_missing_without_printing_secret(tmp_path):
    config = _one_provider_config(tmp_path, environ={})
    gate = evaluate_real_provider_gate(config)
    assert gate.can_execute is False
    assert gate.provider_key_status["stub"] == "MISSING"
    serialized = json.dumps(gate.to_dict())
    assert "sk-" not in serialized
    assert "present-but-not-secret-shaped" not in serialized


def test_gate_passes_with_fake_test_configuration_without_network(tmp_path):
    config = _one_provider_config(tmp_path)
    gate = evaluate_real_provider_gate(config)
    assert gate.can_execute is True
    assert gate.dataset_hash == EXPECTED_DATASET_HASH
    assert gate.manifest_hash == EXPECTED_MANIFEST_HASH
    assert gate.frozen_task_count == 10


def test_runner_simulates_real_provider_execution_with_stub_adapter(tmp_path):
    config = _one_provider_config(tmp_path)
    result = run_real_provider_smoke(config, adapter=_stub_adapter)
    assert len(result["records"]) == 10
    assert result["provider_errors"] == []
    assert result["mock_fallback_used"] is False
    assert result["total_estimated_cost_usd"] == 0.0001


def test_provider_failures_are_captured_not_hidden(tmp_path):
    def failing_adapter(provider, task, config):
        raise RuntimeError("provider failure sk-secret-value")

    config = _one_provider_config(tmp_path)
    result = run_real_provider_smoke(config, adapter=failing_adapter)
    assert len(result["records"]) == 10
    assert result["provider_errors"]
    assert all("sk-" not in error["error_message_sanitized"] for error in result["provider_errors"])


def test_all_provider_failure_produces_conservative_decision(tmp_path):
    def failing_adapter(provider, task, config):
        raise RuntimeError("provider failure")

    config = _one_provider_config(tmp_path)
    result = run_real_provider_smoke(config, adapter=failing_adapter)
    summary = write_real_provider_smoke_artifacts(result)
    assert summary["final_decision"] == "REAL_PROVIDER_SMOKE_ATTEMPTED_ALL_PROVIDERS_FAILED_NO_CLAIM"
    assert summary["providers_completed"] == []
    assert summary["providers_failed"] == ["stub"]


def test_budget_guard_blocks_over_budget_runs(tmp_path):
    config = _one_provider_config(
        tmp_path,
        budget_cap_usd=0.000001,
        providers=(RealProviderSpec("stub", "stub-real-model", "STUB_API_KEY", 0.01),),
    )
    result = run_real_provider_smoke(config, adapter=_stub_adapter)
    assert result["task_attempts_budget_blocked"] == 10
    assert result["records"] == []
    assert result["provider_errors"]


def test_real_provider_artifacts_are_generated(tmp_path):
    config = _one_provider_config(tmp_path)
    result = run_real_provider_smoke(config, adapter=_stub_adapter)
    summary = write_real_provider_smoke_artifacts(result)
    assert (tmp_path / "real_provider_smoke_summary.json").exists()
    assert (tmp_path / "real_provider_smoke_report.md").exists()
    assert (tmp_path / "real_provider_responses.jsonl").exists()
    assert (tmp_path / "real_provider_scores.jsonl").exists()
    assert (tmp_path / "real_provider_costs.json").exists()
    assert (tmp_path / "real_provider_errors.jsonl").exists()
    assert (tmp_path / "real_provider_gate.json").exists()
    assert summary["final_decision"] == "REAL_PROVIDER_SMOKE_ON_FROZEN_N10_COMPLETED_NO_STATISTICAL_CLAIM"


def test_summary_contains_required_real_provider_fields(tmp_path):
    config = _one_provider_config(tmp_path)
    result = run_real_provider_smoke(config, adapter=_stub_adapter)
    summary = write_real_provider_smoke_artifacts(result)
    assert summary["provider_mode"] == "real"
    assert summary["mock_fallback_used"] is False
    assert summary["statistical_claim_authorized"] is False
    assert summary["provider_superiority_claim_authorized"] is False
    assert summary["xendris_superiority_claim_authorized"] is False
    assert summary["external_benchmark_validation_claim_authorized"] is False
    assert summary["frozen_task_count"] == 10


def test_scoring_summary_is_diagnostic_only(tmp_path):
    config = _one_provider_config(tmp_path)
    result = run_real_provider_smoke(config, adapter=_stub_adapter)
    summary = write_real_provider_smoke_artifacts(result)
    score_rows = (tmp_path / "real_provider_scores.jsonl").read_text(encoding="utf-8").splitlines()
    assert score_rows
    first_score = json.loads(score_rows[0])
    assert first_score["scoring_confidence"] == "LOW_DIAGNOSTIC_ONLY"
    assert first_score["statistical_claim_authorized"] is False
    assert first_score["provider_superiority_claim_authorized"] is False
    assert first_score["external_benchmark_validation_claim_authorized"] is False
    assert "No hidden tests" in " ".join(summary["scoring_limitations"])


def test_configuration_missing_writes_blocked_artifacts(tmp_path):
    config = _one_provider_config(tmp_path, environ={})
    result = run_real_provider_smoke(config, adapter=_stub_adapter)
    summary = write_real_provider_smoke_artifacts(result)
    assert summary["final_decision"] == "REAL_PROVIDER_SMOKE_READY_CONFIGURATION_MISSING_NO_EXECUTION"
    assert summary["providers_configured"] == ["stub"]
    assert summary["providers_attempted"] == []
    assert summary["task_attempts_total"] == 0
    assert (tmp_path / "real_provider_gate.json").exists()


def test_original_v0_4_3_frozen_dataset_remains_unchanged():
    hashes = _load_json(DATASET_ROOT / "frozen_dataset_hashes.json")
    assert hashes["dataset_hash"] == EXPECTED_DATASET_HASH
    assert hashes["manifest_hash"] == EXPECTED_MANIFEST_HASH
