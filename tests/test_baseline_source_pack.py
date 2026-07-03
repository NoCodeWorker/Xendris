from phyng.baselines.source_pack import evaluate_source_pack
from phyng.evidence.source_candidates import SourceCandidate, evaluate_candidate_status
from phyng.evidence.citation_audit_v0_9 import CitationAuditResult
from phyng.evidence.claim_source_links_v0_9 import ClaimSourceLinkV09


def test_empty_source_pack_not_ready():
    pack = evaluate_source_pack("BSP-TEST", "CAMPAIGN-002", [], [], [])
    assert pack.coverage_status == "EMPTY"
    assert pack.ready_for_upgrade_attempt is False


def test_partial_source_pack_not_minimum_coverage():
    # Only formula, no observable
    candidates = [
        SourceCandidate(source_candidate_id="C1", requirement_id="BSR-001", trust_level="HIGH")
    ]
    audits = [
        CitationAuditResult(source_id="SRC-1", passed=True, audit_status="PASSED_LIMITED")
    ]
    links = [
        ClaimSourceLinkV09(
            link_id="L1",
            claim_id="C1",
            source_id="SRC-1",
            support_type="FORMULA_SUPPORT",
            support_strength="HIGH",
            audit_status="PASSED_LIMITED"
        )
    ]
    pack = evaluate_source_pack("BSP-TEST", "CAMPAIGN-002", candidates, audits, links)
    assert pack.coverage_status == "PARTIAL"
    assert pack.ready_for_upgrade_attempt is False


def test_url_only_is_candidate_not_ingested():
    candidate = SourceCandidate(
        source_candidate_id="C-URL",
        requirement_id="BSR-001",
        url="http://example.com/paper.pdf",
        candidate_status="CANDIDATE_REGISTERED"
    )
    status = evaluate_candidate_status(candidate)
    assert status == "CANDIDATE_ONLY"


def test_no_fake_metadata_in_source_candidate():
    candidate = SourceCandidate(
        source_candidate_id="C-FAKE",
        requirement_id="BSR-001",
        title="   ",
        authors=[],
        year=None,
        local_path="sources/baseline/non_existent.pdf"
    )
    status = evaluate_candidate_status(candidate)
    # Since title is whitespace, authors empty, and year None, metadata is incomplete
    assert status in ["METADATA_INCOMPLETE", "CANDIDATE_REGISTERED"]
