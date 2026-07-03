from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.campaigns.phi_gradient_source_pack_validation import run_phi_gradient_source_pack_validation_campaign


def test_default_seed_validation_completes_without_support(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    result = run_phi_gradient_source_pack_validation_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED"
    assert result.gate_result.validated_support_count == 0
    assert result.gate_result.manual_review_count > 0


def test_final_gate_keeps_physical_claims_blocked(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    result = run_phi_gradient_source_pack_validation_campaign(tmp_path)

    assert "PHI_GRADIENT is physically validated." in result.gate_result.blocked_claims
    assert "Manual-review extract counts as support." in result.gate_result.blocked_claims


def test_existing_v3_2_behavior_preserved(tmp_path):
    result = run_phi_gradient_source_pack_population_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_SOURCE_PACK_POPULATED"
    assert result.population_result.validation.extract_count == 8
