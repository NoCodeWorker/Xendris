"""Tests for Xendris Foundational Runtime Contract."""

from xendris.core.methodology import (
    CalibrationTraceContract,
    ExecutionMethod,
    MethodologyContract,
    MethodologyValidationResult,
    RuntimeTraceContract,
    validate_benchmark_methodology_config,
    validate_calibrated_runtime_trace,
    validate_runtime_trace,
)
from xendris.core.methodology.runtime_contract import (
    CALIBRATED_RUNTIME_REQUIRED_ARTIFACTS,
    FORBIDDEN_SUBSTITUTIONS,
    RUNTIME_CONTRACT_FINAL_DECISION,
    RUNTIME_REQUIRED_ARTIFACTS,
    get_methodology_doctrine_summary,
)
from xendris.core.methodology.methodology_guard import (
    METHODOLOGY_GUARD_BLOCKED,
    METHODOLOGY_GUARD_READY,
)


# ---------------------------------------------------------------------------
# Execution method validation
# ---------------------------------------------------------------------------

def test_base_does_not_require_runtime_phases():
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_base",
        execution_method=ExecutionMethod.BASE,
        initial_response_present=True,
    )
    result = validate_runtime_trace(trace)
    assert result.is_valid


def test_wrapper_does_not_require_runtime_phases():
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_wrapper",
        execution_method=ExecutionMethod.WRAPPER,
        initial_response_present=True,
    )
    result = validate_runtime_trace(trace)
    assert result.is_valid


def test_runtime_fails_without_deterministic_audit():
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_runtime",
        execution_method=ExecutionMethod.RUNTIME,
        initial_response_present=True,
        deterministic_audit_present=False,
        audit_decision_present=True,
        repair_or_degrade_or_block_considered=True,
        final_response_present=True,
        final_audit_present=True,
    )
    result = validate_runtime_trace(trace)
    assert not result.is_valid
    assert any("deterministic_audit" in e for e in result.errors)


def test_runtime_fails_without_audit_decision():
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_runtime",
        execution_method=ExecutionMethod.RUNTIME,
        initial_response_present=True,
        deterministic_audit_present=True,
        audit_decision_present=False,
        repair_or_degrade_or_block_considered=True,
        final_response_present=True,
        final_audit_present=True,
    )
    result = validate_runtime_trace(trace)
    assert not result.is_valid
    assert any("audit_decision" in e for e in result.errors)


def test_runtime_fails_without_final_audit():
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_runtime",
        execution_method=ExecutionMethod.RUNTIME,
        initial_response_present=True,
        deterministic_audit_present=True,
        audit_decision_present=True,
        repair_or_degrade_or_block_considered=True,
        final_response_present=True,
        final_audit_present=False,
    )
    result = validate_runtime_trace(trace)
    assert not result.is_valid
    assert any("final_audit" in e for e in result.errors)


def test_runtime_passes_with_all_required_phases():
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_runtime",
        execution_method=ExecutionMethod.RUNTIME,
        initial_response_present=True,
        deterministic_audit_present=True,
        audit_decision_present=True,
        repair_or_degrade_or_block_considered=True,
        final_response_present=True,
        final_audit_present=True,
    )
    result = validate_runtime_trace(trace)
    assert result.is_valid
    assert result.decision == METHODOLOGY_GUARD_READY


def test_calibrated_runtime_fails_without_calibration_trace():
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_calibrated_runtime",
        execution_method=ExecutionMethod.CALIBRATED_RUNTIME,
        initial_response_present=True,
        deterministic_audit_present=True,
        audit_decision_present=True,
        repair_or_degrade_or_block_considered=True,
        final_response_present=True,
        final_audit_present=True,
    )
    result = validate_calibrated_runtime_trace(trace, None)
    assert not result.is_valid
    assert any("calibration_trace" in e.lower() for e in result.errors)


def test_calibrated_runtime_fails_without_claim_status():
    cal = CalibrationTraceContract(
        claim_classification_present=False,
        evidence_status_present=True,
        confidence_band_present=True,
        allowed_language_present=True,
        blocked_language_present=True,
        final_calibrated_response_present=True,
    )
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_calibrated_runtime",
        execution_method=ExecutionMethod.CALIBRATED_RUNTIME,
        initial_response_present=True,
        deterministic_audit_present=True,
        audit_decision_present=True,
        repair_or_degrade_or_block_considered=True,
        final_response_present=True,
        final_audit_present=True,
    )
    result = validate_calibrated_runtime_trace(trace, cal)
    assert not result.is_valid
    assert any("claim_classification" in e for e in result.errors)


def test_calibrated_runtime_fails_without_confidence_band():
    cal = CalibrationTraceContract(
        claim_classification_present=True,
        evidence_status_present=True,
        confidence_band_present=False,
        allowed_language_present=True,
        blocked_language_present=True,
        final_calibrated_response_present=True,
    )
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_calibrated_runtime",
        execution_method=ExecutionMethod.CALIBRATED_RUNTIME,
        initial_response_present=True,
        deterministic_audit_present=True,
        audit_decision_present=True,
        repair_or_degrade_or_block_considered=True,
        final_response_present=True,
        final_audit_present=True,
    )
    result = validate_calibrated_runtime_trace(trace, cal)
    assert not result.is_valid
    assert any("confidence_band" in e for e in result.errors)


def test_calibrated_runtime_fails_without_allowed_blocked_language():
    cal = CalibrationTraceContract(
        claim_classification_present=True,
        evidence_status_present=True,
        confidence_band_present=True,
        allowed_language_present=False,
        blocked_language_present=False,
        final_calibrated_response_present=True,
    )
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_calibrated_runtime",
        execution_method=ExecutionMethod.CALIBRATED_RUNTIME,
        initial_response_present=True,
        deterministic_audit_present=True,
        audit_decision_present=True,
        repair_or_degrade_or_block_considered=True,
        final_response_present=True,
        final_audit_present=True,
    )
    result = validate_calibrated_runtime_trace(trace, cal)
    assert not result.is_valid
    assert any("allowed_language" in e for e in result.errors)
    assert any("blocked_language" in e for e in result.errors)


def test_calibrated_runtime_passes_with_complete_traces():
    cal = CalibrationTraceContract(
        claim_classification_present=True,
        evidence_status_present=True,
        confidence_band_present=True,
        allowed_language_present=True,
        blocked_language_present=True,
        final_calibrated_response_present=True,
    )
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_calibrated_runtime",
        execution_method=ExecutionMethod.CALIBRATED_RUNTIME,
        initial_response_present=True,
        deterministic_audit_present=True,
        audit_decision_present=True,
        repair_or_degrade_or_block_considered=True,
        final_response_present=True,
        final_audit_present=True,
    )
    result = validate_calibrated_runtime_trace(trace, cal)
    assert result.is_valid
    assert result.decision == METHODOLOGY_GUARD_READY


def test_variant_runtime_cannot_use_wrapper():
    trace = RuntimeTraceContract(
        task_id="t1", provider_name="deepseek", variant_name="deepseek_runtime",
        execution_method=ExecutionMethod.WRAPPER,
        initial_response_present=True,
    )
    result = validate_runtime_trace(trace)
    assert not result.is_valid
    assert any("runtime" in e and "WRAPPER" in e for e in result.errors)


def test_variant_calibrated_cannot_use_runtime_or_wrapper():
    for bad_method in (ExecutionMethod.RUNTIME, ExecutionMethod.WRAPPER):
        trace = RuntimeTraceContract(
            task_id="t1", provider_name="deepseek", variant_name="deepseek_calibrated_runtime",
            execution_method=bad_method,
            initial_response_present=True,
        )
        result = validate_calibrated_runtime_trace(trace, None)
        assert not result.is_valid
        assert any("calibrated" in e and bad_method.value in e for e in result.errors)


# ---------------------------------------------------------------------------
# Benchmark config validation
# ---------------------------------------------------------------------------

def test_benchmark_config_valid_with_all_methods():
    config = MethodologyContract(
        experiment_type="runtime_paired_lift",
        execution_methods=[ExecutionMethod.BASE, ExecutionMethod.WRAPPER,
                           ExecutionMethod.RUNTIME, ExecutionMethod.CALIBRATED_RUNTIME],
        has_runtime_traces=True,
        has_calibration_traces=True,
        has_runtime_variants=True,
        has_calibrated_runtime_variants=True,
        expected_top_level_executions=240,
        variant_names=[
            "deepseek_base", "deepseek_wrapper", "deepseek_runtime", "deepseek_calibrated_runtime",
            "openai_base", "openai_wrapper", "openai_runtime", "openai_calibrated_runtime",
        ],
    )
    result = validate_benchmark_methodology_config(config)
    assert result.is_valid


def test_benchmark_config_fails_with_only_base_wrapper_for_runtime():
    config = MethodologyContract(
        experiment_type="runtime_paired_lift",
        execution_methods=[ExecutionMethod.BASE, ExecutionMethod.WRAPPER],
        has_runtime_traces=False,
        has_calibration_traces=False,
        has_runtime_variants=False,
        has_calibrated_runtime_variants=False,
        expected_top_level_executions=120,
        variant_names=["deepseek_base", "deepseek_wrapper", "openai_base", "openai_wrapper"],
    )
    result = validate_benchmark_methodology_config(config)
    assert not result.is_valid
    assert any("only defines base/wrapper" in e for e in result.errors)


def test_benchmark_config_fails_when_runtime_artifacts_missing():
    config = MethodologyContract(
        experiment_type="runtime_paired_lift",
        execution_methods=[ExecutionMethod.BASE, ExecutionMethod.WRAPPER,
                           ExecutionMethod.RUNTIME],
        has_runtime_traces=False,
        has_calibration_traces=False,
        has_runtime_variants=True,
        has_calibrated_runtime_variants=False,
        expected_top_level_executions=240,
        variant_names=[
            "deepseek_base", "deepseek_wrapper", "deepseek_runtime",
            "openai_base", "openai_wrapper", "openai_runtime",
        ],
    )
    result = validate_benchmark_methodology_config(config)
    assert not result.is_valid
    assert any("runtime_traces" in e for e in result.errors)


# ---------------------------------------------------------------------------
# Contract constants
# ---------------------------------------------------------------------------

def test_runtime_contract_constants():
    assert RUNTIME_CONTRACT_FINAL_DECISION == "FOUNDATIONAL_RUNTIME_CONTRACT_ESTABLISHED"


def test_runtime_required_artifacts():
    assert "runtime_traces.jsonl" in RUNTIME_REQUIRED_ARTIFACTS
    assert "audit_decisions.jsonl" in RUNTIME_REQUIRED_ARTIFACTS
    assert "repair_attempts.jsonl" in RUNTIME_REQUIRED_ARTIFACTS
    assert "final_audits.jsonl" in RUNTIME_REQUIRED_ARTIFACTS


def test_calibrated_runtime_required_artifacts():
    assert "calibration_traces.jsonl" in CALIBRATED_RUNTIME_REQUIRED_ARTIFACTS
    assert "claim_status.jsonl" in CALIBRATED_RUNTIME_REQUIRED_ARTIFACTS
    assert "confidence_bands.jsonl" in CALIBRATED_RUNTIME_REQUIRED_ARTIFACTS
    assert "allowed_blocked_language.jsonl" in CALIBRATED_RUNTIME_REQUIRED_ARTIFACTS
    assert "calibrated_final_responses.jsonl" in CALIBRATED_RUNTIME_REQUIRED_ARTIFACTS


def test_forbidden_substitutions_are_listed():
    assert any("runtime" in s and "wrapper" in s for s in FORBIDDEN_SUBSTITUTIONS)
    assert any("calibration" in s for s in FORBIDDEN_SUBSTITUTIONS)


def test_doctrine_summary():
    summary = get_methodology_doctrine_summary()
    assert summary["final_decision"] == RUNTIME_CONTRACT_FINAL_DECISION
    assert len(summary["execution_methods"]) >= 4
    assert summary["development_rule"] is not None


def test_audit_decision_enum_values():
    from xendris.core.methodology import AuditDecision
    values = [e.value for e in AuditDecision]
    assert "ALLOW" in values
    assert "BLOCK" in values
    assert "REPAIR_REQUIRED" in values
    assert "HUMAN_REVIEW_REQUIRED" in values


def test_claim_status_enum_values():
    from xendris.core.methodology import ClaimStatus
    values = [e.value for e in ClaimStatus]
    assert "VERIFIED" in values
    assert "CONTRADICTED" in values
    assert "NEEDS_HUMAN_REVIEW" in values


def test_execution_method_order():
    methods = list(ExecutionMethod)
    assert methods.index(ExecutionMethod.BASE) < methods.index(ExecutionMethod.WRAPPER)
    assert methods.index(ExecutionMethod.WRAPPER) < methods.index(ExecutionMethod.RUNTIME)
    assert methods.index(ExecutionMethod.RUNTIME) < methods.index(ExecutionMethod.CALIBRATED_RUNTIME)
