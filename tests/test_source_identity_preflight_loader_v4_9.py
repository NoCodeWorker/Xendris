from pathlib import Path

from phyng.source_identity_preflight.campaign import run_phygn_source_identity_preflight_campaign
from phyng.source_identity_preflight.loader import load_source_identity_preflight_inputs, prior_results_available


def test_missing_prior_results_blocks_preflight(tmp_path: Path):
    inputs = load_source_identity_preflight_inputs(tmp_path)
    result = run_phygn_source_identity_preflight_campaign(tmp_path)

    assert prior_results_available(inputs) is False
    assert result.status == "PHYGN_SOURCE_IDENTITY_PREFLIGHT_BLOCKED_MISSING_PRIOR_RESULTS"
    assert result.inputs_loaded is False
