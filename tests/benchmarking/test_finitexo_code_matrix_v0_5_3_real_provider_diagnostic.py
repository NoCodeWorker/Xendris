import json
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_5.real_provider_diagnostic import (
    DiagnosticProviderResult,
    DiagnosticProviderSpec,
    RealProviderDiagnosticConfig,
    evaluate_diagnostic_preflight,
    run_real_provider_diagnostic,
    validate_diagnostic_artifacts,
    write_real_provider_diagnostic_artifacts,
)


DATASET_ROOT = Path("benchmarks/finitexo_code_matrix_v0_4_3")
RELEASE_GATE = Path("runs/finitexo_code_matrix_v0_5_2_release_gate/release_gate_summary.json")
EXPECTED_DATASET_HASH = "a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4"
EXPECTED_MANIFEST_HASH = "6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e"


def _config(tmp_path, **overrides):
    values = {
        "output_dir": tmp_path,
        "release_gate_summary_path": RELEASE_GATE,
        "providers": (DiagnosticProviderSpec("stub", "stub-model", "STUB_API_KEY", 0.00001),),
        "environ": {
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "STUB_API_KEY": "present-test-key",
        },
    }
    values.update(overrides)
    return RealProviderDiagnosticConfig(**values)


def _adapter(provider, task, config):
    return DiagnosticProviderResult(
        raw_response_text=f"  Diagnostic response for {task['task_id']} preserving API contract.  ",
        prompt_tokens=10,
        completion_tokens=12,
        total_tokens=22,
        estimated_cost_usd=provider.estimated_cost_per_task_usd,
        provider_reported_model=provider.model_name,
    )


def test_blocks_without_release_gate_approval(tmp_path):
    bad_gate = tmp_path / "release_gate_summary.json"
    bad_gate.write_text('{"decision":"BLOCKED"}\n', encoding="utf-8")
    config = _config(tmp_path, release_gate_summary_path=bad_gate)
    preflight = evaluate_diagnostic_preflight(config)
    assert preflight.can_execute is False
    assert preflight.decision == "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_BLOCKED_PRECONDITION_MISSING"


def test_blocks_without_explicit_confirmation_flag(tmp_path):
    config = _config(tmp_path, environ={"STUB_API_KEY": "present-test-key"})
    result = run_real_provider_diagnostic(config, adapter=_adapter)
    summary = write_real_provider_diagnostic_artifacts(result)
    assert summary["final_decision"] == "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_BLOCKED_PRECONDITION_MISSING"
    assert summary["task_attempts_skipped"] == 10


def test_blocks_without_provider_keys(tmp_path):
    config = _config(tmp_path, environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true"})
    preflight = evaluate_diagnostic_preflight(config)
    assert preflight.can_execute is False
    assert preflight.provider_key_status["stub"] == "MISSING"


def test_blocks_without_reading_env_files(tmp_path):
    config = _config(tmp_path)
    preflight = evaluate_diagnostic_preflight(config)
    assert preflight.can_execute is True
    assert ".env" not in json.dumps(preflight.to_dict()).lower()


def test_blocks_without_mock_fallback(tmp_path):
    config = _config(tmp_path, allow_mock_fallback=True)
    preflight = evaluate_diagnostic_preflight(config)
    assert preflight.can_execute is False
    assert any("mock fallback" in blocker for blocker in preflight.blockers)


def test_verifies_frozen_dataset_hash_manifest_hash_and_attempt_count(tmp_path):
    config = _config(
        tmp_path,
        providers=(
            DiagnosticProviderSpec("deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001),
            DiagnosticProviderSpec("openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001),
        ),
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    preflight = evaluate_diagnostic_preflight(config)
    assert preflight.dataset_hash == EXPECTED_DATASET_HASH
    assert preflight.manifest_hash == EXPECTED_MANIFEST_HASH
    assert preflight.frozen_task_count == 10
    assert preflight.task_attempts_expected == 20


def test_records_real_attempted_completed_failed_counts_with_test_doubles(tmp_path):
    config = _config(tmp_path)
    result = run_real_provider_diagnostic(config, adapter=_adapter)
    summary = write_real_provider_diagnostic_artifacts(result)
    assert summary["task_attempts_attempted"] == 10
    assert summary["task_attempts_completed"] == 10
    assert summary["task_attempts_failed"] == 0
    assert summary["providers_attempted"] == ["stub"]
    assert summary["providers_completed"] == ["stub"]


def test_captures_provider_error_without_aborting_entire_run(tmp_path):
    def partial_adapter(provider, task, config):
        if task["task_id"].endswith("001"):
            raise RuntimeError("provider failed with sk-secret")
        return _adapter(provider, task, config)

    config = _config(tmp_path)
    result = run_real_provider_diagnostic(config, adapter=partial_adapter)
    summary = write_real_provider_diagnostic_artifacts(result)
    assert summary["final_decision"] == "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_PARTIAL_NO_CLAIMS"
    assert summary["task_attempts_completed"] == 9
    assert summary["task_attempts_failed"] == 1
    assert "sk-" not in json.dumps(result["provider_errors"])


def test_blocks_on_cost_above_budget(tmp_path):
    config = _config(
        tmp_path,
        budget_cap_usd=0.000001,
        providers=(DiagnosticProviderSpec("stub", "stub-model", "STUB_API_KEY", 0.01),),
    )
    result = run_real_provider_diagnostic(config, adapter=_adapter)
    summary = write_real_provider_diagnostic_artifacts(result)
    assert summary["final_decision"] == "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_BLOCKED_BUDGET"
    assert summary["task_attempts_budget_blocked"] == 10


def test_blocks_on_response_artifacts_existing_while_attempted_count_zero(tmp_path):
    config = _config(tmp_path, environ={"STUB_API_KEY": "present-test-key"})
    result = run_real_provider_diagnostic(config, adapter=_adapter)
    write_real_provider_diagnostic_artifacts(result)
    (tmp_path / "real_provider_responses.jsonl").write_text(
        '{"provider_name":"stub","response_text":"unexpected"}\n',
        encoding="utf-8",
    )
    assert validate_diagnostic_artifacts(tmp_path) == "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_BLOCKED_ARTIFACT_INCONSISTENCY"


def test_claim_authorization_flags_are_false(tmp_path):
    config = _config(tmp_path)
    result = run_real_provider_diagnostic(config, adapter=_adapter)
    summary = write_real_provider_diagnostic_artifacts(result)
    assert summary["statistical_claim_authorized"] is False
    assert summary["provider_superiority_claim_authorized"] is False
    assert summary["xendris_superiority_claim_authorized"] is False
