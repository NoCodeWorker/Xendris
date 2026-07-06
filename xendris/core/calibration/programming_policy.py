"""Programming intervention calibration policy.

This policy encodes a lesson from Programming Reliability v0.1: local
interventions can help or harm depending on category and execution mode.
It is deterministic and non-invasive. It does not rewrite code, call models,
or change benchmark scores.
"""

from __future__ import annotations

from xendris.core.calibration.audit import CalibrationAudit, CalibrationMetrics
from xendris.core.calibration.domain import Domain, ExecutionMode, ProgrammingCategory
from xendris.core.calibration.intervention import InterventionDecision, InterventionLevel


class ProgrammingInterventionPolicy:
    """Deterministic policy for programming-domain intervention strength."""

    domain = Domain.PROGRAMMING

    def decide(
        self,
        category: ProgrammingCategory | str | None,
        execution_mode: ExecutionMode | str,
    ) -> InterventionDecision:
        """Return a conservative intervention decision for a programming task."""
        resolved_category = _resolve_programming_category(category)
        resolved_mode = _resolve_execution_mode(execution_mode)

        if resolved_category == ProgrammingCategory.API_CONTRACTS and resolved_mode in {
            ExecutionMode.BENCHMARK_EXECUTION,
            ExecutionMode.CODE_SANDBOX,
        }:
            return _decision(
                category=resolved_category,
                execution_mode=resolved_mode,
                intervention_level=InterventionLevel.MINIMAL,
                preserve_signature=True,
                allow_extra_imports=False,
                allow_runtime_type_checks=False,
                allow_test_framework_imports=False,
                prefer_minimal_patch=True,
                require_security_scan=False,
                rationale=(
                    "API contract benchmark tasks are harmed by import-heavy or "
                    "signature-changing interventions; preserve the public contract."
                ),
            )

        if resolved_category == ProgrammingCategory.EDGE_CASES:
            return _decision(
                category=resolved_category,
                execution_mode=resolved_mode,
                intervention_level=InterventionLevel.MODERATE,
                preserve_signature=True,
                allow_extra_imports=False,
                allow_runtime_type_checks=True,
                allow_test_framework_imports=False,
                prefer_minimal_patch=True,
                require_security_scan=False,
                rationale=(
                    "Edge cases benefit from moderate local checks, but extra imports "
                    "remain disabled by default in benchmark sandboxes."
                ),
                warnings=("Runtime type checks must not require imports in restricted sandboxes.",),
            )

        if resolved_category == ProgrammingCategory.UNIT_TESTS and resolved_mode == ExecutionMode.CODE_SANDBOX:
            return _decision(
                category=resolved_category,
                execution_mode=resolved_mode,
                intervention_level=InterventionLevel.MINIMAL,
                preserve_signature=True,
                allow_extra_imports=False,
                allow_runtime_type_checks=False,
                allow_test_framework_imports=False,
                prefer_minimal_patch=True,
                require_security_scan=False,
                rationale=(
                    "Code sandbox unit-test tasks should prefer plain asserts and avoid "
                    "pytest or import-heavy generated tests unless explicitly allowed."
                ),
                warnings=("Prefer plain assert tests; pytest imports are disabled by default.",),
            )

        if resolved_category == ProgrammingCategory.SECURITY_BASICS:
            return _decision(
                category=resolved_category,
                execution_mode=resolved_mode,
                intervention_level=(
                    InterventionLevel.STRONG
                    if resolved_mode in {ExecutionMode.PRODUCTION, ExecutionMode.SECURITY_REVIEW}
                    else InterventionLevel.MODERATE
                ),
                preserve_signature=True,
                allow_extra_imports=False,
                allow_runtime_type_checks=True,
                allow_test_framework_imports=False,
                prefer_minimal_patch=True,
                require_security_scan=True,
                rationale=(
                    "Security tasks require scanning, but coarse sandbox pattern matching "
                    "can create false positives."
                ),
                warnings=("Coarse sandbox pattern matching can produce false-positive security risks.",),
            )

        if resolved_mode == ExecutionMode.PRODUCTION:
            return _decision(
                category=resolved_category,
                execution_mode=resolved_mode,
                intervention_level=InterventionLevel.STRONG,
                preserve_signature=True,
                allow_extra_imports=True,
                allow_runtime_type_checks=True,
                allow_test_framework_imports=False,
                prefer_minimal_patch=False,
                require_security_scan=True,
                rationale=(
                    "Production mode allows stronger checks than benchmark mode, but "
                    "explicit API contracts remain protected."
                ),
                warnings=("Production checks require deployment and test evidence before public claims.",),
            )

        return _decision(
            category=resolved_category,
            execution_mode=resolved_mode,
            intervention_level=InterventionLevel.MINIMAL,
            preserve_signature=True,
            allow_extra_imports=False,
            allow_runtime_type_checks=False,
            allow_test_framework_imports=False,
            prefer_minimal_patch=True,
            require_security_scan=False,
            rationale=(
                "Unknown or neutral programming category defaults to minimal "
                "intervention to avoid overengineering and benchmark contamination."
            ),
            warnings=("Unknown category: defaulted to conservative minimal intervention.",),
        )

    def audit(
        self,
        category: ProgrammingCategory | str | None,
        execution_mode: ExecutionMode | str,
        metrics: CalibrationMetrics | None = None,
    ) -> CalibrationAudit:
        """Return an audit object for the deterministic policy decision."""
        decision = self.decide(category, execution_mode)
        return CalibrationAudit(
            decision=decision,
            rationale=decision.rationale,
            metrics=metrics or CalibrationMetrics(),
            notes=("No intervention without domain-calibrated benefit.",),
        )


def _decision(
    *,
    category: ProgrammingCategory | str,
    execution_mode: ExecutionMode,
    intervention_level: InterventionLevel,
    preserve_signature: bool,
    allow_extra_imports: bool,
    allow_runtime_type_checks: bool,
    allow_test_framework_imports: bool,
    prefer_minimal_patch: bool,
    require_security_scan: bool,
    rationale: str,
    warnings: tuple[str, ...] = (),
) -> InterventionDecision:
    return InterventionDecision(
        domain=Domain.PROGRAMMING,
        category=category,
        execution_mode=execution_mode,
        intervention_level=intervention_level,
        preserve_signature=preserve_signature,
        allow_extra_imports=allow_extra_imports,
        allow_runtime_type_checks=allow_runtime_type_checks,
        allow_test_framework_imports=allow_test_framework_imports,
        prefer_minimal_patch=prefer_minimal_patch,
        require_security_scan=require_security_scan,
        rationale=rationale,
        warnings=warnings,
    )


def _resolve_programming_category(category: ProgrammingCategory | str | None) -> ProgrammingCategory | str:
    if isinstance(category, ProgrammingCategory):
        return category
    if category is None:
        return "UNKNOWN"
    normalized = str(category).strip().upper()
    try:
        return ProgrammingCategory(normalized)
    except ValueError:
        try:
            return ProgrammingCategory[normalized]
        except KeyError:
            return normalized or "UNKNOWN"


def _resolve_execution_mode(execution_mode: ExecutionMode | str) -> ExecutionMode:
    if isinstance(execution_mode, ExecutionMode):
        return execution_mode
    normalized = str(execution_mode).strip().upper()
    try:
        return ExecutionMode(normalized)
    except ValueError:
        try:
            return ExecutionMode[normalized]
        except KeyError:
            return ExecutionMode.EXPLORATION


__all__ = ["ProgrammingInterventionPolicy"]
