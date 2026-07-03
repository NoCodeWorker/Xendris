"""Frontera C roadmap update after LOG_BOUNDARY control failure."""

from __future__ import annotations

from phyng.frontera_c_disposition.candidate_disposition import PROHIBITED_ACTIONS
from phyng.frontera_c_disposition.schemas import CandidateDisposition, FronteraCRoadmapUpdate


def build_roadmap_update(disposition: CandidateDisposition) -> FronteraCRoadmapUpdate:
    return FronteraCRoadmapUpdate(
        previous_active_candidate="LOG_BOUNDARY",
        previous_blocker="LOG_BOUNDARY_GAIN_EXPLAINED_BY_SIMPLE_CONTROL",
        new_blocker="FRONTERA_C_BLOCKED_NEGATIVE_CONTROL_FAILURE",
        candidates_archived=[disposition.candidate_family],
        candidates_retained_as_fixtures=[disposition.candidate_family],
        current_validation_status="NOT_VALIDATED",
        next_viable_paths=[
            "EXPAND_VISIBILITY_DATASET",
            "REPRIORITIZE_CANDIDATE_FAMILIES",
            "NEW_EXPERIMENT_DESIGN",
            "HUMAN_SOURCE_LOOKUP_FOR_NEXT_CANDIDATE",
            "PAUSE_VALIDATION_AND_HARDEN_BENCHMARKS",
        ],
        recommended_path="EXPAND_VISIBILITY_DATASET",
        rationale=(
            "The pipeline extracted accepted y_true from Hackermueller 2004, but LOG_BOUNDARY failed controls. "
            "The immediate bottleneck is single-source N=4 fragility, so dataset expansion is a data path, not a LOG_BOUNDARY rescue."
        ),
        forbidden_paths=PROHIBITED_ACTIONS,
    )
