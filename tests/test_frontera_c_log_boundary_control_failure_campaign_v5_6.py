from pathlib import Path

from phyng.frontera_c_disposition.campaign import run_frontera_c_log_boundary_control_failure_review_campaign


def test_campaign_generates_disposition_outputs():
    result = run_frontera_c_log_boundary_control_failure_review_campaign(".")

    assert result.status == "LOG_BOUNDARY_ARCHIVED_AS_VALIDATION_CANDIDATE"
    assert result.inputs_loaded is True
    assert result.review.can_proceed_to_c_structure_ablation is False
    assert result.review.can_support_frontera_c_validation is False
    assert result.disposition.primary_disposition == "ARCHIVE_AS_VALIDATION_CANDIDATE"
    assert result.next_direction.allowed_next_phase == "v5.7 - Visibility/Decoherence Dataset Expansion"
    for path in result.output_paths.values():
        assert Path(path).exists()


def test_no_predictive_gain_recomputed():
    result = run_frontera_c_log_boundary_control_failure_review_campaign(".")

    assert result.review.notes
    assert "No PredictiveGain was recomputed in v5.6." in result.review.notes
    assert result.blocked_claims.physical_claim_created is False


def test_reports_include_canonical_status():
    result = run_frontera_c_log_boundary_control_failure_review_campaign(".")
    campaign_report = Path(result.report_paths["campaign"])

    assert campaign_report.exists()
    assert "## Canonical Status" in campaign_report.read_text(encoding="utf-8")
