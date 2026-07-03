from pathlib import Path

from phyng.source_acquisition.campaign import run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign


def test_reports_generated():
    result = run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign(".")

    assert result.report_paths
    assert Path("docs/344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md").exists()
    assert all(Path(path).exists() for path in result.report_paths.values())


def test_claim_boundaries_preserved():
    result = run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign(".")

    assert result.next_gate_decision["log_boundary_reactivated"] is False
    assert result.next_gate_decision["source_acquisition_is_evidence"] is False
    assert result.next_gate_decision["physical_claim_created"] is False
    assert result.next_gate_decision["frontera_c_validated"] is False
