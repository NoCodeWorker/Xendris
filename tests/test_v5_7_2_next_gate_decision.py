from phyng.campaigns.frontera_c_targeted_source_download_observable_location import (
    run_frontera_c_targeted_source_download_observable_location_campaign,
)


def test_no_predictive_gain_computed():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")

    assert result.next_gate_decision["no_predictive_gain_computed"] is True
    assert result.next_gate_decision["frontera_c_validated"] is False


def test_next_gate_decision_counts_are_consistent():
    result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")

    assert result.next_gate_decision["verified_source_object_count"] == result.verified_source_object_count
    assert result.next_gate_decision["candidate_location_count"] == len(result.location_candidates)
    assert result.next_gate_decision["observed_measurement_candidate_count"] == len(result.observed_measurement_candidates)
