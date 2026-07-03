from pathlib import Path

from phyng.repository_audit.structure import audit_repository_structure


def test_repository_audit_discovers_packages():
    result = audit_repository_structure(Path("."))

    assert "phyng" in result.packages
    assert "phyng.repository_audit.structure" in result.modules
    assert result.schemas


def test_repository_audit_discovers_campaigns():
    result = audit_repository_structure(Path("."))

    assert "phyng.campaigns.repository_orchestration_audit" in result.campaigns
    assert any(campaign.startswith("phyng.campaigns.") for campaign in result.campaigns)
