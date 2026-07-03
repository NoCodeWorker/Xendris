"""Prediction-rule declarations for v5.9."""

from __future__ import annotations

from phyng.candidates.schemas import CandidateFamilyRecord, CandidatePredictionRule


def build_prediction_rules(families: list[CandidateFamilyRecord], missing_features: dict[str, list[str]]) -> list[CandidatePredictionRule]:
    rules: list[CandidatePredictionRule] = []
    for family in families:
        missing = missing_features.get(family.candidate_family_id, [])
        status = _status(family, missing)
        rules.append(
            CandidatePredictionRule(
                candidate_family_id=family.candidate_family_id,
                rule_id=f"RULE-v5_9-{family.candidate_family_id}",
                rule_status=status,
                input_features=[feature for feature in family.required_features if feature not in missing],
                target_variable="value_numeric",
                formula_or_algorithm=family.prediction_rule_summary or "UNDEFINED",
                parameter_policy=_parameter_policy(family),
                training_policy="Group-aware fitting only after v6.0 permission; no fitting performed in v5.9.",
                prediction_domain="visibility/decoherence accepted y_true dataset",
                constraints=["No y_true-derived features", "No source_id lookup", "No page/figure lookup"],
                leakage_risk="LOW" if status in {"READY_FOR_ALIGNMENT", "METHOD_ONLY_NOT_CANDIDATE"} else "MEDIUM",
                ablation_plan_available=family.can_run_c_structure_ablation,
                notes=family.notes,
            )
        )
    return rules


def _status(family: CandidateFamilyRecord, missing: list[str]) -> str:
    if family.candidate_type == "METHOD_ONLY":
        return "METHOD_ONLY_NOT_CANDIDATE"
    if family.allowed_role == "baseline_comparator":
        return "METHOD_ONLY_NOT_CANDIDATE"
    if "SLOT_4" in " ".join(family.scientific_debt_blockers):
        return "BLOCKED_SCIENTIFIC_DEBT"
    if "operational_scale_L_m" in missing:
        return "BLOCKED_AD_HOC_SCALE"
    if missing:
        return "BLOCKED_MISSING_FEATURES"
    if family.prediction_rule_summary is None:
        return "BLOCKED_MISSING_FEATURES"
    return "READY_FOR_ALIGNMENT"


def _parameter_policy(family: CandidateFamilyRecord) -> str:
    if family.candidate_type == "DATA_BASELINE":
        return "Baseline parameters may be fit only inside v6.0 cross-validation."
    if family.prediction_rule_summary is None:
        return "No parameter policy because no active prediction rule is defined."
    return "Predeclared parameters only; no post-hoc target tuning in v5.9."
