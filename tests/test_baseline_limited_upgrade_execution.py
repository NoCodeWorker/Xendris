"""
Unit tests for phyng.baselines.limited_upgrade_execution
"""

from pathlib import Path

import pytest

from phyng.baselines.limited_upgrade_execution import (
    BaselineUpgradeExecutionResult,
    _candidate_to_record,
    _link_from_audit,
    run_limited_upgrade_execution,
)
from phyng.evidence.citation_audit_v0_9 import CitationAuditResult
from phyng.evidence.source_candidates import SourceCandidate
from phyng.evidence.source_records_v0_9 import SourceRecordV09


# ── Helpers ────────────────────────────────────────────────────────────────

def _make_candidate(local_path: str | None = None, req_id: str = "BSR-001") -> SourceCandidate:
    return SourceCandidate(
        source_candidate_id="CAND-001",
        requirement_id=req_id,
        title="Test Paper",
        authors=["Author A"],
        year="2024",
        source_type="PAPER",
        local_path=local_path,
        url=None,
        trust_level="HIGH",
        notes="A test note.",
        candidate_status="REGISTERED_NEEDS_METADATA",
    )


def _make_audit(source_id: str, passed: bool) -> CitationAuditResult:
    return CitationAuditResult(
        source_id=source_id,
        audit_status="PASSED_LIMITED" if passed else "FAILED_NO_LOCAL_CONTENT",
        passed=passed,
        has_formula_support=passed,
        has_observable_support=passed,
        has_parameter_support=False,
        has_contradiction=False,
        trust_issues=[],
        extraction_issues=[] if passed else ["No local file found."],
        missing_fields=[],
    )


# ── _candidate_to_record ───────────────────────────────────────────────────

class TestCandidateToRecord:
    def test_no_local_path_gives_not_ingested(self) -> None:
        cand = _make_candidate(local_path=None)
        record = _candidate_to_record(cand, 0)
        assert record.ingestion_status == "NOT_INGESTED"
        assert record.metadata_status == "UNKNOWN"
        assert record.source_id == "SRC-V10-001"

    def test_nonexistent_local_path_gives_not_ingested(self, tmp_path: Path) -> None:
        cand = _make_candidate(local_path=str(tmp_path / "missing.pdf"))
        record = _candidate_to_record(cand, 1)
        assert record.ingestion_status == "NOT_INGESTED"

    def test_existing_local_path_gives_ingested(self, tmp_path: Path) -> None:
        f = tmp_path / "paper.pdf"
        f.write_bytes(b"content")
        cand = _make_candidate(local_path=str(f))
        record = _candidate_to_record(cand, 2)
        assert record.ingestion_status == "INGESTED_WITH_EXTRACTS"
        assert record.metadata_status == "COMPLETE"

    def test_existing_path_partial_metadata(self, tmp_path: Path) -> None:
        f = tmp_path / "paper.pdf"
        f.write_bytes(b"x")
        cand = SourceCandidate(
            source_candidate_id="CAND-X",
            requirement_id="BSR-001",
            title=None,
            authors=[],
            year=None,
            source_type="PAPER",
            local_path=str(f),
            url=None,
            trust_level="HIGH",
            notes=None,
            candidate_status="REGISTERED_NEEDS_METADATA",
        )
        record = _candidate_to_record(cand, 0)
        assert record.metadata_status == "PARTIAL"


# ── _link_from_audit ───────────────────────────────────────────────────────

class TestLinkFromAudit:
    def test_failed_audit_returns_none(self, tmp_path: Path) -> None:
        cand = _make_candidate()
        record = _candidate_to_record(cand, 0)
        audit = _make_audit(record.source_id, passed=False)
        result = _link_from_audit(record, audit, "BSR-001", 0, cand)
        assert result is None

    def test_passed_audit_creates_link(self, tmp_path: Path) -> None:
        cand = _make_candidate()
        record = _candidate_to_record(cand, 0)
        audit = _make_audit(record.source_id, passed=True)
        link = _link_from_audit(record, audit, "BSR-001", 0, cand)
        assert link is not None
        assert link.support_type == "FORMULA_SUPPORT"
        assert link.support_strength == "HIGH"
        assert link.audit_status == "PASSED_LIMITED"

    def test_bsr003_maps_to_observable_support(self) -> None:
        cand = _make_candidate(req_id="BSR-003")
        record = _candidate_to_record(cand, 0)
        audit = _make_audit(record.source_id, passed=True)
        link = _link_from_audit(record, audit, "BSR-003", 0, cand)
        assert link is not None
        assert link.support_type == "OBSERVABLE_SUPPORT"

    def test_bsr004_maps_to_context_support(self) -> None:
        cand = _make_candidate(req_id="BSR-004")
        record = _candidate_to_record(cand, 0)
        audit = _make_audit(record.source_id, passed=True)
        link = _link_from_audit(record, audit, "BSR-004", 0, cand)
        assert link is not None
        assert link.support_type == "CONTEXT_SUPPORT"

    def test_long_notes_not_included_as_excerpt(self) -> None:
        cand = SourceCandidate(
            source_candidate_id="C",
            requirement_id="BSR-001",
            title="T",
            authors=[],
            year="2024",
            source_type="PAPER",
            local_path=None,
            url=None,
            trust_level="HIGH",
            notes="x" * 300,
            candidate_status="REGISTERED_NEEDS_METADATA",
        )
        record = _candidate_to_record(cand, 0)
        audit = _make_audit(record.source_id, passed=True)
        link = _link_from_audit(record, audit, "BSR-001", 0, cand)
        assert link is not None
        assert link.quote_or_excerpt is None


# ── run_limited_upgrade_execution (integration) ────────────────────────────

class TestRunLimitedUpgradeExecution:
    def test_empty_sources_dir_stays_baseline_requires_source(self, tmp_path: Path) -> None:
        baseline = tmp_path / "sources" / "baseline"
        baseline.mkdir(parents=True)
        result = run_limited_upgrade_execution(project_root=tmp_path)

        assert result.upgrade_success is False
        assert result.audited_sources_count == 0
        assert "BASELINE_REQUIRES_SOURCE" in result.baseline_after

    def test_no_sources_dir_stays_baseline_requires_source(self, tmp_path: Path) -> None:
        result = run_limited_upgrade_execution(project_root=tmp_path)
        assert result.upgrade_success is False

    def test_result_always_has_blocked_claims(self, tmp_path: Path) -> None:
        result = run_limited_upgrade_execution(project_root=tmp_path)
        assert len(result.blocked_claims) >= 3
        assert any("predict" in c.lower() or "validated" in c.lower() for c in result.blocked_claims)

    def test_report_paths_generated(self, tmp_path: Path) -> None:
        baseline = tmp_path / "sources" / "baseline"
        baseline.mkdir(parents=True)
        result = run_limited_upgrade_execution(project_root=tmp_path)
        assert len(result.report_paths) == 6
        for rp in result.report_paths:
            assert Path(rp).exists()

    def test_execution_id_propagated(self, tmp_path: Path) -> None:
        result = run_limited_upgrade_execution(
            project_root=tmp_path, execution_id="EXEC-TEST-999"
        )
        assert result.execution_id == "EXEC-TEST-999"

    def test_campaign_id_is_fixed(self, tmp_path: Path) -> None:
        result = run_limited_upgrade_execution(project_root=tmp_path)
        assert result.campaign_id == "BASELINE-SRC-PACK-001"
        assert result.linked_campaign_id == "CAMPAIGN-002"
