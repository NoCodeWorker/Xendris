"""Methodology types for Xendris foundational contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ExecutionMethod(str, Enum):
    BASE = "BASE"
    WRAPPER = "WRAPPER"
    RUNTIME = "RUNTIME"
    CALIBRATED_RUNTIME = "CALIBRATED_RUNTIME"


class RuntimePhase(str, Enum):
    INITIAL_GENERATION = "INITIAL_GENERATION"
    DETERMINISTIC_AUDIT = "DETERMINISTIC_AUDIT"
    AUDIT_DECISION = "AUDIT_DECISION"
    REPAIR_OR_DEGRADE_OR_BLOCK = "REPAIR_OR_DEGRADE_OR_BLOCK"
    FINAL_RESPONSE_SELECTION = "FINAL_RESPONSE_SELECTION"
    FINAL_AUDIT = "FINAL_AUDIT"


class CalibrationPhase(str, Enum):
    CLAIM_CLASSIFICATION = "CLAIM_CLASSIFICATION"
    EVIDENCE_STATUS_RESOLUTION = "EVIDENCE_STATUS_RESOLUTION"
    CONFIDENCE_BANDING = "CONFIDENCE_BANDING"
    ALLOWED_LANGUAGE_SELECTION = "ALLOWED_LANGUAGE_SELECTION"
    BLOCKED_LANGUAGE_SELECTION = "BLOCKED_LANGUAGE_SELECTION"
    FINAL_CALIBRATED_RESPONSE = "FINAL_CALIBRATED_RESPONSE"


class AuditDecision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_LIMITATIONS = "ALLOW_WITH_LIMITATIONS"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    BLOCK = "BLOCK"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


class ClaimStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    DIAGNOSTIC_ONLY = "DIAGNOSTIC_ONLY"
    HYPOTHESIS = "HYPOTHESIS"
    UNSUPPORTED = "UNSUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"


@dataclass
class RuntimeTraceContract:
    task_id: str
    provider_name: str
    variant_name: str
    execution_method: ExecutionMethod
    initial_response_present: bool = False
    deterministic_audit_present: bool = False
    audit_decision_present: bool = False
    repair_or_degrade_or_block_considered: bool = False
    final_response_present: bool = False
    final_audit_present: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "provider_name": self.provider_name,
            "variant_name": self.variant_name,
            "execution_method": self.execution_method.value,
            "initial_response_present": self.initial_response_present,
            "deterministic_audit_present": self.deterministic_audit_present,
            "audit_decision_present": self.audit_decision_present,
            "repair_or_degrade_or_block_considered": self.repair_or_degrade_or_block_considered,
            "final_response_present": self.final_response_present,
            "final_audit_present": self.final_audit_present,
        }


@dataclass
class CalibrationTraceContract:
    claim_classification_present: bool = False
    evidence_status_present: bool = False
    confidence_band_present: bool = False
    allowed_language_present: bool = False
    blocked_language_present: bool = False
    final_calibrated_response_present: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_classification_present": self.claim_classification_present,
            "evidence_status_present": self.evidence_status_present,
            "confidence_band_present": self.confidence_band_present,
            "allowed_language_present": self.allowed_language_present,
            "blocked_language_present": self.blocked_language_present,
            "final_calibrated_response_present": self.final_calibrated_response_present,
        }


@dataclass
class MethodologyContract:
    experiment_type: str
    execution_methods: list[ExecutionMethod]
    has_runtime_traces: bool = False
    has_calibration_traces: bool = False
    has_runtime_variants: bool = False
    has_calibrated_runtime_variants: bool = False
    expected_top_level_executions: int = 0
    variant_names: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_type": self.experiment_type,
            "execution_methods": [m.value for m in self.execution_methods],
            "has_runtime_traces": self.has_runtime_traces,
            "has_calibration_traces": self.has_calibration_traces,
            "has_runtime_variants": self.has_runtime_variants,
            "has_calibrated_runtime_variants": self.has_calibrated_runtime_variants,
            "expected_top_level_executions": self.expected_top_level_executions,
            "variant_names": self.variant_names,
        }


@dataclass
class MethodologyValidationResult:
    is_valid: bool
    decision: str = "METHODOLOGY_GUARD_BLOCKED"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "decision": self.decision,
            "errors": self.errors,
            "warnings": self.warnings,
        }
