from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_5.real_provider_authorized import (
    AuthorizedDiagnosticConfig,
    AuthorizedProviderResult,
    AuthorizedProviderSpec,
    evaluate_authorized_preflight,
    run_authorized_diagnostic,
    write_authorized_diagnostic_artifacts,
)


RELEASE_GATE = Path("runs/finitexo_code_matrix_v0_5_2_release_gate/release_gate_summary.json")
EXPECTED_DATASET_HASH = "a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4"
EXPECTED_MANIFEST_HASH = "6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e"


def _config(tmp_path, **overrides):
    values = {
        "output_dir": tmp_path,
        "release_gate_summary_path": RELEASE_GATE,
        "providers": (AuthorizedProviderSpec("stub", "stub-model", "STUB_API_KEY", 0.00001),),
        "environ": {
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "STUB_API_KEY": "present-test-key",
        },
    }
    values.update(overrides)
    return AuthorizedDiagnosticConfig(**values)


def _adapter(provider, task, config):
    return AuthorizedProviderResult(
        raw_response_text=f"Authorized diagnostic response for {task['task_id']} preserving API contract.",
        prompt_tokens=10,
        completion_tokens=12,
        total_tokens=22,
        estimated_cost_usd=provider.estimated_cost_per_task_usd,
        provider_reported_model=provider.model_name,
    )


def test_blocks_without_confirmation(tmp_path):
    config = _config(tmp_path, environ={"STUB_API_KEY": "present-test-key"})
    summary = write_authorized_diagnostic_artifacts(run_authorized_diagnostic(config, adapter=_adapter))
    assert summary["final_decision"] == "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_BLOCKED_PRECONDITION_MISSING"
    assert summary["providers_attempted"] == []
    assert summary["task_attempts_skipped"] == 10


def test_blocks_without_provider_keys(tmp_path):
    config = _config(tmp_path, environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true"})
    preflight = evaluate_authorized_preflight(config)
    assert preflight.can_execute is False
    assert preflight.provider_key_status["stub"] == "MISSING"


def test_authorized_preflight_verifies_dataset_hash_manifest_hash_and_expected_attempts(tmp_path):
    config = _config(
        tmp_path,
        providers=(
            AuthorizedProviderSpec("deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001),
            AuthorizedProviderSpec("openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001),
        ),
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    preflight = evaluate_authorized_preflight(config)
    assert preflight.can_execute is True
    assert preflight.dataset_hash == EXPECTED_DATASET_HASH
    assert preflight.manifest_hash == EXPECTED_MANIFEST_HASH
    assert preflight.frozen_task_count == 10
    assert preflight.task_attempts_expected == 20


def test_with_variables_present_providers_are_attempted(tmp_path):
    config = _config(tmp_path)
    summary = write_authorized_diagnostic_artifacts(run_authorized_diagnostic(config, adapter=_adapter))
    assert summary["providers_attempted"] == ["stub"]
    assert summary["task_attempts_attempted"] == 10
    assert summary["task_attempts_completed"] == 10
    assert summary["final_decision"] == "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_COMPLETED_DIAGNOSTIC_ONLY"


def test_provider_errors_are_captured_as_diagnostic_failures(tmp_path):
    def failing_adapter(provider, task, config):
        raise RuntimeError("network failed with sk-secret")

    config = _config(tmp_path)
    result = run_authorized_diagnostic(config, adapter=failing_adapter)
    summary = write_authorized_diagnostic_artifacts(result)
    assert summary["final_decision"] == "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_COMPLETED_WITH_PROVIDER_ERRORS"
    assert summary["task_attempts_failed"] == 10
    assert "sk-" not in str(result["provider_errors"])


def test_budget_blocks_before_execution(tmp_path):
    config = _config(
        tmp_path,
        budget_cap_usd=0.000001,
        providers=(AuthorizedProviderSpec("stub", "stub-model", "STUB_API_KEY", 0.01),),
    )
    summary = write_authorized_diagnostic_artifacts(run_authorized_diagnostic(config, adapter=_adapter))
    assert summary["final_decision"] == "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_BLOCKED_BUDGET"
    assert summary["task_attempts_budget_blocked"] == 10


def test_no_mock_fallback_and_no_claims_authorized(tmp_path):
    config = _config(tmp_path)
    summary = write_authorized_diagnostic_artifacts(run_authorized_diagnostic(config, adapter=_adapter))
    assert summary["mock_fallback_used"] is False
    assert summary["statistical_claim_authorized"] is False
    assert summary["provider_superiority_claim_authorized"] is False
    assert summary["xendris_superiority_claim_authorized"] is False


def test_artifacts_are_generated(tmp_path):
    config = _config(tmp_path)
    write_authorized_diagnostic_artifacts(run_authorized_diagnostic(config, adapter=_adapter))
    assert (tmp_path / "real_provider_diagnostic_summary.json").exists()
    assert (tmp_path / "real_provider_diagnostic_report.md").exists()
    assert (tmp_path / "real_provider_responses.jsonl").exists()
    assert (tmp_path / "real_provider_scores.jsonl").exists()
    assert (tmp_path / "real_provider_costs.json").exists()
    assert (tmp_path / "real_provider_errors.jsonl").exists()
    assert (tmp_path / "real_provider_gate.json").exists()
    assert (tmp_path / "provider_request_metadata.jsonl").exists()
    assert (tmp_path / "provider_preflight.json").exists()
