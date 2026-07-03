from phyng.campaigns.phi_gradient_real_source_acquisition import (
    run_phi_gradient_real_source_acquisition_campaign,
)
from phyng.campaigns.phi_gradient_reviewed_local_manifest import (
    run_phi_gradient_reviewed_local_manifest_campaign,
)


def test_reviewed_manifest_campaign_blocks_physical_claims(tmp_path):
    result = run_phi_gradient_reviewed_local_manifest_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_REVIEWED_MANIFEST_CREATED"
    assert "PHI_GRADIENT is physically validated." in result.gate_result.blocked_claims
    assert "A reviewed manifest proves PHI_GRADIENT." in result.gate_result.blocked_claims


def test_existing_v3_0_behavior_preserved(tmp_path):
    result = run_phi_gradient_real_source_acquisition_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING"
    assert result.acquisition_result.actual_real_sources_acquired is False
