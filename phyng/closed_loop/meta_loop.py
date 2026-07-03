"""Meta-improvement proposal and risk classification."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.closed_loop.schemas import MetaChangeProposal, MetaObservation


LOW_RISK = {"REPORT_TEMPLATE_CHANGE", "WARNING_TEMPLATE_CHANGE", "QUESTION_PRIORITY_CHANGE", "HEURISTIC_WEIGHT_CHANGE"}
MEDIUM_RISK = {"CANONICAL_MAPPING_ADDITION", "MODEL_ROUTING_CHANGE", "BENCHMARK_DESIGN_UPDATE"}
HIGH_RISK = {
    "CANONICAL_MAPPING_CHANGE",
    "GATE_THRESHOLD_CHANGE",
    "CLAIM_PERMISSION_CHANGE",
    "SOURCE_REQUIREMENT_CHANGE",
    "BENCHMARK_REQUIREMENT_CHANGE",
    "FINANCIAL_GATE_CHANGE",
    "EXECUTION_GATE_CHANGE",
}


def propose_meta_improvement(observation: MetaObservation) -> MetaChangeProposal:
    change_type = observation.evidence.get("change_type", "REPORT_TEMPLATE_CHANGE")
    return classify_meta_change_risk(
        MetaChangeProposal(
            proposal_id=f"{observation.observation_id}-META-001",
            change_type=change_type,
            description=f"Meta-improvement proposed from observation: {observation.summary}",
            affected_modules=observation.evidence.get("affected_modules", ["reports"]),
            current_behavior=observation.evidence.get("current_behavior", "Current behavior recorded."),
            proposed_behavior=observation.evidence.get("proposed_behavior", "Improve warning/report clarity."),
            canonical_status=normalize_status("META_CHANGE_PROPOSED", domain="closed_loop"),
        )
    )


def classify_meta_change_risk(proposal: MetaChangeProposal) -> MetaChangeProposal:
    if proposal.change_type in HIGH_RISK:
        risk = "HIGH"
        shadow = True
        review = True
        status = "META_CHANGE_REQUIRES_HUMAN_REVIEW"
    elif proposal.change_type in MEDIUM_RISK:
        risk = "MEDIUM"
        shadow = True
        review = True
        status = "META_CHANGE_REQUIRES_HUMAN_REVIEW"
    else:
        risk = "LOW"
        shadow = False
        review = False
        status = "META_CHANGE_APPROVED_LOW_RISK"
    return proposal.model_copy(
        update={
            "risk_level": risk,
            "requires_shadow_mode": shadow,
            "requires_human_review": review,
            "expected_behavior_change": risk != "LOW",
            "canonical_status": normalize_status(status, domain="closed_loop"),
        },
        deep=True,
    )
