from phyng.dataset_expansion.campaign import run_frontera_c_visibility_decoherence_dataset_expansion_campaign


def test_out_of_source_readiness_requires_two_sources():
    result = run_frontera_c_visibility_decoherence_dataset_expansion_campaign(".")

    assert result.benchmark_readiness["independent_source_count"] == 1
    assert result.benchmark_readiness["out_of_source_split_possible"] is False
    assert result.benchmark_readiness["readiness"] == "PARTIAL_N_SMALL"


def test_next_gate_decision_matches_counts():
    result = run_frontera_c_visibility_decoherence_dataset_expansion_campaign(".")

    assert result.next_gate_decision["accepted_ytrue_count_total"] == len(result.accepted_ytrue)
    assert result.next_gate_decision["independent_source_count"] == result.dataset.source_count
    assert result.status == "VISIBILITY_DECOHERENCE_DATASET_EXPANSION_PARTIAL"
