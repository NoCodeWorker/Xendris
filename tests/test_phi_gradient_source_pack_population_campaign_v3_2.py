from phyng.campaigns.phi_gradient_reviewed_local_manifest import run_phi_gradient_reviewed_local_manifest_campaign
from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign


def test_source_pack_status_is_review_required(tmp_path):
    result = run_phi_gradient_source_pack_population_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_SOURCE_PACK_POPULATED"
    assert result.population_result.canonical_status.canonical_permission.value == "REVIEW_REQUIRED"
    assert result.population_result.canonical_status.evidence_level.value == "SYNTHETIC_ONLY"


def test_physical_claims_remain_blocked(tmp_path):
    result = run_phi_gradient_source_pack_population_campaign(tmp_path)

    assert "PHI_GRADIENT is physically validated." in result.population_result.blocked_claims
    assert "A seed extract is validated support." in result.population_result.blocked_claims
    assert "A candidate benchmark is benchmark support." in result.population_result.blocked_claims


def test_existing_v3_1_behavior_preserved(tmp_path):
    result = run_phi_gradient_reviewed_local_manifest_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_REVIEWED_MANIFEST_CREATED"
    assert result.gate_result.validated_extract_count == 0
