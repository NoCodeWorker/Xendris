from phyng.targeted_ytrue.campaign import run_frontera_c_targeted_ytrue_extraction_campaign


def test_dataset_quality_tracks_source_and_threshold_counts():
    result = run_frontera_c_targeted_ytrue_extraction_campaign(".")
    quality = result.dataset_quality

    assert quality.total_accepted_ytrue_count == result.expanded_dataset["accepted_ytrue_count"]
    assert quality.independent_source_count >= 2
    assert quality.benchmark_readiness in {"PARTIAL_MULTI_SOURCE_N_SMALL", "READY_FOR_OUT_OF_SOURCE_CONTROL"}
