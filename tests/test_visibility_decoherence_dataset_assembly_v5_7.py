from phyng.dataset_expansion.campaign import run_frontera_c_visibility_decoherence_dataset_expansion_campaign


def test_dataset_expansion_is_not_candidate_rescue():
    result = run_frontera_c_visibility_decoherence_dataset_expansion_campaign(".")

    assert result.next_gate_decision["log_boundary_remains_archived"] is True
    assert result.next_gate_decision["dataset_expansion_is_candidate_rescue"] is False
    assert result.dataset.accepted_ytrue_count == 4
