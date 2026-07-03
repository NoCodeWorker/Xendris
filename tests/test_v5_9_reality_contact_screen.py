from phyng.candidates.campaign import run_frontera_c_reality_contact_candidate_family_campaign


def test_candidate_requires_control_plan():
    run_frontera_c_reality_contact_candidate_family_campaign(".")
    import json

    payload = json.loads(open("data/frontera_c/candidates/candidate_reality_contact_screen_v5_9.json", encoding="utf-8").read())
    records = {record["candidate_family_id"]: record for record in payload["records"]}

    assert records["PHI_GRADIENT_METHOD_ONLY"]["has_control_plan"] is True
    assert records["PHI_GRADIENT_METHOD_ONLY"]["reality_contact_passed"] is False


def test_candidate_requires_ablation_plan():
    run_frontera_c_reality_contact_candidate_family_campaign(".")
    import json

    payload = json.loads(open("data/frontera_c/candidates/candidate_reality_contact_screen_v5_9.json", encoding="utf-8").read())
    records = {record["candidate_family_id"]: record for record in payload["records"]}

    assert records["SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE"]["has_ablation_plan"] is False
    assert records["SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE"]["reality_contact_passed"] is False
