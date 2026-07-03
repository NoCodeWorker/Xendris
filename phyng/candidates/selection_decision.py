"""Selection decision for v5.9 candidate-family screening."""

from __future__ import annotations

from phyng.candidates.schemas import CandidateLeakageRecord, CandidateRealityContactRecord, CandidateSelectionDecision


def build_selection_decision(
    screen: list[CandidateRealityContactRecord],
    leakage: list[CandidateLeakageRecord],
) -> CandidateSelectionDecision:
    passed = [record for record in screen if record.reality_contact_passed]
    blocked_leakage = {record.candidate_family_id for record in leakage if record.leakage_status == "BLOCKING"}
    blocked_missing = [record for record in screen if "has_required_features" in record.failure_reasons]
    blocked_debt = [record for record in screen if "has_no_blocking_debt" in record.failure_reasons]
    if passed:
        selected = passed[0]
        return CandidateSelectionDecision(
            final_status="CANDIDATE_FAMILY_SELECTED_FOR_PREDICTIVE_GATE",
            selected_candidate_family=selected.candidate_family_id,
            selected_rule_id=f"RULE-v5_9-{selected.candidate_family_id}",
            candidate_count=len(screen),
            passed_candidate_count=len(passed),
            rejected_candidate_count=len(screen) - len(passed),
            blocked_by_leakage_count=len(blocked_leakage),
            blocked_by_missing_features_count=len(blocked_missing),
            blocked_by_scientific_debt_count=len(blocked_debt),
            rationale="At least one active candidate family passed all v5.9 reality-contact requirements.",
            allowed_next_phase="v6.0 - Candidate Prediction Alignment & PredictiveGain Gate",
            blocked_next_phases=["Frontera C validation", "physical claim"],
        )
    status = "CANDIDATE_SELECTION_BLOCKED_BY_MISSING_FEATURES" if blocked_missing else "NO_CANDIDATE_WITH_REALITY_CONTACT"
    return CandidateSelectionDecision(
        final_status=status,
        selected_candidate_family=None,
        selected_rule_id=None,
        candidate_count=len(screen),
        passed_candidate_count=0,
        rejected_candidate_count=len(screen),
        blocked_by_leakage_count=len(blocked_leakage),
        blocked_by_missing_features_count=len(blocked_missing),
        blocked_by_scientific_debt_count=len(blocked_debt),
        rationale="No active candidate family has all required non-leaking features, prediction rule, controls, ablation plan, and debt clearance.",
        allowed_next_phase=None,
        blocked_next_phases=["v6.0 PredictiveGain gate", "negative controls", "C-structure ablation", "Frontera C validation"],
    )
