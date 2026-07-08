"""Benchmark methodology gate for v0.9 runtime paired lift.

Requires all 8 variants (base, wrapper, runtime, calibrated_runtime for each provider),
runtime traces, calibration traces, audit decisions, repair attempts artifacts.
"""

from __future__ import annotations

from typing import Any

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

METHODOLOGY_GUARD_READY = "METHODOLOGY_GUARD_READY"
METHODOLOGY_GUARD_BLOCKED = "METHODOLOGY_GUARD_BLOCKED"


V0_9_REQUIRED_VARIANTS = [
    "deepseek_base",
    "deepseek_wrapper",
    "deepseek_runtime",
    "deepseek_calibrated_runtime",
    "openai_base",
    "openai_wrapper",
    "openai_runtime",
    "openai_calibrated_runtime",
]

V0_9_REQUIRED_EXECUTION_METHODS = [
    ExecutionMethod.BASE,
    ExecutionMethod.WRAPPER,
    ExecutionMethod.RUNTIME,
    ExecutionMethod.CALIBRATED_RUNTIME,
]

V0_9_REQUIRED_ARTIFACTS = [
    "runtime_traces.jsonl",
    "calibration_traces.jsonl",
    "audit_decisions.jsonl",
    "repair_attempts.jsonl",
]


def build_v0_9_methodology_contract(
    has_runtime_traces: bool = False,
    has_calibration_traces: bool = False,
    variant_names: list[str] | None = None,
) -> MethodologyContract:
    return MethodologyContract(
        experiment_type="runtime_paired_lift",
        execution_methods=list(V0_9_REQUIRED_EXECUTION_METHODS),
        has_runtime_traces=has_runtime_traces,
        has_calibration_traces=has_calibration_traces,
        has_runtime_variants=True,
        has_calibrated_runtime_variants=True,
        expected_top_level_executions=240,
        variant_names=variant_names or list(V0_9_REQUIRED_VARIANTS),
    )


def check_v0_9_methodology_gate(
    config: MethodologyContract | None = None,
    configured_variants: list[str] | None = None,
    configured_artifacts: list[str] | None = None,
) -> MethodologyValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    variants = configured_variants or (config.variant_names if config else [])
    artifacts = configured_artifacts or []

    # Check all 8 required variants present
    for required in V0_9_REQUIRED_VARIANTS:
        if required not in variants:
            errors.append(f"missing required variant: {required}")

    # Check for runtime variants
    has_runtime = any("runtime" in v and "calibrated" not in v for v in variants)
    if not has_runtime:
        errors.append("runtime variants are absent - at least one of deepseek_runtime/openai_runtime required")

    # Check for calibrated runtime variants
    has_calibrated = any("calibrated" in v for v in variants)
    if not has_calibrated:
        errors.append("calibrated runtime variants are absent")

    # Check required artifacts
    for artifact in V0_9_REQUIRED_ARTIFACTS:
        if artifact not in artifacts:
            errors.append(f"missing required artifact: {artifact}")

    # Top-level executions check
    if config and config.expected_top_level_executions != 240:
        errors.append(
            f"expected_top_level_executions must be 240, got {config.expected_top_level_executions}"
        )

    decision = METHODOLOGY_GUARD_READY if not errors else METHODOLOGY_GUARD_BLOCKED
    return MethodologyValidationResult(
        is_valid=not errors,
        decision=decision,
        errors=errors,
        warnings=warnings,
    )


def validate_v0_9_runtime_trace(
    trace: RuntimeTraceContract,
) -> MethodologyValidationResult:
    return validate_runtime_trace(trace)


def validate_v0_9_calibrated_runtime_trace(
    trace: RuntimeTraceContract,
    calibration_trace: CalibrationTraceContract | None,
) -> MethodologyValidationResult:
    return validate_calibrated_runtime_trace(trace, calibration_trace)
