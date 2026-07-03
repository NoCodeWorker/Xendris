"""
Tests for phyng.evidence.real_source_candidates
"""

from phyng.evidence.real_source_candidates import get_baseline_real_source_candidates, RealSourceCandidate

def test_real_candidates_exist():
    candidates = get_baseline_real_source_candidates()
    assert len(candidates) > 0
    for c in candidates:
        assert isinstance(c, RealSourceCandidate)
        assert c.source_candidate_id.startswith("SRC-BASE-")
        assert len(c.intended_support_types) > 0
        assert c.trust_level == "HIGH"

def test_candidates_are_not_ingested():
    candidates = get_baseline_real_source_candidates()
    for c in candidates:
        # Before ingestion they must have local_file_status as MISSING
        assert c.local_file_status == "MISSING"
        # Verification status should not be fully ready/extracted without audit
        assert c.verification_status != "READY_FOR_EXTRACTION"
