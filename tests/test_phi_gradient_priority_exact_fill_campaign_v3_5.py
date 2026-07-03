from pathlib import Path

from phyng.campaigns.phi_gradient_exact_extract_review import run_phi_gradient_exact_extract_review_campaign
from phyng.campaigns.phi_gradient_priority_exact_fill import run_phi_gradient_priority_exact_fill_campaign
from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign


def test_campaign_generates_reports(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    run_phi_gradient_exact_extract_review_campaign(tmp_path)

    result = run_phi_gradient_priority_exact_fill_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT"
    assert result.gate_result.priority_source_count == 5
    assert result.report_paths["campaign"].endswith("PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5.md")
    assert Path(result.report_paths["campaign"]).exists()


def test_existing_v3_4_behavior_preserved(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)

    result = run_phi_gradient_exact_extract_review_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW"
    assert result.gate_result.validation_ready_count == 0
