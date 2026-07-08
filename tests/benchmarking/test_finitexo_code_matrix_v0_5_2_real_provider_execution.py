import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.dataset_loader import load_frozen_dataset
from benchmarks.finitexo_code_matrix_v0_5.real_provider_execution import (
    ProviderExecutionResult,
    ProviderExecutionSpec,
    RealProviderExecutionConfig,
    evaluate_real_provider_execution_gate,
    run_real_provider_execution,
    write_real_provider_execution_artifacts,
)


ROOT = Path("benchmarks/finitexo_code_matrix_v0_5")
DATASET_ROOT = Path("benchmarks/finitexo_code_matrix_v0_4_3")
EXPECTED_DATASET_HASH = "a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4"
EXPECTED_MANIFEST_HASH = "6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _config(tmp_path, **overrides):
    values = {
        "output_dir": tmp_path,
        "providers": (ProviderExecutionSpec("stub", "stub-real-model", "STUB_API_KEY", 0.00001),),
        "environ": {
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "STUB_API_KEY": "present-test-key",
        },
    }
    values.update(overrides)
    return RealProviderExecutionConfig(**values)


def _adapter(provider, task, config):
    return ProviderExecutionResult(
        raw_response_text=f"  Diagnostic provider response for {task['task_id']} preserving API contract.  ",
        prompt_tokens=11,
        completion_tokens=13,
        total_tokens=24,
        estimated_cost_usd=provider.estimated_cost_per_task_usd,
        provider_reported_model=provider.model_name,
    )


def test_v0_5_2_manifest_exists_and_preserves_hash_contract():
    manifest = _load_json(ROOT / "real_provider_execution_manifest.json")
    assert manifest["benchmark_version"] == "v0.5.2"
    assert manifest["input_dataset_version"] == "v0.4.3"
    assert manifest["expected_dataset_hash"] == EXPECTED_DATASET_HASH
    assert manifest["expected_manifest_hash"] == EXPECTED_MANIFEST_HASH
    assert manifest["mock_fallback_allowed"] is False


def test_no_execution_without_confirmation(tmp_path):
    config = _config(tmp_path, environ={"STUB_API_KEY": "present-test-key"})
    result = run_real_provider_execution(config, adapter=_adapter)
    summary = write_real_provider_execution_artifacts(result)
    assert summary["final_decision"] == "REAL_PROVIDER_SMOKE_CONFIGURATION_MISSING_NO_EXECUTION"
    assert summary["providers_attempted"] == []
    assert summary["task_attempts_skipped"] == 10
    assert summary["total_estimated_cost_usd"] == 0.0


def test_no_execution_without_keys(tmp_path):
    config = _config(tmp_path, environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true"})
    gate = evaluate_real_provider_execution_gate(config)
    assert gate.can_execute is False
    assert gate.provider_key_status["stub"] == "MISSING"


def test_no_env_loading_is_required_for_injected_process_environment(tmp_path):
    config = _config(tmp_path)
    gate = evaluate_real_provider_execution_gate(config)
    assert gate.can_execute is True
    assert ".env" not in json.dumps(gate.to_dict()).lower()


def test_no_mock_fallback_allowed(tmp_path):
    config = _config(tmp_path, allow_mock_fallback=True)
    gate = evaluate_real_provider_execution_gate(config)
    assert gate.can_execute is False
    assert any("mock fallback" in blocker for blocker in gate.blockers)


def test_frozen_dataset_hash_and_manifest_hash_are_checked():
    dataset = load_frozen_dataset(DATASET_ROOT)
    assert dataset.dataset_hash == EXPECTED_DATASET_HASH
    assert dataset.manifest_hash == EXPECTED_MANIFEST_HASH
    assert len(dataset.tasks) == 10


def test_skipped_attempts_are_counted_correctly(tmp_path):
    config = _config(
        tmp_path,
        providers=(
            ProviderExecutionSpec("a", "a-model", "A_KEY", 0.00001),
            ProviderExecutionSpec("b", "b-model", "B_KEY", 0.00001),
        ),
        environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true"},
    )
    result = run_real_provider_execution(config, adapter=_adapter)
    assert result["task_attempts_skipped"] == 20
    summary = write_real_provider_execution_artifacts(result)
    assert summary["providers_configured"] == ["a", "b"]
    assert summary["providers_attempted"] == []


def test_partial_provider_failures_are_captured(tmp_path):
    def partial_adapter(provider, task, config):
        if task["task_id"].endswith("001"):
            raise RuntimeError("provider failed with sk-secret")
        return _adapter(provider, task, config)

    config = _config(tmp_path)
    result = run_real_provider_execution(config, adapter=partial_adapter)
    summary = write_real_provider_execution_artifacts(result)
    assert result["provider_errors"]
    assert "sk-" not in json.dumps(result["provider_errors"])
    assert summary["task_attempts_failed"] == 1
    assert summary["task_attempts_completed"] == 9


def test_successful_provider_responses_are_scored(tmp_path):
    config = _config(tmp_path)
    result = run_real_provider_execution(config, adapter=_adapter)
    summary = write_real_provider_execution_artifacts(result)
    assert summary["final_decision"] == "REAL_PROVIDER_SMOKE_EXECUTED_DIAGNOSTIC_ONLY"
    scores = (tmp_path / "real_provider_scores.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(scores) == 10
    first_score = json.loads(scores[0])
    assert first_score["statistical_claim_authorized"] is False
    assert first_score["provider_superiority_claim_authorized"] is False


def test_response_records_include_raw_and_normalized_text(tmp_path):
    config = _config(tmp_path)
    result = run_real_provider_execution(config, adapter=_adapter)
    write_real_provider_execution_artifacts(result)
    first = json.loads((tmp_path / "real_provider_responses.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert "raw_provider_response_text" in first
    assert "normalized_response_text" in first
    assert first["raw_provider_response_text"] != first["normalized_response_text"]


def test_cost_accounting_and_request_metadata_are_generated(tmp_path):
    config = _config(tmp_path)
    result = run_real_provider_execution(config, adapter=_adapter)
    summary = write_real_provider_execution_artifacts(result)
    assert summary["total_estimated_cost_usd"] == 0.0001
    assert (tmp_path / "real_provider_costs.json").exists()
    assert (tmp_path / "provider_request_metadata.jsonl").exists()


def test_final_gate_decision_is_conservative(tmp_path):
    config = _config(tmp_path, statistical_claim_authorized=True)
    gate = evaluate_real_provider_execution_gate(config)
    assert gate.can_execute is False
    assert gate.decision == "REAL_PROVIDER_SMOKE_CONFIGURATION_MISSING_NO_EXECUTION"


def test_all_required_artifacts_are_generated(tmp_path):
    config = _config(tmp_path)
    result = run_real_provider_execution(config, adapter=_adapter)
    write_real_provider_execution_artifacts(result)
    assert (tmp_path / "real_provider_execution_summary.json").exists()
    assert (tmp_path / "real_provider_execution_report.md").exists()
    assert (tmp_path / "real_provider_responses.jsonl").exists()
    assert (tmp_path / "real_provider_scores.jsonl").exists()
    assert (tmp_path / "real_provider_costs.json").exists()
    assert (tmp_path / "real_provider_errors.jsonl").exists()
    assert (tmp_path / "real_provider_gate.json").exists()
    assert (tmp_path / "provider_request_metadata.jsonl").exists()


def test_original_v0_4_3_frozen_dataset_remains_unchanged():
    hashes = _load_json(DATASET_ROOT / "frozen_dataset_hashes.json")
    assert hashes["dataset_hash"] == EXPECTED_DATASET_HASH
    assert hashes["manifest_hash"] == EXPECTED_MANIFEST_HASH
