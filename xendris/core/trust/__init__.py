"""Xendris Trust Kernel.

Minimal deterministic core for representing and auditing answer claims.

The trust kernel does not extract claims with an LLM, retrieve sources, call
providers, or validate factual truth. It evaluates declared claims using
structural support states and conservative decision rules.
"""

from .audit import ReasoningAudit
from .benchmark_gate import (
    BenchmarkExclusionReason,
    BenchmarkGateDecision,
    BenchmarkGateResult,
    gate_benchmark_output,
)
from .benchmark_diagnostics import (
    BenchmarkSuiteDiagnostics,
    BenchmarkSuiteReadiness,
    diagnose_benchmark_suite,
)
from .claims import Claim, make_claim
from .contracts import validate_reasoning_audit
from .evidence import (
    Evidence,
    EvidenceBinding,
    EvidenceType,
    bind_evidence_to_claim,
    compute_support_score,
)
from .evaluators import TrustKernelEvaluator, evaluate_claims
from .reasoning import (
    classify_code_production_issue,
    classify_evidence_issue,
    classify_user_provided_origin,
    detect_language,
    evaluate_reasoning_transversally,
)
from .quality import (
    BenchmarkReadiness,
    QualityAction,
    QualityDimension,
    QualityImprovementPlan,
    QualityPriority,
    build_quality_improvement_plan,
    validate_quality_improvement_plan,
)
from .types import AuditDecision, ClaimStatus, ClaimType, RiskLevel

__all__ = [
    "AuditDecision",
    "BenchmarkExclusionReason",
    "BenchmarkGateDecision",
    "BenchmarkGateResult",
    "BenchmarkReadiness",
    "BenchmarkSuiteDiagnostics",
    "BenchmarkSuiteReadiness",
    "Claim",
    "ClaimStatus",
    "ClaimType",
    "Evidence",
    "EvidenceBinding",
    "EvidenceType",
    "QualityAction",
    "QualityDimension",
    "QualityImprovementPlan",
    "QualityPriority",
    "ReasoningAudit",
    "RiskLevel",
    "TrustKernelEvaluator",
    "bind_evidence_to_claim",
    "build_quality_improvement_plan",
    "compute_support_score",
    "diagnose_benchmark_suite",
    "classify_code_production_issue",
    "classify_evidence_issue",
    "classify_user_provided_origin",
    "detect_language",
    "evaluate_claims",
    "evaluate_reasoning_transversally",
    "gate_benchmark_output",
    "make_claim",
    "validate_reasoning_audit",
    "validate_quality_improvement_plan",
]
