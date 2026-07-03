"""Reality-contact screen for v5.9 candidate families."""

from __future__ import annotations

from phyng.candidates.schemas import (
    CandidateFamilyRecord,
    CandidateLeakageRecord,
    CandidatePredictionRule,
    CandidateRealityContactRecord,
)


def build_reality_contact_screen(
    families: list[CandidateFamilyRecord],
    rules: list[CandidatePredictionRule],
    leakage: list[CandidateLeakageRecord],
    missing_features: dict[str, list[str]],
) -> list[CandidateRealityContactRecord]:
    rule_by_id = {rule.candidate_family_id: rule for rule in rules}
    leakage_by_id = {record.candidate_family_id: record for record in leakage}
    records: list[CandidateRealityContactRecord] = []
    for family in families:
        rule = rule_by_id[family.candidate_family_id]
        leak = leakage_by_id[family.candidate_family_id]
        is_active_candidate = family.candidate_type == "C_STRUCTURE_CANDIDATE" and family.allowed_role != "baseline_comparator"
        has_features = not missing_features.get(family.candidate_family_id)
        has_rule = rule.rule_status == "READY_FOR_ALIGNMENT"
        has_no_leakage = leak.leakage_status != "BLOCKING"
        no_debt = not family.scientific_debt_blockers
        booleans = {
            "has_target_alignment": bool(family.target_observable_classes) and is_active_candidate,
            "has_required_features": has_features,
            "has_prediction_rule": has_rule,
            "has_no_leakage": has_no_leakage,
            "has_baseline_comparator": family.can_compare_to_baseline,
            "has_control_plan": family.can_run_negative_controls,
            "has_ablation_plan": family.can_run_c_structure_ablation,
            "has_no_blocking_debt": no_debt,
        }
        reasons = [key for key, value in booleans.items() if not value]
        records.append(
            CandidateRealityContactRecord(
                candidate_family_id=family.candidate_family_id,
                **booleans,
                reality_contact_passed=all(booleans.values()),
                failure_reasons=reasons,
            )
        )
    return records
