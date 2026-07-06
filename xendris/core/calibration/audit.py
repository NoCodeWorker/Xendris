"""Audit structures for deterministic intervention calibration."""

from __future__ import annotations

from dataclasses import dataclass, field

from xendris.core.calibration.intervention import InterventionDecision


@dataclass(frozen=True)
class CalibrationMetrics:
    """Aggregate calibration metrics, when supplied by measured fixtures."""

    intervention_gain_rate: float | None = None
    intervention_harm_rate: float | None = None
    false_positive_security_rate: float | None = None
    sandbox_import_failure_rate: float | None = None
    overengineering_failure_rate: float | None = None
    minimal_solution_preservation_rate: float | None = None
    domain_calibration_score: float | None = None

    def to_dict(self) -> dict[str, float | None]:
        """Return a JSON-compatible representation."""
        return {
            "intervention_gain_rate": self.intervention_gain_rate,
            "intervention_harm_rate": self.intervention_harm_rate,
            "false_positive_security_rate": self.false_positive_security_rate,
            "sandbox_import_failure_rate": self.sandbox_import_failure_rate,
            "overengineering_failure_rate": self.overengineering_failure_rate,
            "minimal_solution_preservation_rate": self.minimal_solution_preservation_rate,
            "domain_calibration_score": self.domain_calibration_score,
        }


@dataclass(frozen=True)
class CalibrationAudit:
    """Audit object recording a calibration decision and its rationale."""

    decision: InterventionDecision
    rationale: str
    metrics: CalibrationMetrics = field(default_factory=CalibrationMetrics)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        return {
            "decision": {
                "domain": self.decision.domain.value,
                "category": (
                    self.decision.category.value
                    if hasattr(self.decision.category, "value")
                    else str(self.decision.category)
                ),
                "execution_mode": self.decision.execution_mode.value,
                "intervention_level": self.decision.intervention_level.value,
                "preserve_signature": self.decision.preserve_signature,
                "allow_extra_imports": self.decision.allow_extra_imports,
                "allow_runtime_type_checks": self.decision.allow_runtime_type_checks,
                "allow_test_framework_imports": self.decision.allow_test_framework_imports,
                "prefer_minimal_patch": self.decision.prefer_minimal_patch,
                "require_security_scan": self.decision.require_security_scan,
                "rationale": self.decision.rationale,
                "warnings": list(self.decision.warnings),
            },
            "rationale": self.rationale,
            "metrics": self.metrics.to_dict(),
            "notes": list(self.notes),
        }


__all__ = ["CalibrationAudit", "CalibrationMetrics"]
