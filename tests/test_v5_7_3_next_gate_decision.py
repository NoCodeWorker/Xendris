from phyng.targeted_ytrue.campaign import run_frontera_c_targeted_ytrue_extraction_campaign


def test_threshold_requires_total_10_and_two_sources():
    result = run_frontera_c_targeted_ytrue_extraction_campaign(".")

    if result.next_gate_decision["total_accepted_ytrue_count"] < 10:
        assert result.status != "TARGETED_YTRUE_EXTRACTION_THRESHOLD_REACHED"
    if result.status == "TARGETED_YTRUE_EXTRACTION_THRESHOLD_REACHED":
        assert result.next_gate_decision["independent_source_count"] >= 2


def test_no_predictive_gain_computed():
    result = run_frontera_c_targeted_ytrue_extraction_campaign(".")

    assert result.next_gate_decision["no_predictive_gain_computed"] is True
    assert result.next_gate_decision["benchmark_built"] is False
