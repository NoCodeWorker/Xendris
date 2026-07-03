from phyng.targeted_ytrue.campaign import run_frontera_c_targeted_ytrue_extraction_campaign


def test_hackermueller_v53_records_not_duplicated():
    result = run_frontera_c_targeted_ytrue_extraction_campaign(".")
    existing_ids = [record["y_true_id"] for record in result.expanded_dataset["records"] if str(record["y_true_id"]).startswith("YTRUE-v5_3")]

    assert len(existing_ids) == 4
    assert len(set(existing_ids)) == 4


def test_conditions_are_not_ytrue():
    result = run_frontera_c_targeted_ytrue_extraction_campaign(".")

    assert all(item.variable_name in {"visibility_fraction", "interference_contrast"} for item in result.accepted)
    assert all("velocity_m_s" not in item.variable_name for item in result.accepted)
