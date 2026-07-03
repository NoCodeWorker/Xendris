from pathlib import Path

from phyng.repository_audit.modules import audit_dependencies, audit_module_boundaries


def test_module_audit_records_imports():
    records = audit_module_boundaries(Path("."))
    by_module = {record.module: record for record in records}

    campaign = by_module["phyng.campaigns.business_model_validation_gate"]
    assert "phyng.business_validation.schemas" in campaign.imports
    assert campaign.tests_covering_module


def test_dependency_audit_reports_records_without_failing_on_heuristics():
    records = audit_dependencies(Path("."))

    assert records
    assert any(record.module == "phyng.campaigns.business_model_validation_gate" for record in records)
