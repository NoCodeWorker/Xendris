from phyng.frontera_c_disposition.blocked_claims import build_blocked_claims
from phyng.frontera_c_disposition.candidate_disposition import build_candidate_disposition
from phyng.frontera_c_disposition.control_failure_review import build_control_failure_review
from phyng.frontera_c_disposition.loader import load_control_failure_inputs
from phyng.frontera_c_disposition.next_research_direction import build_next_research_direction
from phyng.frontera_c_disposition.roadmap_update import build_roadmap_update


def test_next_direction_generated():
    disposition = build_candidate_disposition(build_control_failure_review(load_control_failure_inputs(".")))
    next_direction = build_next_research_direction(build_roadmap_update(disposition), build_blocked_claims())

    assert next_direction.final_status == "LOG_BOUNDARY_ARCHIVED_AS_VALIDATION_CANDIDATE"
    assert next_direction.selected_next_direction == "EXPAND_VISIBILITY_DATASET"
    assert next_direction.allowed_next_phase == "v5.7 - Visibility/Decoherence Dataset Expansion"
