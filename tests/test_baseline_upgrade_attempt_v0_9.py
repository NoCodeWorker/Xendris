import tempfile
from pathlib import Path
from phyng.baselines.source_pack import evaluate_source_pack
from phyng.baselines.upgrade_attempt import run_baseline_upgrade_attempt_v0_9
from phyng.evidence.source_candidates import SourceCandidate
from phyng.evidence.citation_audit_v0_9 import CitationAuditResult
from phyng.evidence.claim_source_links_v0_9 import ClaimSourceLinkV09
from phyng.campaigns.campaign_002_source_ingestion_upgrade import run_campaign_002_source_ingestion_upgrade


def test_no_sources_keeps_baseline_requires_source():
    pack = evaluate_source_pack("BSP-TEST", "CAMPAIGN-002", [], [], [])
    result = run_baseline_upgrade_attempt_v0_9(
        attempt_id="AT-1",
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        pack=pack,
        audits=[],
        links=[]
    )
    assert result.baseline_after == "BASELINE_REQUIRES_SOURCE"
    assert result.success is False


def test_metadata_only_does_not_upgrade():
    candidates = [
        SourceCandidate(source_candidate_id="C1", requirement_id="BSR-001")
    ]
    audits = [
        CitationAuditResult(source_id="S1", passed=True, audit_status="PASSED_METADATA_ONLY")
    ]
    links = [
        ClaimSourceLinkV09(
            link_id="L1",
            claim_id="CLAIM-1",
            source_id="S1",
            support_type="CONTEXT_SUPPORT",
            support_strength="MEDIUM",
            audit_status="PASSED_METADATA_ONLY"
        )
    ]
    pack = evaluate_source_pack("BSP-TEST", "CAMPAIGN-002", candidates, audits, links)
    result = run_baseline_upgrade_attempt_v0_9(
        attempt_id="AT-2",
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        pack=pack,
        audits=audits,
        links=links
    )
    assert result.baseline_after == "BASELINE_REQUIRES_DIRECT_SUPPORT"
    assert result.success is False


def test_formula_only_does_not_make_limited_baseline():
    candidates = [
        SourceCandidate(source_candidate_id="C1", requirement_id="BSR-001")
    ]
    audits = [
        CitationAuditResult(source_id="S1", passed=True, audit_status="PASSED_LIMITED")
    ]
    links = [
        ClaimSourceLinkV09(
            link_id="L1",
            claim_id="CLAIM-1",
            source_id="S1",
            support_type="FORMULA_SUPPORT",
            support_strength="HIGH",
            audit_status="PASSED_LIMITED"
        )
    ]
    pack = evaluate_source_pack("BSP-TEST", "CAMPAIGN-002", candidates, audits, links)
    result = run_baseline_upgrade_attempt_v0_9(
        attempt_id="AT-3",
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        pack=pack,
        audits=audits,
        links=links
    )
    assert result.baseline_after == "BASELINE_BACKGROUND_SUPPORTED"
    assert result.success is False


def test_formula_and_observable_support_upgrades_to_limited():
    candidates = [
        SourceCandidate(source_candidate_id="C1", requirement_id="BSR-001"),
        SourceCandidate(source_candidate_id="C2", requirement_id="BSR-003")
    ]
    audits = [
        CitationAuditResult(source_id="S1", passed=True, audit_status="PASSED_LIMITED"),
        CitationAuditResult(source_id="S2", passed=True, audit_status="PASSED_LIMITED")
    ]
    links = [
        ClaimSourceLinkV09(
            link_id="L1",
            claim_id="CLAIM-1",
            source_id="S1",
            support_type="FORMULA_SUPPORT",
            support_strength="HIGH",
            audit_status="PASSED_LIMITED"
        ),
        ClaimSourceLinkV09(
            link_id="L2",
            claim_id="CLAIM-1",
            source_id="S2",
            support_type="OBSERVABLE_SUPPORT",
            support_strength="HIGH",
            audit_status="PASSED_LIMITED"
        )
    ]
    pack = evaluate_source_pack("BSP-TEST", "CAMPAIGN-002", candidates, audits, links)
    result = run_baseline_upgrade_attempt_v0_9(
        attempt_id="AT-4",
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        pack=pack,
        audits=audits,
        links=links,
        has_parameter=False,
        has_assumptions=False
    )
    assert result.baseline_after == "BASELINE_SOURCE_BACKED_LIMITED"
    assert result.success is True


def test_parameter_and_assumptions_upgrade_to_ready():
    candidates = [
        SourceCandidate(source_candidate_id="C1", requirement_id="BSR-001"),
        SourceCandidate(source_candidate_id="C2", requirement_id="BSR-003")
    ]
    audits = [
        CitationAuditResult(source_id="S1", passed=True, audit_status="PASSED_LIMITED"),
        CitationAuditResult(source_id="S2", passed=True, audit_status="PASSED_LIMITED")
    ]
    links = [
        ClaimSourceLinkV09(
            link_id="L1",
            claim_id="CLAIM-1",
            source_id="S1",
            support_type="FORMULA_SUPPORT",
            support_strength="HIGH",
            audit_status="PASSED_LIMITED"
        ),
        ClaimSourceLinkV09(
            link_id="L2",
            claim_id="CLAIM-1",
            source_id="S2",
            support_type="OBSERVABLE_SUPPORT",
            support_strength="HIGH",
            audit_status="PASSED_LIMITED"
        )
    ]
    pack = evaluate_source_pack("BSP-TEST", "CAMPAIGN-002", candidates, audits, links)
    result = run_baseline_upgrade_attempt_v0_9(
        attempt_id="AT-5",
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        pack=pack,
        audits=audits,
        links=links,
        has_parameter=True,
        has_assumptions=True
    )
    assert result.baseline_after == "BASELINE_SOURCE_BACKED_READY"
    assert result.success is True


def test_contradiction_blocks_upgrade():
    candidates = [
        SourceCandidate(source_candidate_id="C1", requirement_id="BSR-001")
    ]
    audits = [
        CitationAuditResult(source_id="S1", passed=False, audit_status="FAILED_CONTRADICTORY")
    ]
    links = [
        ClaimSourceLinkV09(
            link_id="L1",
            claim_id="CLAIM-1",
            source_id="S1",
            support_type="CONTRADICTION",
            support_strength="HIGH",
            audit_status="FAILED_CONTRADICTORY"
        )
    ]
    pack = evaluate_source_pack("BSP-TEST", "CAMPAIGN-002", candidates, audits, links)
    result = run_baseline_upgrade_attempt_v0_9(
        attempt_id="AT-6",
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        pack=pack,
        audits=audits,
        links=links
    )
    assert result.baseline_after == "BASELINE_CONTRADICTED"
    assert result.success is False


def test_limited_baseline_does_not_unlock_candidate_prediction():
    candidates = [
        SourceCandidate(source_candidate_id="C1", requirement_id="BSR-001"),
        SourceCandidate(source_candidate_id="C2", requirement_id="BSR-003")
    ]
    audits = [
        CitationAuditResult(source_id="S1", passed=True, audit_status="PASSED_LIMITED"),
        CitationAuditResult(source_id="S2", passed=True, audit_status="PASSED_LIMITED")
    ]
    links = [
        ClaimSourceLinkV09(
            link_id="L1",
            claim_id="CLAIM-1",
            source_id="S1",
            support_type="FORMULA_SUPPORT",
            support_strength="HIGH",
            audit_status="PASSED_LIMITED"
        ),
        ClaimSourceLinkV09(
            link_id="L2",
            claim_id="CLAIM-1",
            source_id="S2",
            support_type="OBSERVABLE_SUPPORT",
            support_strength="HIGH",
            audit_status="PASSED_LIMITED"
        )
    ]
    pack = evaluate_source_pack("BSP-TEST", "CAMPAIGN-002", candidates, audits, links)
    result = run_baseline_upgrade_attempt_v0_9(
        attempt_id="AT-7",
        campaign_id="CAMPAIGN-002",
        baseline_before="TOY_INTERNAL",
        pack=pack,
        audits=audits,
        links=links
    )
    # Check that candidate physical prediction is blocked
    assert any("predicts" in claim.lower() for claim in result.blocked_claims)
    assert any("validated" in claim.lower() for claim in result.blocked_claims)


def test_empty_source_pack_run_upgrade_fails_honestly():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        attempt = run_campaign_002_source_ingestion_upgrade(tmp_path)
        assert attempt.baseline_after == "BASELINE_REQUIRES_SOURCE"
        assert attempt.success is False
        
        # Check that reports were generated
        assert (tmp_path / "reports" / "rag" / "baseline_source_pack.md").exists()
        assert (tmp_path / "reports" / "rag" / "baseline_source_candidates.md").exists()
        assert (tmp_path / "reports" / "rag" / "citation_audit_v0_9.md").exists()
        assert (tmp_path / "reports" / "rag" / "claim_source_links_v0_9.md").exists()
        assert (tmp_path / "reports" / "campaigns" / "CAMPAIGN-002_baseline_upgrade_attempt_v0_9.md").exists()
        assert (tmp_path / "reports" / "model_comparison" / "baseline_upgrade_attempt_v0_9.md").exists()
