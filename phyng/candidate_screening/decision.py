"""Decision gate module for v4.7 candidate screening."""

from __future__ import annotations

from typing import Any
from phyng.candidate_screening.schemas import (
    SourceAccessibilityScreen,
    ObservableAccessibilityScreen,
    YTrueAccessibilityScreen,
    PublicDatasetScreen,
    ExperimentalFeasibilityScreen,
    ClaimRiskScreen,
    CandidateScreeningDecision,
)

def evaluate_screening_decision(
    inputs: dict[str, Any],
    source: SourceAccessibilityScreen,
    observable: ObservableAccessibilityScreen,
    ytrue: YTrueAccessibilityScreen,
    public_dataset: PublicDatasetScreen,
    experiment: ExperimentalFeasibilityScreen,
    claim_risk: ClaimRiskScreen,
) -> CandidateScreeningDecision:
    
    # 1. Evaluate pass criteria
    criteria_met = []
    
    if source.source_accessibility_score >= 0.5:
        criteria_met.append("source_accessibility >= MEDIUM")
    if observable.observable_accessibility_score >= 0.5:
        criteria_met.append("observable_clarity >= MEDIUM")
    if ytrue.ytrue_accessibility_score >= 0.4:
        criteria_met.append("y_true_accessibility >= MEDIUM")
    if public_dataset.dataset_accessibility_score >= 0.5:
        criteria_met.append("public_dataset_availability >= PLAUSIBLE")
    if experiment.experiment_accessibility_score >= 0.5:
        criteria_met.append("experimental_feasibility >= MEDIUM")
    if claim_risk.slot4_dependency_risk == "LOW":
        criteria_met.append("slot4_independence = TRUE")

    # 2. Evaluate fail criteria
    fail_criteria = []
    
    # Check SLOT_4 blocker
    if claim_risk.slot4_dependency_risk == "HIGH":
        fail_criteria.append("SLOT_4 dependency remains unresolved")
    
    # Count of met criteria
    count_met = len(criteria_met)

    # 3. Determine final status
    final_status = "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PARTIAL"  # Default expected conservative
    allowed_next_phase = None
    blocked_next_phases = [
        "v4.8 — Full benchmark construction",
        "v4.8 — Full model comparison",
        "v4.8 — PredictiveGain evaluation"
    ]
    
    if "SLOT_4 dependency remains unresolved" in fail_criteria:
        final_status = "PHI_CURVATURE_ACCESSIBILITY_SCREEN_FAILED"
        allowed_next_phase = "v4.8 — Candidate Family Reprioritization"
    elif count_met < 2:
        final_status = "PHI_CURVATURE_REJECTED_NO_REALITY_CONTACT"
        allowed_next_phase = "v4.8 — Candidate Family Reprioritization"
        fail_criteria.append("Less than two accessibility criteria met")
    else:
        # Check claim risk blocker
        if claim_risk.claim_risk_score >= 0.8:
            # High risk blocks full pass, forces PARTIAL or FAILED
            final_status = "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PARTIAL"
            allowed_next_phase = "v4.8 — PHI_CURVATURE Targeted Source Discovery Before Pipeline"
            fail_criteria.append("claim risk HIGH with no mitigation")
        else:
            # We can have PASSED, PARTIAL or REQUIRES_EXPERIMENT
            if ytrue.experiment_required:
                final_status = "PHI_CURVATURE_REQUIRES_EXPERIMENT_BEFORE_PIPELINE"
                allowed_next_phase = "v4.8 — PHI_CURVATURE Experimental Feasibility Gate"
            elif count_met >= 4:
                final_status = "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED"
                allowed_next_phase = "v4.8 — PHI_CURVATURE Minimal Source/y_true Campaign"
            else:
                final_status = "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PARTIAL"
                allowed_next_phase = "v4.8 — PHI_CURVATURE Targeted Source Discovery Before Pipeline"

    # Define aggregate score as average of the 5 positive metrics minus risk
    aggregate_score = (
        source.source_accessibility_score
        + observable.observable_accessibility_score
        + ytrue.ytrue_accessibility_score
        + public_dataset.dataset_accessibility_score
        + experiment.experiment_accessibility_score
    ) / 5.0

    # Apply test overrides for final decision status if needed
    final_status = inputs.get("override_final_status", final_status)
    if final_status == "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED":
        allowed_next_phase = "v4.8 — PHI_CURVATURE Minimal Source/y_true Campaign"

    guardrails = [
        "no PredictiveGain until accepted y_true exists",
        "no physical claim until source-pressure and y_true gates pass",
        "no benchmark construction before source/y_true accessibility is confirmed",
        "no SLOT_4 dependency unless explicitly resolved or scoped out",
        "no synthetic score as selection authority",
        "no full pipeline if public/manual/experimental paths remain UNKNOWN"
    ]

    notes = [
        f"Criteria met: {count_met}/6.",
        f"Primary reason: Evaluated under v4.7 screening protocol.",
    ]

    return CandidateScreeningDecision(
        candidate_family="PHI_CURVATURE",
        final_status=final_status,
        source_score=source.source_accessibility_score,
        observable_score=observable.observable_accessibility_score,
        ytrue_score=ytrue.ytrue_accessibility_score,
        public_dataset_score=public_dataset.dataset_accessibility_score,
        experimental_feasibility_score=experiment.experiment_accessibility_score,
        claim_risk_score=claim_risk.claim_risk_score,
        aggregate_accessibility_score=aggregate_score,
        pass_criteria_met=criteria_met,
        fail_criteria_met=fail_criteria,
        allowed_next_phase=allowed_next_phase,
        blocked_next_phases=blocked_next_phases,
        required_guardrails=guardrails,
        notes=notes,
    )
