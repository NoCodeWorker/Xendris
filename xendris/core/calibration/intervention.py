"""Intervention decision types for Xendris calibration policies.

The core rule is: no intervention without domain-calibrated benefit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from xendris.core.calibration.domain import Domain, ExecutionMode, ProgrammingCategory


class InterventionLevel(str, Enum):
    """Strength of local intervention allowed by a calibration policy."""

    NONE = "NONE"
    MINIMAL = "MINIMAL"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    HUMAN_REVIEW = "HUMAN_REVIEW"


@dataclass(frozen=True)
class InterventionDecision:
    """Deterministic calibration result for a candidate intervention."""

    domain: Domain
    category: ProgrammingCategory | str
    execution_mode: ExecutionMode
    intervention_level: InterventionLevel
    preserve_signature: bool
    allow_extra_imports: bool
    allow_runtime_type_checks: bool
    allow_test_framework_imports: bool
    prefer_minimal_patch: bool
    require_security_scan: bool
    rationale: str
    warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def is_conservative(self) -> bool:
        """Return whether the decision avoids broad intervention risk."""
        return (
            self.preserve_signature
            and self.prefer_minimal_patch
            and not self.allow_test_framework_imports
            and self.intervention_level in {
                InterventionLevel.NONE,
                InterventionLevel.MINIMAL,
                InterventionLevel.MODERATE,
            }
        )


__all__ = ["InterventionDecision", "InterventionLevel"]
