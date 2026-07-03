"""Reports module for v4.7 candidate screening."""

from __future__ import annotations

import os
from pathlib import Path
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

def generate_reports(
    root: str | Path,
    inputs: dict[str, Any],
    source: SourceAccessibilityScreen,
    observable: ObservableAccessibilityScreen,
    ytrue: YTrueAccessibilityScreen,
    public_dataset: PublicDatasetScreen,
    experiment: ExperimentalFeasibilityScreen,
    claim_risk: ClaimRiskScreen,
    decision: CandidateScreeningDecision,
) -> list[Path]:
    root_path = Path(root)

    # Directories
    screening_dir = root_path / "reports/candidate_screening"
    campaigns_dir = root_path / "reports/campaigns"
    
    os.makedirs(screening_dir, exist_ok=True)
    os.makedirs(campaigns_dir, exist_ok=True)

    generated_paths = []

    pivot_ref = inputs.get("pivot_decision_v4_6", {}).get("decision_ref", "UNKNOWN")

    discipline_note = """> Accessibility is not evidence.
> It is permission to look for evidence.
"""

    # Helper function to write files
    def write_report(filename: str, content: str, folder: Path = screening_dir) -> Path:
        p = folder / filename
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        generated_paths.append(p)
        return p

    # 1. Inputs Report
    write_report(
        "phi_curvature_screening_inputs_v4_7.md",
        f"""# PHI_CURVATURE Screening Inputs (v4.7)

- **Candidate Family**: `{decision.candidate_family}`
- **v4.6 Pivot Reference**: `{pivot_ref}`

## Loaded inputs
- `next_candidate_family_selection_matrix_v4_6.json`
- `phygn_v4_6_pivot_decision_v4_6.json`
- `phi_gradient_method_only_redefinition_v4_6.json`
- `phi_gradient_final_claim_permissions_v4_6.json`
- `phi_gradient_experiment_requirement_v4_6.json`
- `DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json`
"""
    )

    # 2. Source Accessibility Report
    write_report(
        "phi_curvature_source_accessibility_screen_v4_7.md",
        f"""# Source Accessibility Screen — PHI_CURVATURE (v4.7)

- **Source Location Quality**: `{source.source_location_quality}`
- **Source Accessibility Score**: `{source.source_accessibility_score}`
- **Likely Domains**: `{', '.join(source.likely_source_domains)}`
- **Known Refs**: `{', '.join(source.known_source_refs)}`
- **Recommended Next Action**: `{source.recommended_next_action}`

## Blockers
{chr(10).join(f'- {b}' for b in source.blockers) if source.blockers else '- None'}
"""
    )

    # 3. Observable Accessibility Report
    write_report(
        "phi_curvature_observable_accessibility_screen_v4_7.md",
        f"""# Observable Accessibility Screen — PHI_CURVATURE (v4.7)

- **Observable Clarity**: `{observable.observable_clarity}`
- **Observable Accessibility Score**: `{observable.observable_accessibility_score}`
- **Proposed Observables**: `{', '.join(observable.proposed_observables)}`
- **Observable Classes**: `{', '.join(observable.observable_classes)}`
- **Directly Measurable**: `{', '.join(observable.directly_measurable)}`
- **Proxy Observables**: `{', '.join(observable.proxy_observables)}`

## Notes
{chr(10).join(f'- {n}' for n in observable.notes) if observable.notes else '- None'}
"""
    )

    # 4. Y_true Accessibility Report
    write_report(
        "phi_curvature_ytrue_accessibility_screen_v4_7.md",
        f"""# y_true Accessibility Screen — PHI_CURVATURE (v4.7)

- **Manual Extraction Likelihood**: `{ytrue.manual_extraction_likelihood}`
- **Public Dataset Likelihood**: `{ytrue.public_dataset_likelihood}`
- **Experiment Required**: `{ytrue.experiment_required}`
- **Minimum y_true Feasibility**: `{ytrue.minimum_ytrue_feasibility}`
- **y_true Accessibility Score**: `{ytrue.ytrue_accessibility_score}`

## Blockers
{chr(10).join(f'- {b}' for b in ytrue.blockers) if ytrue.blockers else '- None'}
"""
    )

    # 5. Public Dataset Report
    write_report(
        "phi_curvature_public_dataset_screen_v4_7.md",
        f"""# Public Dataset Screen — PHI_CURVATURE (v4.7)

- **Dataset Availability**: `{public_dataset.dataset_availability}`
- **Dataset Accessibility Score**: `{public_dataset.dataset_accessibility_score}`
- **Plausible Repo Types**: `{', '.join(public_dataset.plausible_repository_types)}`

## Notes
{chr(10).join(f'- {n}' for n in public_dataset.notes) if public_dataset.notes else '- None'}
"""
    )

    # 6. Experimental Feasibility Report
    write_report(
        "phi_curvature_experimental_feasibility_screen_v4_7.md",
        f"""# Experimental Feasibility Screen — PHI_CURVATURE (v4.7)

- **Feasibility Level**: `{experiment.feasibility_level}`
- **Experiment Accessibility Score**: `{experiment.experiment_accessibility_score}`
- **Required Observables**: `{', '.join(experiment.required_observables)}`
- **Possible Classes**: `{', '.join(experiment.possible_experiment_classes)}`
- **Required Apparatus**: `{', '.join(experiment.required_apparatus)}`
- **Cost Risk**: `{experiment.cost_risk}`
- **Timeline Risk**: `{experiment.timeline_risk}`

## Notes
{chr(10).join(f'- {n}' for n in experiment.notes) if experiment.notes else '- None'}
"""
    )

    # 7. Claim Risk Report
    write_report(
        "phi_curvature_claim_risk_screen_v4_7.md",
        f"""# Claim Risk Screen — PHI_CURVATURE (v4.7)

- **Physical Claim Risk**: `{claim_risk.physical_claim_risk}`
- **SLOT_4 Dependency Risk**: `{claim_risk.slot4_dependency_risk}`
- **Claim Risk Score**: `{claim_risk.claim_risk_score}`

## Mitigation Rules
{chr(10).join(f'- {r}' for r in claim_risk.mitigation_rules) if claim_risk.mitigation_rules else '- None'}
"""
    )

    # 8. Screening Decision Report
    write_report(
        "phi_curvature_screening_decision_v4_7.md",
        f"""# Screening Decision — PHI_CURVATURE (v4.7)

- **Final Status**: `{decision.final_status}`
- **Aggregate Accessibility Score**: `{decision.aggregate_accessibility_score:.3f}`
- **Allowed Next Phase**: `{decision.allowed_next_phase}`

## Pass Criteria Met
{chr(10).join(f'- {c}' for c in decision.pass_criteria_met) if decision.pass_criteria_met else '- None'}

## Fail Criteria Met
{chr(10).join(f'- {f}' for f in decision.fail_criteria_met) if decision.fail_criteria_met else '- None'}

## Blocked Next Phases
{chr(10).join(f'- {b}' for b in decision.blocked_next_phases) if decision.blocked_next_phases else '- None'}

## Required Guardrails
{chr(10).join(f'- {g}' for g in decision.required_guardrails) if decision.required_guardrails else '- None'}

## Discipline Note
{discipline_note}
"""
    )

    # 9. Campaign Report
    write_report(
        "PHI-CURVATURE-SOURCE-YTRUE-ACCESSIBILITY-SCREEN-v4_7.md",
        f"""# Campaign Report: PHI-CURVATURE-SOURCE-YTRUE-ACCESSIBILITY-SCREEN-v4_7

- **Candidate Family**: `{decision.candidate_family}`
- **v4.6 Pivot Reference**: `{pivot_ref}`
- **Canonical Status**: `{decision.final_status}`
- **Allowed Next Phase**: `{decision.allowed_next_phase}`

## Summary of Screens
1. **Source Accessibility**: Quality is `{source.source_location_quality}` (score `{source.source_accessibility_score}`).
2. **Observable Clarity**: Clarity is `{observable.observable_clarity}` (score `{observable.observable_accessibility_score}`).
3. **y_true Accessibility**: Feasibility is `{ytrue.minimum_ytrue_feasibility}` (score `{ytrue.ytrue_accessibility_score}`).
4. **Public Dataset**: Availability is `{public_dataset.dataset_availability}` (score `{public_dataset.dataset_accessibility_score}`).
5. **Experimental Feasibility**: Level is `{experiment.feasibility_level}` (score `{experiment.experiment_accessibility_score}`).
6. **SLOT_4 Independence**: Status is `{claim_risk.slot4_dependency_risk == 'LOW'}` (score `{claim_risk.slot4_dependency_risk}`).
7. **Claim Risk**: Physical claim risk is `{claim_risk.physical_claim_risk}` (score `{claim_risk.claim_risk_score}`).

## Required Guardrails
{chr(10).join(f'- {g}' for g in decision.required_guardrails) if decision.required_guardrails else '- None'}

## Discipline Note
{discipline_note}
""",
        folder=campaigns_dir
    )

    return generated_paths
