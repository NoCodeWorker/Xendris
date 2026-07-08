"""Tests for v0.9 methodology guard."""

from benchmarks.finitexo_code_matrix_v0_9.methodology_guard.runtime_methodology_gate import (
    V0_9_REQUIRED_VARIANTS,
    V0_9_REQUIRED_ARTIFACTS,
    METHODOLOGY_GUARD_READY,
    METHODOLOGY_GUARD_BLOCKED,
    check_v0_9_methodology_gate,
    build_v0_9_methodology_contract,
    validate_v0_9_runtime_trace,
    validate_v0_9_calibrated_runtime_trace,
)
from xendris.core.methodology import (
    CalibrationTraceContract,
    ExecutionMethod,
    RuntimeTraceContract,
)


# ---------------------------------------------------------------------------
# Variant requirements
# ---------------------------------------------------------------------------

def test_v0_9_requires_all_8_variants():
    result = check_v0_9_methodology_gate(
        configured_variants=[],
        configured_artifacts=[],
    )
    assert not result.is_valid
    assert len(result.errors) >= 2  # at least missing variants + missing artifacts


def test_all_variants_present_blocks_none_missing():
    result = check_v0_9_methodology_gate(
        configured_variants=list(V0_9_REQUIRED_VARIANTS),
        configured_artifacts=list(V0_9_REQUIRED_ARTIFACTS),
    )
    assert result.is_valid
    assert result.decision == METHODOLOGY_GUARD_READY


def test_missing_deepseek_runtime_blocks():
    variants = [v for v in V0_9_REQUIRED_VARIANTS if v != "deepseek_runtime"]
    result = check_v0_9_methodology_gate(
        configured_variants=variants,
        configured_artifacts=list(V0_9_REQUIRED_ARTIFACTS),
    )
    assert not result.is_valid
    assert any("deepseek_runtime" in e for e in result.errors)


def test_missing_calibrated_runtime_blocks():
    variants = [v for v in V0_9_REQUIRED_VARIANTS if "calibrated" not in v]
    result = check_v0_9_methodology_gate(
        configured_variants=variants,
        configured_artifacts=list(V0_9_REQUIRED_ARTIFACTS),
    )
    assert not result.is_valid
    assert any("calibrated" in e.lower() for e in result.errors)


def test_missing_any_single_variant_blocks():
    for missing in V0_9_REQUIRED_VARIANTS:
        variants = [v for v in V0_9_REQUIRED_VARIANTS if v != missing]
        result = check_v0_9_methodology_gate(
            configured_variants=variants,
            configured_artifacts=list(V0_9_REQUIRED_ARTIFACTS),
        )
        assert not result.is_valid
        assert any(missing in e for e in result.errors)


# ---------------------------------------------------------------------------
# Artifact requirements
# ---------------------------------------------------------------------------

def test_missing_runtime_traces_blocks():
    artifacts = [a for a in V0_9_REQUIRED_ARTIFACTS if a != "runtime_traces.jsonl"]
    result = check_v0_9_methodology_gate(
        configured_variants=list(V0_9_REQUIRED_VARIANTS),
        configured_artifacts=artifacts,
    )
    assert not result.is_valid
    assert any("runtime_traces" in e for e in result.errors)


def test_missing_calibration_traces_blocks():
    artifacts = [a for a in V0_9_REQUIRED_ARTIFACTS if a != "calibration_traces.jsonl"]
    result = check_v0_9_methodology_gate(
        configured_variants=list(V0_9_REQUIRED_VARIANTS),
        configured_artifacts=artifacts,
    )
    assert not result.is_valid
    assert any("calibration_traces" in e for e in result.errors)


def test_missing_audit_decisions_blocks():
    artifacts = [a for a in V0_9_REQUIRED_ARTIFACTS if a != "audit_decisions.jsonl"]
    result = check_v0_9_methodology_gate(
        configured_variants=list(V0_9_REQUIRED_VARIANTS),
        configured_artifacts=artifacts,
    )
    assert not result.is_valid
    assert any("audit_decisions" in e for e in result.errors)


def test_missing_repair_attempts_blocks():
    artifacts = [a for a in V0_9_REQUIRED_ARTIFACTS if a != "repair_attempts.jsonl"]
    result = check_v0_9_methodology_gate(
        configured_variants=list(V0_9_REQUIRED_VARIANTS),
        configured_artifacts=artifacts,
    )
    assert not result.is_valid
    assert any("repair_attempts" in e for e in result.errors)


# ---------------------------------------------------------------------------
# Expected executions
# ---------------------------------------------------------------------------

def test_expected_executions_must_be_240():
    config = build_v0_9_methodology_contract(
        has_runtime_traces=True,
        has_calibration_traces=True,
    )
    assert config.expected_top_level_executions == 240


def test_gate_blocks_wrong_execution_count():
    config = build_v0_9_methodology_contract(
        has_runtime_traces=True,
        has_calibration_traces=True,
    )
    # Swap to wrong count
    import dataclasses
    bad_config = dataclasses.replace(config, expected_top_level_executions=180)
    result = check_v0_9_methodology_gate(
        config=bad_config,
        configured_variants=list(V0_9_REQUIRED_VARIANTS),
        configured_artifacts=list(V0_9_REQUIRED_ARTIFACTS),
    )
    assert not result.is_valid
    assert any("240" in e for e in result.errors)


# ---------------------------------------------------------------------------
# Guard ready decision
# ---------------------------------------------------------------------------

def test_guard_ready_only_when_all_requirements_met():
    result = check_v0_9_methodology_gate(
        configured_variants=list(V0_9_REQUIRED_VARIANTS),
        configured_artifacts=list(V0_9_REQUIRED_ARTIFACTS),
    )
    assert result.is_valid
    assert result.decision == METHODOLOGY_GUARD_READY
    assert len(result.errors) == 0


def test_guard_blocks_when_nothing_configured():
    result = check_v0_9_methodology_gate()
    assert not result.is_valid
    assert result.decision == METHODOLOGY_GUARD_BLOCKED
    assert len(result.errors) > 0


# ---------------------------------------------------------------------------
# Runtime trace validation via methodology guard
# ---------------------------------------------------------------------------

def test_validate_runtime_trace_via_gate():
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
    result = validate_v0_9_runtime_trace(trace)
    assert result.is_valid


def test_validate_calibrated_runtime_trace_via_gate():
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
    result = validate_v0_9_calibrated_runtime_trace(trace, cal)
    assert result.is_valid


# ---------------------------------------------------------------------------
# No provider calls in tests
# ---------------------------------------------------------------------------

def test_no_provider_calls():
    """Verify that test infrastructure does not trigger live providers."""
    from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift import RuntimeConfig
    config = RuntimeConfig()
    assert config.environ.get("FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM") != "true"


def test_contract_artifact_exists():
    from pathlib import Path
    doc = Path("docs/methodology/XENDRIS_FOUNDATIONAL_RUNTIME_CONTRACT.md")
    assert doc.exists()
