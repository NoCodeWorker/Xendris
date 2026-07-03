from phyng.closed_loop.meta_loop import classify_meta_change_risk, propose_meta_improvement
from phyng.closed_loop.schemas import MetaChangeProposal, MetaObservation
from phyng.core.compatibility import normalize_status


def test_meta_change_risk_classifies_gate_change_as_high_risk():
    proposal = MetaChangeProposal(
        proposal_id="META-HIGH-001",
        change_type="GATE_THRESHOLD_CHANGE",
        description="Relax gate threshold",
        current_behavior="strict",
        proposed_behavior="less strict",
        canonical_status=normalize_status("META_CHANGE_PROPOSED", domain="closed_loop"),
    )

    classified = classify_meta_change_risk(proposal)

    assert classified.risk_level == "HIGH"
    assert classified.requires_human_review is True


def test_high_risk_meta_change_requires_human_review():
    observation = MetaObservation(
        observation_id="OBS-HIGH-001",
        source="test",
        observation_type="gate",
        summary="change claim permission",
        evidence={"change_type": "CLAIM_PERMISSION_CHANGE"},
    )

    proposal = propose_meta_improvement(observation)

    assert proposal.risk_level == "HIGH"
    assert proposal.requires_shadow_mode is True
    assert proposal.requires_human_review is True
