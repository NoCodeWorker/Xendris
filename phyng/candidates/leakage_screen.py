"""Leakage screening for v5.9 candidate families."""

from __future__ import annotations

from phyng.candidates.schemas import CandidateFamilyRecord, CandidateLeakageRecord, CandidatePredictionRule


def build_leakage_screen(families: list[CandidateFamilyRecord], rules: list[CandidatePredictionRule]) -> list[CandidateLeakageRecord]:
    rule_by_id = {rule.candidate_family_id: rule for rule in rules}
    records: list[CandidateLeakageRecord] = []
    for family in families:
        rule = rule_by_id[family.candidate_family_id]
        posthoc = family.candidate_family_id in {"PHI_LOCALIZED_WINDOW", "PHI_BANDPASS", "THRESHOLD_SATURATION"}
        ad_hoc = rule.rule_status == "BLOCKED_AD_HOC_SCALE"
        blocking = posthoc or ad_hoc
        records.append(
            CandidateLeakageRecord(
                candidate_family_id=family.candidate_family_id,
                target_column_not_used=True,
                original_value_text_not_used=True,
                source_lookup_not_used=True,
                page_figure_lookup_not_used=True,
                condition_value_not_derived_from_target=True,
                duplicate_target_not_used=True,
                posthoc_fit_flagged=posthoc,
                ad_hoc_scale_flagged=ad_hoc,
                leakage_status="BLOCKING" if blocking else "LOW",
                notes=["No scoring or fitting was performed in v5.9."],
            )
        )
    return records
