from pathlib import Path

from phyng.repository_audit.campaigns import audit_campaigns
from phyng.repository_audit.reports import audit_reports
from phyng.repository_audit.tests import audit_tests


def test_campaign_report_and_test_audits_return_records():
    campaigns = audit_campaigns(Path("."))
    reports = audit_reports(Path("."))
    tests = audit_tests(Path("."))

    assert any(record.entrypoint.endswith("business_model_validation_gate.py") for record in campaigns)
    assert any(record.path.endswith("BUSINESS-MODEL-VALIDATION-GATE-v1_9.md") for record in reports)
    assert any(record.path.endswith("test_business_model_validation_campaign_v1_9.py") for record in tests)


def test_report_audit_maps_required_sections_when_present():
    records = audit_reports(Path("."))
    campaign_report = next(
        record for record in records
        if record.path.endswith("BUSINESS-MODEL-VALIDATION-GATE-v1_9.md")
    )

    assert campaign_report.title
    assert campaign_report.gate_results
    assert campaign_report.blocked_claims
