from phyng.candidates.campaign import run_frontera_c_reality_contact_candidate_family_campaign


def test_candidate_rejects_missing_features():
    run_frontera_c_reality_contact_candidate_family_campaign(".")
    import json

    schema = json.loads(open("data/frontera_c/candidates/candidate_feature_schema_v5_9.json", encoding="utf-8").read())

    assert "value_numeric" in schema["forbidden_feature_columns"]
    assert schema["missing_required_features_by_candidate"]["C_COORDINATE_RESPONSE"]
    assert schema["missing_required_features_by_candidate"]["SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE"]
