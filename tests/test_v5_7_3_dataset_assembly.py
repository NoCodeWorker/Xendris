from phyng.targeted_ytrue.campaign import run_frontera_c_targeted_ytrue_extraction_campaign


def test_expanded_dataset_contains_existing_and_new_ytrue():
    result = run_frontera_c_targeted_ytrue_extraction_campaign(".")

    assert result.expanded_dataset["existing_accepted_ytrue_count"] == 4
    assert result.expanded_dataset["new_accepted_ytrue_count"] == len(result.accepted)
    assert result.expanded_dataset["accepted_ytrue_count"] == 4 + len(result.accepted)
