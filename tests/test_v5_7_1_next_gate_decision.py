from phyng.source_acquisition.campaign import run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign


def test_next_gate_requires_three_resolved_sources():
    result = run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign(".")

    assert result.next_gate_decision["resolved_candidate_source_count"] >= 3
    assert result.next_gate_decision["allowed_next_phase"] == "v5.7.2 - Targeted Source Download & Observable Location Review"


def test_no_predictive_gain_computed():
    result = run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign(".")

    assert result.next_gate_decision["no_predictive_gain_computed"] is True
    assert result.next_gate_decision["no_ytrue_extracted"] is True
