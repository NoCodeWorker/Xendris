"""Phygn v2.0 repository orchestration audit campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.repository_audit.campaigns import audit_campaigns
from phyng.repository_audit.modules import audit_dependencies, audit_module_boundaries
from phyng.repository_audit.ontology import audit_core_ontology
from phyng.repository_audit.refactor_map import generate_refactor_map
from phyng.repository_audit.report import write_repository_audit_reports
from phyng.repository_audit.reports import audit_reports
from phyng.repository_audit.schemas import RepositoryAuditCampaignResult
from phyng.repository_audit.structure import audit_repository_structure
from phyng.repository_audit.tests import audit_tests


def run_repository_orchestration_audit_campaign(root: str | Path = ".") -> RepositoryAuditCampaignResult:
    repo_root = Path(root)
    repository_audit = audit_repository_structure(repo_root)
    ontology_records = audit_core_ontology(repo_root)
    module_records = audit_module_boundaries(repo_root)
    dependency_records = audit_dependencies(repo_root)
    campaign_records = audit_campaigns(repo_root)
    report_records = audit_reports(repo_root)
    test_records = audit_tests(repo_root)
    recommendations = generate_refactor_map(repository_audit)

    result = RepositoryAuditCampaignResult(
        campaign_id="REPOSITORY-ORCHESTRATION-AUDIT-v2_0",
        version="2.0",
        status="COMPLETE_DISCOVERY_NO_BEHAVIOR_CHANGE",
        repository_audit=repository_audit,
        ontology_records=ontology_records,
        module_records=module_records,
        dependency_records=dependency_records,
        campaign_records=campaign_records,
        report_records=report_records,
        test_records=test_records,
        recommendations=recommendations,
        warnings=[
            "Audit findings are heuristic and must be reviewed before canonicalization.",
            "High-risk module moves and public API changes require human review.",
        ],
    )
    result.report_paths = write_repository_audit_reports(result, repo_root / "reports")
    return result
