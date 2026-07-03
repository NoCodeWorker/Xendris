"""Campaign orchestrator for v4.6 candidate freeze review."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from phyng.candidate_decision.loader import load_candidate_decision_inputs, MissingFreezeDecisionError
from phyng.candidate_decision.freeze_review import perform_freeze_review
from phyng.candidate_decision.claim_permissions import establish_claim_permissions
from phyng.candidate_decision.method_redefinition import redefine_as_method_only
from phyng.candidate_decision.experiment_requirement import evaluate_experiment_requirement
from phyng.candidate_decision.next_candidate_matrix import evaluate_selection_matrix
from phyng.candidate_decision.pivot_decision import determine_pivot_decision
from phyng.candidate_decision.reports import generate_reports
from phyng.candidate_decision.schemas import CampaignResultv46

def run_candidate_decision_campaign(root: str | Path = ".") -> CampaignResultv46 | dict[str, Any]:
    root_path = Path(root)

    # 1. Load inputs
    try:
        inputs = load_candidate_decision_inputs(root_path)
    except MissingFreezeDecisionError:
        # Return blocked campaign result
        return {
            "status": "PHI_GRADIENT_FREEZE_REVIEW_BLOCKED_MISSING_FREEZE_DECISION",
            "message": "Freeze decision file is missing. Review blocked."
        }
    except FileNotFoundError as e:
        raise e

    # 2. Run steps
    review = perform_freeze_review(inputs)
    permissions = establish_claim_permissions(inputs, review.freeze_decision_ref)
    redefinition = redefine_as_method_only(inputs)
    experiment = evaluate_experiment_requirement(inputs)
    matrix = evaluate_selection_matrix(inputs)
    pivot = determine_pivot_decision(inputs, matrix)

    # Set overall status
    campaign_status = "PHI_GRADIENT_FREEZE_REVIEW_COMPLETED"

    # 3. Write JSON output files
    decisions_dir = root_path / "data/candidate_decisions"
    os.makedirs(decisions_dir, exist_ok=True)

    outputs_map = {
        "phi_gradient_freeze_review_v4_6.json": review,
        "phi_gradient_final_claim_permissions_v4_6.json": permissions,
        "phi_gradient_method_only_redefinition_v4_6.json": redefinition,
        "phi_gradient_experiment_requirement_v4_6.json": experiment,
        "next_candidate_family_selection_matrix_v4_6.json": matrix,
        "phygn_v4_6_pivot_decision_v4_6.json": pivot,
    }

    for filename, model_or_list in outputs_map.items():
        file_path = decisions_dir / filename
        if isinstance(model_or_list, list):
            data = [item.model_dump() for item in model_or_list]
        else:
            data = model_or_list.model_dump()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # 4. Generate Reports
    generate_reports(root_path, review, permissions, redefinition, experiment, matrix, pivot)

    return CampaignResultv46(
        status=campaign_status,
        freeze_review=review,
        permissions=permissions,
        redefinition=redefinition,
        experiment=experiment,
        matrix=matrix,
        pivot=pivot,
    )
