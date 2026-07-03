"""Reports module for v4.6 candidate freeze review."""

from __future__ import annotations

import os
from pathlib import Path
from phyng.candidate_decision.schemas import (
    CandidateFreezeReview,
    FinalClaimPermissions,
    MethodOnlyRedefinition,
    ExperimentRequirement,
    CandidateFamilySelectionRecord,
    PivotDecision,
)

def generate_reports(
    root: str | Path,
    review: CandidateFreezeReview,
    permissions: FinalClaimPermissions,
    redefinition: MethodOnlyRedefinition,
    experiment: ExperimentRequirement,
    matrix: list[CandidateFamilySelectionRecord],
    pivot: PivotDecision,
) -> list[Path]:
    root_path = Path(root)

    # Directories
    decisions_dir = root_path / "reports/candidate_decisions"
    campaigns_dir = root_path / "reports/campaigns"
    
    os.makedirs(decisions_dir, exist_ok=True)
    os.makedirs(campaigns_dir, exist_ok=True)

    generated_paths = []

    # 1. Freeze Review Report
    freeze_review_path = decisions_dir / "phi_gradient_freeze_review_v4_6.md"
    freeze_review_md = f"""# Candidate Freeze Review — PHI_GRADIENT (v4.6)

- **Candidate ID**: {review.candidate_id}
- **Freeze Status**: {review.freeze_status}
- **Accepted y_true Count**: {review.accepted_y_true_count}
- **Predictive Gain Status**: {review.predictive_gain_status}
- **SLOT_4 Debt Status**: {review.slot4_debt_status}
- **Review Status / Canonical Status**: {review.review_status}

## Notes
{chr(10).join(f'- {n}' for n in review.notes)}

## Discipline Note
> A frozen candidate is not dead knowledge. It is protected knowledge.
"""
    with open(freeze_review_path, "w", encoding="utf-8") as f:
        f.write(freeze_review_md)
    generated_paths.append(freeze_review_path)

    # 2. Claim Permissions Report
    permissions_path = decisions_dir / "phi_gradient_final_claim_permissions_v4_6.md"
    allowed_bullets = "\n".join(f"- `{c}`" for c in permissions.allowed_claims)
    blocked_bullets = "\n".join(f"- `{c}`" for c in permissions.blocked_claims)
    unblock_bullets = "\n".join(f"- {c}" for c in permissions.required_to_unblock)
    permissions_md = f"""# Final Claim Permissions — PHI_GRADIENT (v4.6)

- **Decision Ref**: {permissions.decision_ref}
- **Predictive Gain Permission**: {permissions.predictive_gain_permission}
- **Physical Claim Permission**: {permissions.physical_claim_permission}
- **Gradient Mechanism Claim Permission**: {permissions.gradient_mechanism_claim_permission}
- **Benchmark Method Permission**: {permissions.benchmark_method_permission}
- **Method-Only Permission**: {permissions.method_only_permission}

## Allowed Claims
{allowed_bullets}

## Blocked Claims
{blocked_bullets}

## Required to Unblock
{unblock_bullets}
"""
    with open(permissions_path, "w", encoding="utf-8") as f:
        f.write(permissions_md)
    generated_paths.append(permissions_path)

    # 3. Method-Only Redefinition Report
    redef_path = decisions_dir / "phi_gradient_method_only_redefinition_v4_6.md"
    allowed_roles = "\n".join(f"- {r}" for r in redefinition.allowed_method_roles)
    prohibited_roles = "\n".join(f"- {r}" for r in redefinition.prohibited_scientific_roles)
    redef_md = f"""# Method-Only Redefinition — PHI_GRADIENT (v4.6)

- **Redefinition Status**: {redefinition.redefinition_status}
- **Required Label**: `{redefinition.required_label}`

## Allowed Methodological Roles
{allowed_roles}

## Prohibited Scientific Roles
{prohibited_roles}

## Notes
{chr(10).join(f'- {n}' for n in redefinition.notes)}

## Final Principle
> A method-only object must not masquerade as a physical model.
"""
    with open(redef_path, "w", encoding="utf-8") as f:
        f.write(redef_md)
    generated_paths.append(redef_path)

    # 4. Experiment Requirement Report
    exp_path = decisions_dir / "phi_gradient_experiment_requirement_v4_6.md"
    obs_bullets = ", ".join(experiment.required_observables)
    app_bullets = ", ".join(experiment.required_apparatus)
    exp_md = f"""# Experiment Requirement — PHI_GRADIENT (v4.6)

- **Requirement Status**: {experiment.requirement_status}
- **Recommended Action**: {experiment.recommended_action}
- **Required Observables**: {obs_bullets}
- **Minimum Measurements**: {experiment.minimum_measurements}
- **Required Sensitivity**: {experiment.required_sensitivity}
- **Required Apparatus**: {app_bullets}

## Risks
- **Feasibility Risk**: {experiment.feasibility_risk}
- **Cost Risk**: {experiment.cost_risk}
- **Timeline Risk**: {experiment.timeline_risk}

## Reason
{experiment.reason}
"""
    with open(exp_path, "w", encoding="utf-8") as f:
        f.write(exp_md)
    generated_paths.append(exp_path)

    # 5. Next Candidate Matrix Report
    matrix_path = decisions_dir / "next_candidate_family_selection_matrix_v4_6.md"
    matrix_rows = []
    for r in matrix:
        matrix_rows.append(
            f"| `{r.family_id}` | `{r.previous_status}` | {r.synthetic_survivability_score} | {r.y_true_accessibility} | {r.experimental_feasibility} | {r.selection_score:.2f} | `{r.recommended_action}` |"
        )
    matrix_md = f"""# Next Candidate Family Selection Matrix (v4.6)

| Family ID | Previous Status | Synthetic Score | y_true Access | Exp Feasibility | Selection Score | Recommended Action |
|---|---|---|---|---|---|---|
{chr(10).join(matrix_rows)}

## Selection Rules
- Do not select a next candidate by synthetic score alone.
- A candidate must satisfy accessibility/feasibility requirements to qualify.
- Best choice selected: `{pivot.next_candidate_family}`.
"""
    with open(matrix_path, "w", encoding="utf-8") as f:
        f.write(matrix_md)
    generated_paths.append(matrix_path)

    # 6. Pivot Decision Report
    pivot_path = decisions_dir / "phygn_v4_6_pivot_decision_v4_6.md"
    pivot_md = f"""# Pivot Decision (v4.6)

- **Decision ID**: {pivot.decision_ref}
- **Pivot Recommended**: {pivot.pivot_recommended}
- **Next Candidate Family**: `{pivot.next_candidate_family}`
- **Recommended Next Phase**: `{pivot.recommended_next_phase}`

## Notes
{chr(10).join(f'- {n}' for n in pivot.notes)}
"""
    with open(pivot_path, "w", encoding="utf-8") as f:
        f.write(pivot_md)
    generated_paths.append(pivot_path)

    # 7. Campaign Summary Report
    campaign_path = campaigns_dir / "PHI-GRADIENT-CANDIDATE-FREEZE-REVIEW-v4_6.md"
    campaign_md = f"""# Campaign Report: PHI-GRADIENT-CANDIDATE-FREEZE-REVIEW-v4_6

- **Campaign Status**: `{pivot.freeze_review_status}`
- **Pivot Target**: `{pivot.next_candidate_family}`
- **Next Recommended Phase**: `{pivot.recommended_next_phase}`

## Summary of Decisions

1. **Freeze Review**: Confirmed candidate is frozen with status `{review.freeze_status}`.
2. **Permissions**: Established that `PredictiveGain` is `{permissions.predictive_gain_permission}` and physical claims are `{permissions.physical_claim_permission}`.
3. **Method Redefinition**: Redefined as `{redefinition.required_label}` (status `{redefinition.redefinition_status}`).
4. **Pivot Matrix**: Built selection matrix. Recommended pivot to family `{pivot.next_candidate_family}`.

## Final Principle
> The pipeline must be able to convert failed evidence acquisition into better research direction.
"""
    with open(campaign_path, "w", encoding="utf-8") as f:
        f.write(campaign_md)
    generated_paths.append(campaign_path)

    return generated_paths
