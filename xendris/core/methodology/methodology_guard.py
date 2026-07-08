"""Methodology guard functions for Xendris foundational contract."""

from __future__ import annotations

from .methodology_types import (
    AuditDecision,
    CalibrationPhase,
    ClaimStatus,
    ExecutionMethod,
    MethodologyContract,
    MethodologyValidationResult,
    RuntimePhase,
    RuntimeTraceContract,
    CalibrationTraceContract,
)


METHODOLOGY_GUARD_READY = "METHODOLOGY_GUARD_READY"
METHODOLOGY_GUARD_BLOCKED = "METHODOLOGY_GUARD_BLOCKED"

RUNTIME_REQUIRED_PHASES = {
    RuntimePhase.INITIAL_GENERATION,
    RuntimePhase.DETERMINISTIC_AUDIT,
    RuntimePhase.AUDIT_DECISION,
    RuntimePhase.REPAIR_OR_DEGRADE_OR_BLOCK,
    RuntimePhase.FINAL_RESPONSE_SELECTION,
    RuntimePhase.FINAL_AUDIT,
}

CALIBRATION_REQUIRED_PHASES = {
    CalibrationPhase.CLAIM_CLASSIFICATION,
    CalibrationPhase.EVIDENCE_STATUS_RESOLUTION,
    CalibrationPhase.CONFIDENCE_BANDING,
    CalibrationPhase.ALLOWED_LANGUAGE_SELECTION,
    CalibrationPhase.BLOCKED_LANGUAGE_SELECTION,
    CalibrationPhase.FINAL_CALIBRATED_RESPONSE,
}


def validate_runtime_trace(trace: RuntimeTraceContract) -> MethodologyValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    method = trace.execution_method
    name_lower = trace.variant_name.lower()

    # If named "runtime" but method is BASE or WRAPPER
    if "runtime" in name_lower and method in (ExecutionMethod.BASE, ExecutionMethod.WRAPPER):
        errors.append(
            f"variant '{trace.variant_name}' contains 'runtime' but execution_method is {method.value}"
        )

    # If method is RUNTIME or CALIBRATED_RUNTIME, require runtime phases
    if method in (ExecutionMethod.RUNTIME, ExecutionMethod.CALIBRATED_RUNTIME):
        if not trace.initial_response_present:
            errors.append("missing initial_response for runtime variant")
        if not trace.deterministic_audit_present:
            errors.append("missing deterministic_audit for runtime variant")
        if not trace.audit_decision_present:
            errors.append("missing audit_decision for runtime variant")
        if not trace.repair_or_degrade_or_block_considered:
            errors.append("missing repair_or_degrade_or_block_consideration for runtime variant")
        if not trace.final_response_present:
            errors.append("missing final_response for runtime variant")
        if not trace.final_audit_present:
            errors.append("missing final_audit for runtime variant")

    # If method is BASE or WRAPPER, runtime phases are not required
    if method in (ExecutionMethod.BASE, ExecutionMethod.WRAPPER):
        if trace.deterministic_audit_present or trace.audit_decision_present:
            warnings.append(
                f"variant '{trace.variant_name}' has runtime audit fields but method is {method.value} - audit fields will be ignored"
            )

    decision = METHODOLOGY_GUARD_READY if not errors else METHODOLOGY_GUARD_BLOCKED
    return MethodologyValidationResult(
        is_valid=not errors,
        decision=decision,
        errors=errors,
        warnings=warnings,
    )


def validate_calibrated_runtime_trace(
    trace: RuntimeTraceContract,
    calibration_trace: CalibrationTraceContract | None,
) -> MethodologyValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    # First validate the runtime portion
    runtime_result = validate_runtime_trace(trace)
    errors.extend(runtime_result.errors)
    warnings.extend(runtime_result.warnings)

    method = trace.execution_method
    name_lower = trace.variant_name.lower()

    # If named "calibrated" but method is not CALIBRATED_RUNTIME
    if "calibrated" in name_lower and method != ExecutionMethod.CALIBRATED_RUNTIME:
        errors.append(
            f"variant '{trace.variant_name}' contains 'calibrated' but execution_method is {method.value}"
        )

    if method == ExecutionMethod.CALIBRATED_RUNTIME:
        if calibration_trace is None:
            errors.append("missing calibration_trace for CALIBRATED_RUNTIME variant")
        else:
            if not calibration_trace.claim_classification_present:
                errors.append("missing claim_classification for calibrated runtime")
            if not calibration_trace.evidence_status_present:
                errors.append("missing evidence_status for calibrated runtime")
            if not calibration_trace.confidence_band_present:
                errors.append("missing confidence_band for calibrated runtime")
            if not calibration_trace.allowed_language_present:
                errors.append("missing allowed_language for calibrated runtime")
            if not calibration_trace.blocked_language_present:
                errors.append("missing blocked_language for calibrated runtime")
            if not calibration_trace.final_calibrated_response_present:
                errors.append("missing final_calibrated_response for calibrated runtime")

    decision = METHODOLOGY_GUARD_READY if not errors else METHODOLOGY_GUARD_BLOCKED
    return MethodologyValidationResult(
        is_valid=not errors,
        decision=decision,
        errors=errors,
        warnings=warnings,
    )


def validate_benchmark_methodology_config(config: MethodologyContract) -> MethodologyValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    variant_names_lower = [v.lower() for v in config.variant_names]

    has_runtime_variant = any("runtime" in v for v in variant_names_lower)
    has_calibrated_runtime_variant = any("calibrated" in v and "runtime" in v for v in variant_names_lower)

    # Config claims runtime but has no runtime variants
    if config.has_runtime_variants and not has_runtime_variant:
        errors.append("config claims has_runtime_variants but no variant contains 'runtime'")
    if config.has_calibrated_runtime_variants and not has_calibrated_runtime_variant:
        errors.append("config claims has_calibrated_runtime_variants but no variant contains 'calibrated'")

    # If experiment is about runtime, must have runtime variants
    if "runtime" in config.experiment_type.lower() and not has_runtime_variant:
        errors.append(
            f"experiment_type '{config.experiment_type}' references runtime but no runtime variant configured"
        )

    # Runtime benchmarks must not only have base/wrapper
    if "runtime" in config.experiment_type.lower():
        methods = set(config.execution_methods)
        if methods <= {ExecutionMethod.BASE, ExecutionMethod.WRAPPER}:
            errors.append(
                "runtime benchmark only defines base/wrapper variants - runtime variants required"
            )

    # Calibrated runtime config requires runtime traces
    if has_calibrated_runtime_variant and not config.has_runtime_traces:
        errors.append("calibrated runtime variants require runtime_traces artifact")

    # If config has runtime variants, runtime traces are required
    if has_runtime_variant and not config.has_runtime_traces:
        errors.append("runtime variants require runtime_traces artifact")

    # If config has calibrated runtime variants, calibration traces required
    if has_calibrated_runtime_variant and not config.has_calibration_traces:
        errors.append("calibrated runtime variants require calibration_traces artifact")

    # Expected top-level executions
    if config.expected_top_level_executions <= 0:
        errors.append("expected_top_level_executions must be > 0")
    elif config.expected_top_level_executions != len(config.variant_names) * 30:
        warnings.append(
            f"expected_top_level_executions ({config.expected_top_level_executions}) "
            f"does not match variants ({len(config.variant_names)}) * 30 tasks"
        )

    decision = METHODOLOGY_GUARD_READY if not errors else METHODOLOGY_GUARD_BLOCKED
    return MethodologyValidationResult(
        is_valid=not errors,
        decision=decision,
        errors=errors,
        warnings=warnings,
    )
