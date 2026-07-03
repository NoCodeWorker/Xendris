from phyng.dataset_expansion.campaign import run_frontera_c_visibility_decoherence_dataset_expansion_campaign


def test_no_physical_claim_created():
    result = run_frontera_c_visibility_decoherence_dataset_expansion_campaign(".")

    assert result.dataset_quality["physical_claim_created"] is False
    assert result.dataset_quality["frontera_c_validated"] is False


def test_quality_flags_single_source_n_small():
    result = run_frontera_c_visibility_decoherence_dataset_expansion_campaign(".")

    assert "SINGLE_SOURCE" in result.dataset_quality["quality_flags"]
    assert "N_SMALL_4" in result.dataset_quality["quality_flags"]
