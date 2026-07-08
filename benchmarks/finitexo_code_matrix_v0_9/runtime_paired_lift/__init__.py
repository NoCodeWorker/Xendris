"""Finitexo Code Matrix v0.9.0 — Runtime Paired Lift (n=30).

Restores foundational Xendris runtime methodology after wrapper-only deviations
in v0.7.0 and v0.8.1.
"""

from .runtime_lift_audit import build_repair_prompt, run_audit
from .runtime_lift_config import RuntimeConfig, RuntimeVariantSpec, validate_run_id_suffix
from .runtime_lift_gate import RuntimePreflight, evaluate_runtime_preflight
from .runtime_lift_report import build_runtime_lift_report
from .runtime_lift_runner import (
    BLOCKED_BUDGET,
    BLOCKED_PREFLIGHT,
    COMPLETED,
    PARTIAL,
    run_runtime_paired_lift,
    write_runtime_lift_artifacts,
)
from .runtime_lift_scoring import (
    FAMILIES,
    aggregate_by_family_variant,
    aggregate_by_variant,
    compute_audit_decision_distribution,
    compute_family_lift,
    compute_paired_lift,
    compute_repair_metrics,
    score_runtime_response,
)
from .runtime_lift_types import (
    AUDIT_COMPONENTS,
    RuntimeAuditDecision,
    RuntimeAuditResult,
    RuntimeScoredRecord,
    RuntimeTrace,
    RuntimeVariantAggregate,
)
