from phyng.source_acquisition.candidate_sources import build_candidate_sources
from phyng.source_acquisition.observable_target_matrix import build_observable_target_matrix


def test_observable_targets_prioritized():
    targets = build_observable_target_matrix(build_candidate_sources())

    assert targets
    assert any(item.target_observable_class == "FRINGE_VISIBILITY" for item in targets)
    assert all(item.expected_location_type == "FIGURE" for item in targets)
