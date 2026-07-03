from phyng.source_identity_preflight.decision import BLOCKED_CLAIMS, build_source_identity_preflight_gate
from phyng.source_identity_preflight.schemas import CandidatePreflightDecisionRecord


def test_no_physical_claim_created():
    assert "Any candidate is validated." in BLOCKED_CLAIMS
    assert "Any candidate has PredictiveGain." in BLOCKED_CLAIMS
    assert "Source identity preflight creates physical validation." in BLOCKED_CLAIMS


def test_no_candidate_passed_gate_status():
    decisions = [
        CandidatePreflightDecisionRecord(
            family_id="PHI_CURVATURE",
            slot4_dependency="INDEPENDENT",
            claim_risk="LOW",
            preflight_status="PREFLIGHT_FAILED_NO_RESOLVABLE_SOURCES",
            blocked_next_phases=[],
            required_next_action="lookup",
        )
    ]

    gate = build_source_identity_preflight_gate(decisions)

    assert gate.final_status == "PHYGN_SOURCE_IDENTITY_PREFLIGHT_NO_CANDIDATE_PASSED"
    assert gate.passed_candidate_count == 0
