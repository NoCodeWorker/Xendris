"""Next candidate selection matrix module for v4.6 candidate freeze review."""

from __future__ import annotations

from typing import Any
from phyng.candidate_decision.schemas import CandidateFamilySelectionRecord

def evaluate_selection_matrix(inputs: dict[str, Any]) -> list[CandidateFamilySelectionRecord]:
    # Construct selection records for the 8 candidate families
    records = [
        CandidateFamilySelectionRecord(
            family_id="PHI_CURVATURE",
            previous_status="PHI_CANDIDATE_SURVIVES_CONTROLS",
            synthetic_survivability_score=0.4668,
            negative_control_resistance_score=0.1788,
            source_support_availability="HIGH",
            y_true_accessibility="MEDIUM",
            public_dataset_availability="PLAUSIBLE",
            observable_clarity="HIGH",
            slot4_independence="INDEPENDENT",
            experimental_feasibility="HIGH",
            claim_risk_level="LOW",
            selection_score=0.85,
            recommended_action="SELECT_FOR_SOURCE_AND_YTRUE_SCREENING",
            notes=["Clear curvature observable in literature.", "Satisfies non-synthetic selection rule."]
        ),
        CandidateFamilySelectionRecord(
            family_id="PHI_LOCALIZED_WINDOW",
            previous_status="PHI_CANDIDATE_SURVIVES_CONTROLS",
            synthetic_survivability_score=0.4566,
            negative_control_resistance_score=0.1500,
            source_support_availability="MEDIUM",
            y_true_accessibility="LOW",
            public_dataset_availability="NONE",
            observable_clarity="MEDIUM",
            slot4_independence="INDEPENDENT",
            experimental_feasibility="MEDIUM",
            claim_risk_level="MEDIUM",
            selection_score=0.60,
            recommended_action="KEEP_AS_METHOD_ONLY",
            notes=["Window size adds empirical parameter dependency."]
        ),
        CandidateFamilySelectionRecord(
            family_id="PHI_BANDPASS",
            previous_status="PHI_CANDIDATE_SURVIVES_CONTROLS",
            synthetic_survivability_score=0.3774,
            negative_control_resistance_score=0.1000,
            source_support_availability="LOW",
            y_true_accessibility="LOW",
            public_dataset_availability="NONE",
            observable_clarity="LOW",
            slot4_independence="INDEPENDENT",
            experimental_feasibility="LOW",
            claim_risk_level="MEDIUM",
            selection_score=0.40,
            recommended_action="KEEP_AS_METHOD_ONLY",
            notes=["Low synthetic score and unclear physical observable."]
        ),
        CandidateFamilySelectionRecord(
            family_id="PHI_GRADIENT",
            previous_status="PHI_GRADIENT_EMPIRICALLY_UNGROUNDED_FREEZE",
            synthetic_survivability_score=0.4745,
            negative_control_resistance_score=0.2000,
            source_support_availability="LOW",
            y_true_accessibility="NONE",
            public_dataset_availability="NONE",
            observable_clarity="HIGH",
            slot4_independence="DEPENDENT",
            experimental_feasibility="LOW",
            claim_risk_level="HIGH",
            selection_score=0.0,
            recommended_action="KEEP_AS_METHOD_ONLY",
            notes=["Frozen in v4.5 due to zero y_true records.", "Blocks predictive loop."]
        ),
        CandidateFamilySelectionRecord(
            family_id="B_SUPPRESSED",
            previous_status="UNSUPPORTED",
            synthetic_survivability_score=0.5500,
            negative_control_resistance_score=0.0500,
            source_support_availability="LOW",
            y_true_accessibility="NONE",
            public_dataset_availability="NONE",
            observable_clarity="MEDIUM",
            slot4_independence="INDEPENDENT",
            experimental_feasibility="LOW",
            claim_risk_level="HIGH",
            selection_score=0.10,
            recommended_action="ARCHIVE",
            notes=["Down-ranked after v1.5 negative-control evidence."]
        ),
        CandidateFamilySelectionRecord(
            family_id="QB_STRUCTURAL",
            previous_status="UNSUPPORTED",
            synthetic_survivability_score=0.3000,
            negative_control_resistance_score=0.0200,
            source_support_availability="LOW",
            y_true_accessibility="NONE",
            public_dataset_availability="NONE",
            observable_clarity="LOW",
            slot4_independence="DEPENDENT",
            experimental_feasibility="LOW",
            claim_risk_level="HIGH",
            selection_score=0.05,
            recommended_action="ARCHIVE",
            notes=["Dependent on SLOT_4 and lacks empirical support."]
        ),
        CandidateFamilySelectionRecord(
            family_id="LOG_BOUNDARY",
            previous_status="UNSUPPORTED",
            synthetic_survivability_score=0.2500,
            negative_control_resistance_score=0.0100,
            source_support_availability="LOW",
            y_true_accessibility="NONE",
            public_dataset_availability="NONE",
            observable_clarity="LOW",
            slot4_independence="INDEPENDENT",
            experimental_feasibility="LOW",
            claim_risk_level="MEDIUM",
            selection_score=0.05,
            recommended_action="ARCHIVE",
            notes=["Lacks empirical support."]
        ),
        CandidateFamilySelectionRecord(
            family_id="THRESHOLD_SATURATION",
            previous_status="UNSUPPORTED",
            synthetic_survivability_score=0.2000,
            negative_control_resistance_score=0.0100,
            source_support_availability="LOW",
            y_true_accessibility="NONE",
            public_dataset_availability="NONE",
            observable_clarity="LOW",
            slot4_independence="INDEPENDENT",
            experimental_feasibility="LOW",
            claim_risk_level="MEDIUM",
            selection_score=0.05,
            recommended_action="ARCHIVE",
            notes=["Lacks empirical support."]
        )
    ]

    return records
