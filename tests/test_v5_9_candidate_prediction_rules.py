from phyng.candidates.campaign import run_frontera_c_reality_contact_candidate_family_campaign


def test_candidate_requires_prediction_rule():
    run_frontera_c_reality_contact_candidate_family_campaign(".")
    import json

    payload = json.loads(open("data/frontera_c/candidates/candidate_prediction_rules_v5_9.json", encoding="utf-8").read())
    rules = {record["candidate_family_id"]: record for record in payload["records"]}

    assert rules["PHI_CURVATURE"]["rule_status"] == "BLOCKED_MISSING_FEATURES"
    assert rules["C_COORDINATE_RESPONSE"]["rule_status"] == "BLOCKED_AD_HOC_SCALE"


def test_baseline_is_not_selected_as_frontera_candidate():
    run_frontera_c_reality_contact_candidate_family_campaign(".")
    import json

    decision = json.loads(open("data/frontera_c/candidates/candidate_selection_decision_v5_9.json", encoding="utf-8").read())

    assert decision["selected_candidate_family"] != "DATA_DRIVEN_PHYSICS_BASELINE"
