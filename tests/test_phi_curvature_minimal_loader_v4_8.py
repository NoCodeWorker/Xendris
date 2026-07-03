from pathlib import Path

from phyng.phi_curvature_minimal_campaign.campaign import run_phi_curvature_minimal_source_ytrue_campaign
from phyng.phi_curvature_minimal_campaign.loader import load_phi_curvature_minimal_inputs


def test_missing_v47_screen_blocks_campaign(tmp_path: Path):
    inputs = load_phi_curvature_minimal_inputs(tmp_path)
    result = run_phi_curvature_minimal_source_ytrue_campaign(tmp_path)

    assert inputs.missing_files
    assert result.status == "PHI_CURVATURE_MINIMAL_CAMPAIGN_BLOCKED_MISSING_SCREEN"
    assert result.inputs_loaded is False
