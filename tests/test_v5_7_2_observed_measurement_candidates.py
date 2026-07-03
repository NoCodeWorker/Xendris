from phyng.campaigns.frontera_c_targeted_source_download_observable_location import (
    run_frontera_c_targeted_source_download_observable_location_campaign,
)


def test_observed_measurement_candidate_permits_v573():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")

    if result.observed_measurement_candidates:
        assert result.next_gate_decision["allowed_next_phase"] == "v5.7.3 - Targeted y_true Extraction"
        assert all(candidate.classification == "OBSERVED_MEASUREMENT_CANDIDATE" for candidate in result.observed_measurement_candidates)


def test_observed_measurement_candidates_require_figure_review():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")

    assert all("REQUIRES_HUMAN_FIGURE_REVIEW" in candidate.extraction_blockers for candidate in result.observed_measurement_candidates)
