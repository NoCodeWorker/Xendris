from phyng.candidates.campaign import run_frontera_c_reality_contact_candidate_family_campaign


def test_candidate_rejects_target_leakage():
    run_frontera_c_reality_contact_candidate_family_campaign(".")
    import json

    payload = json.loads(open("data/frontera_c/candidates/candidate_leakage_screen_v5_9.json", encoding="utf-8").read())
    records = {record["candidate_family_id"]: record for record in payload["records"]}

    assert records["PHI_LOCALIZED_WINDOW"]["leakage_status"] == "BLOCKING"
    assert records["PHI_LOCALIZED_WINDOW"]["posthoc_fit_flagged"] is True
    assert all(record["target_column_not_used"] for record in payload["records"])
