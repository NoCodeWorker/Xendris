"""Input loader for v4.8 PHI_CURVATURE minimal campaign."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.phi_curvature_minimal_campaign.schemas import PhiCurvatureMinimalInputs


REQUIRED_INPUTS = {
    "screening_decision": "data/candidate_screening/phi_curvature_screening_decision_v4_7.json",
    "source_screen": "data/candidate_screening/phi_curvature_source_accessibility_screen_v4_7.json",
    "observable_screen": "data/candidate_screening/phi_curvature_observable_accessibility_screen_v4_7.json",
    "ytrue_screen": "data/candidate_screening/phi_curvature_ytrue_accessibility_screen_v4_7.json",
    "public_dataset_screen": "data/candidate_screening/phi_curvature_public_dataset_screen_v4_7.json",
    "experimental_feasibility_screen": "data/candidate_screening/phi_curvature_experimental_feasibility_screen_v4_7.json",
    "claim_risk_screen": "data/candidate_screening/phi_curvature_claim_risk_screen_v4_7.json",
    "phi_gradient_method_only": "data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json",
    "slot4_debt": "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json",
}


def load_phi_curvature_minimal_inputs(root: str | Path = ".") -> PhiCurvatureMinimalInputs:
    repo_root = Path(root)
    payloads: dict[str, dict] = {}
    missing: list[str] = []
    for key, rel_path in REQUIRED_INPUTS.items():
        path = repo_root / rel_path
        if not path.exists():
            missing.append(rel_path)
            payloads[key] = {}
            continue
        payloads[key] = json.loads(path.read_text(encoding="utf-8"))
    return PhiCurvatureMinimalInputs(missing_files=missing, **payloads)


def v47_screen_passed(inputs: PhiCurvatureMinimalInputs) -> bool:
    return inputs.screening_decision.get("final_status") == "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED"
