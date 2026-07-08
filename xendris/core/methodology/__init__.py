"""Xendris Foundational Methodology Contract.

Enforces that Xendris Runtime and Xendris Calibrated Runtime
are never silently degraded into prompt wrappers.
"""

from .methodology_types import (
    AuditDecision,
    CalibrationPhase,
    CalibrationTraceContract,
    ClaimStatus,
    ExecutionMethod,
    MethodologyContract,
    MethodologyValidationResult,
    RuntimePhase,
    RuntimeTraceContract,
)
from .methodology_guard import (
    validate_benchmark_methodology_config,
    validate_calibrated_runtime_trace,
    validate_runtime_trace,
)
from .runtime_contract import (
    RUNTIME_CONTRACT_FINAL_DECISION,
    RUNTIME_REQUIRED_ARTIFACTS,
    CALIBRATED_RUNTIME_REQUIRED_ARTIFACTS,
    FORBIDDEN_SUBSTITUTIONS,
    get_methodology_doctrine_summary,
)
