from phyng.campaigns.phi_gradient_exact_extract_review import run_phi_gradient_exact_extract_review_campaign
from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.campaigns.phi_gradient_source_pack_validation import run_phi_gradient_source_pack_validation_campaign


def test_exact_extract_review_default_keeps_claims_blocked(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    result = run_phi_gradient_exact_extract_review_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW"
    assert result.gate_result.validation_ready_count == 0
    assert "PHI_GRADIENT is physically validated." in result.gate_result.blocked_claims


def test_existing_v3_3_behavior_preserved(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    result = run_phi_gradient_source_pack_validation_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED"
    assert result.gate_result.validated_support_count == 0
