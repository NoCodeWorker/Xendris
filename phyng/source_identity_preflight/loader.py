"""Input loading for v4.9 source identity preflight."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.source_identity_preflight.schemas import SourceIdentityPreflightInputs


REQUIRED_INPUTS = {
    "v48_gate": "data/phi_curvature/next/phi_curvature_v4_8_next_gate_decision.json",
    "v48_resolution": "data/phi_curvature/sources/phi_curvature_source_resolution_v4_8.json",
    "v48_availability": "data/phi_curvature/sources/phi_curvature_source_availability_v4_8.json",
    "candidate_matrix": "data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json",
    "pivot_decision": "data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json",
    "phi_gradient_method_only": "data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json",
    "slot4_debt": "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json",
}


def load_source_identity_preflight_inputs(root: str | Path = ".") -> SourceIdentityPreflightInputs:
    repo_root = Path(root)
    payloads: dict[str, dict | list] = {}
    missing: list[str] = []
    for key, rel_path in REQUIRED_INPUTS.items():
        path = repo_root / rel_path
        if not path.exists():
            payloads[key] = [] if key in {"v48_resolution", "v48_availability", "candidate_matrix"} else {}
            missing.append(rel_path)
            continue
        payloads[key] = json.loads(path.read_text(encoding="utf-8"))
    return SourceIdentityPreflightInputs(missing_files=missing, **payloads)


def prior_results_available(inputs: SourceIdentityPreflightInputs) -> bool:
    return not inputs.missing_files and bool(inputs.candidate_matrix)
