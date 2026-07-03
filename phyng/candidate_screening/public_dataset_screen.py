"""Public dataset screening module for v4.7."""

from __future__ import annotations

from typing import Any
from phyng.candidate_screening.schemas import PublicDatasetScreen

def screen_public_dataset(inputs: dict[str, Any]) -> PublicDatasetScreen:
    matrix = inputs.get("selection_matrix_v4_6", [])
    record = next((r for r in matrix if r.get("family_id") == "PHI_CURVATURE"), {})
    
    availability = str(inputs.get("override_dataset_availability") or record.get("public_dataset_availability") or "PLAUSIBLE")

    if availability == "PLAUSIBLE":
        score = 0.5
    elif availability == "HIGH":
        score = 0.8
    elif availability == "LOW":
        score = 0.2
    else:
        score = 0.0

    return PublicDatasetScreen(
        candidate_family="PHI_CURVATURE",
        plausible_repository_types=["ZENODO", "FIGSHARE"],
        known_dataset_refs=[],
        local_dataset_refs=[],
        dataset_availability=availability,
        dataset_accessibility_score=score,
        required_search_queries=["phi curvature quantum decoherence", "curvature coefficient measurements"],
        notes=["Zenodo contains a possible candidate dataset that requires manual vetting."]
    )
