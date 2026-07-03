from pathlib import Path

from phyng.campaigns.phi_gradient_exact_extract_review import run_phi_gradient_exact_extract_review_campaign
from phyng.campaigns.phi_gradient_local_source_text_registry import run_phi_gradient_local_source_text_registry_campaign
from phyng.campaigns.phi_gradient_priority_exact_fill import run_phi_gradient_priority_exact_fill_campaign
from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign


def test_reports_include_canonical_section(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)

    result = run_phi_gradient_local_source_text_registry_campaign(tmp_path)

    for path in result.report_paths.values():
        text = Path(path).read_text(encoding="utf-8")
        assert "## Canonical Status" in text


def test_campaign_generates_reports(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)

    result = run_phi_gradient_local_source_text_registry_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_LOCAL_SOURCE_FILES_MISSING"
    assert result.registry_result.manual_download_task_count == 5
    assert Path(result.report_paths["campaign"]).exists()
    assert result.report_paths["campaign"].endswith("PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6.md")


def test_physical_claims_remain_blocked(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)

    result = run_phi_gradient_local_source_text_registry_campaign(tmp_path)

    assert "PHI_GRADIENT is physically validated." in result.registry_result.blocked_claims
    assert "A source hash is source support." in result.registry_result.blocked_claims


def test_existing_v3_5_behavior_preserved(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    run_phi_gradient_exact_extract_review_campaign(tmp_path)

    result = run_phi_gradient_priority_exact_fill_campaign(tmp_path)

    assert result.status == "PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT"
    assert result.gate_result.validation_ready_count == 0
