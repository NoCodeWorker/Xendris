from phyng.frontera_c_disposition.candidate_disposition import build_candidate_disposition
from phyng.frontera_c_disposition.control_failure_review import build_control_failure_review
from phyng.frontera_c_disposition.loader import load_control_failure_inputs
from phyng.frontera_c_disposition.roadmap_update import build_roadmap_update


def test_roadmap_blocks_validation_after_control_failure():
    disposition = build_candidate_disposition(build_control_failure_review(load_control_failure_inputs(".")))
    roadmap = build_roadmap_update(disposition)

    assert roadmap.new_blocker == "FRONTERA_C_BLOCKED_NEGATIVE_CONTROL_FAILURE"
    assert roadmap.current_validation_status == "NOT_VALIDATED"
    assert roadmap.recommended_path == "EXPAND_VISIBILITY_DATASET"
    assert "C-structure ablation for LOG_BOUNDARY" in roadmap.forbidden_paths
