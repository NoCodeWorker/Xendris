from pathlib import Path

from phyng.dataset_expansion.campaign import run_frontera_c_visibility_decoherence_dataset_expansion_campaign


def test_reports_generated():
    result = run_frontera_c_visibility_decoherence_dataset_expansion_campaign(".")

    assert result.report_paths
    assert Path("docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md").exists()
    assert all(Path(path).exists() for path in result.report_paths.values())


def test_campaign_outputs_and_claim_boundaries():
    result = run_frontera_c_visibility_decoherence_dataset_expansion_campaign(".")

    assert result.inputs_loaded is True
    assert result.next_gate_decision["physical_claim_created"] is False
    assert result.next_gate_decision["frontera_c_validated"] is False
    assert "LOG_BOUNDARY is restored as active validation candidate" in result.next_gate_decision["blocked_claims"]
