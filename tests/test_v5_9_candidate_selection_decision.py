from phyng.candidates.campaign import run_frontera_c_reality_contact_candidate_family_campaign


def test_selected_candidate_permits_v60():
    result = run_frontera_c_reality_contact_candidate_family_campaign(".")

    if result["passed_candidate_count"] > 0:
        assert result["allowed_next_phase"] == "v6.0 - Candidate Prediction Alignment & PredictiveGain Gate"
    else:
        assert result["allowed_next_phase"] is None


def test_no_predictive_gain_computed():
    run_frontera_c_reality_contact_candidate_family_campaign(".")
    import json

    next_gate = json.loads(open("data/frontera_c/candidates/v5_9_next_gate_decision.json", encoding="utf-8").read())

    assert next_gate["no_predictive_gain_computed"] is True
    assert next_gate["benchmark_scoring_run"] is False
