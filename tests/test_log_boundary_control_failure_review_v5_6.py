from phyng.frontera_c_disposition.control_failure_review import build_control_failure_review
from phyng.frontera_c_disposition.loader import load_control_failure_inputs


def test_gain_explained_by_simple_control_blocks_c_ablation():
    review = build_control_failure_review(load_control_failure_inputs("."))

    assert review.primary_failure_reason == "GAIN_EXPLAINED_BY_SIMPLE_CONTROL"
    assert review.can_proceed_to_c_structure_ablation is False
    assert review.can_support_frontera_c_validation is False
