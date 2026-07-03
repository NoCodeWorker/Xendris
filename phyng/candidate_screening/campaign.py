"""Campaign orchestrator for v4.7 candidate screening."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from phyng.candidate_screening.loader import load_screening_inputs, MissingPivotDecisionError
from phyng.candidate_screening.source_accessibility import screen_source_accessibility
from phyng.candidate_screening.observable_accessibility import screen_observable_accessibility
from phyng.candidate_screening.ytrue_accessibility import screen_ytrue_accessibility
from phyng.candidate_screening.public_dataset_screen import screen_public_dataset
from phyng.candidate_screening.experimental_feasibility import screen_experimental_feasibility
from phyng.candidate_screening.claim_risk import screen_claim_risk
from phyng.candidate_screening.decision import evaluate_screening_decision
from phyng.candidate_screening.reports import generate_reports
from phyng.candidate_screening.schemas import CampaignResultv47

def run_phi_curvature_accessibility_screen_campaign(root: str | Path = ".") -> CampaignResultv47 | dict[str, Any]:
    root_path = Path(root)

    # 1. Load inputs
    try:
        inputs = load_screening_inputs(root_path)
    except MissingPivotDecisionError:
        return {
            "status": "PHI_CURVATURE_ACCESSIBILITY_BLOCKED_MISSING_PIVOT_DECISION",
            "message": "Pivot decision file is missing. Screening blocked."
        }
    except FileNotFoundError as e:
        raise e

    # 2. Run screens
    source = screen_source_accessibility(inputs)
    observable = screen_observable_accessibility(inputs)
    ytrue = screen_ytrue_accessibility(inputs)
    public_dataset = screen_public_dataset(inputs)
    experiment = screen_experimental_feasibility(inputs)
    claim_risk = screen_claim_risk(inputs)
    
    # 3. Decision Gate
    decision = evaluate_screening_decision(
        inputs, source, observable, ytrue, public_dataset, experiment, claim_risk
    )

    # 4. Write JSON outputs
    screening_dir = root_path / "data/candidate_screening"
    os.makedirs(screening_dir, exist_ok=True)

    # Prepare inputs dictionary for serialization
    screening_inputs_data = {
        "selection_matrix_v4_6": inputs["selection_matrix_v4_6"],
        "pivot_decision_v4_6": inputs["pivot_decision_v4_6"],
        "method_only_redefinition_v4_6": inputs["method_only_redefinition_v4_6"],
        "final_claim_permissions_v4_6": inputs["final_claim_permissions_v4_6"],
        "experiment_requirement_v4_6": inputs["experiment_requirement_v4_6"],
        "debt_slot4": inputs["debt_slot4"],
    }

    outputs_map = {
        "phi_curvature_screening_inputs_v4_7.json": screening_inputs_data,
        "phi_curvature_source_accessibility_screen_v4_7.json": source,
        "phi_curvature_observable_accessibility_screen_v4_7.json": observable,
        "phi_curvature_ytrue_accessibility_screen_v4_7.json": ytrue,
        "phi_curvature_public_dataset_screen_v4_7.json": public_dataset,
        "phi_curvature_experimental_feasibility_screen_v4_7.json": experiment,
        "phi_curvature_claim_risk_screen_v4_7.json": claim_risk,
        "phi_curvature_screening_decision_v4_7.json": decision,
    }

    for filename, val in outputs_map.items():
        file_path = screening_dir / filename
        if isinstance(val, dict):
            data = val
        else:
            data = val.model_dump()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # 5. Generate Reports
    generate_reports(root_path, inputs, source, observable, ytrue, public_dataset, experiment, claim_risk, decision)

    # Wrap the status
    campaign_status = "PHI_CURVATURE_ACCESSIBILITY_SCREEN_COMPLETED"

    return CampaignResultv47(
        status=campaign_status,
        source_screen=source,
        observable_screen=observable,
        ytrue_screen=ytrue,
        public_dataset=public_dataset,
        experiment=experiment,
        claim_risk=claim_risk,
        decision=decision,
    )
