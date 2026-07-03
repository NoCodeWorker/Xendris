"""Generate claim permission updates for v4.1."""

from __future__ import annotations

from phyng.model_comparison.schemas import ClaimPermissionUpdate


def build_claim_permission_update() -> ClaimPermissionUpdate:
    """Build the official claim permission update for v4.1 model comparison."""
    return ClaimPermissionUpdate(
        update_id="PHI-GRADIENT-CLAIM-PERMISSION-v4_1",
        source_pressure_ref="data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json",
        benchmark_ref="data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json",
        debt_ref="data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json",
        model_comparison_ref="data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json",
        allowed_claims=[
            "A debt-bounded benchmark comparison was performed.",
            "Candidate behavior was compared against source-pressure-derived benchmark rows.",
            "SLOT_4 debt remained enforced during comparison.",
            "Negative controls were applied or queued.",
        ],
        blocked_claims=[
            "PHI_GRADIENT is validated.",
            "PHI_GRADIENT has predictive gain.",
            "Gradient mechanism is supported.",
            "Frontera C is validated.",
            "Invariant is empirically confirmed.",
        ],
        conditional_claims=[
            "Candidate may be benchmark-actionable if comparison score survives negative controls.",
        ],
        physical_claim_permission="BLOCKED",  # Hardcoded BLOCKED
        gradient_mechanism_claim_permission="BLOCKED_BY_SLOT4_DEBT",  # Hardcoded BLOCKED_BY_SLOT4_DEBT
        benchmark_claim_permission="BENCHMARK_COMPARISON_PERFORMED_LIMITED",
        next_required_gate="v4.2 — Observable Dataset Normalization & Real y_true Acquisition Plan",
    )
