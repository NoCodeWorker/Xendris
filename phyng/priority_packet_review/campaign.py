"""Campaign orchestration for PHI_GRADIENT priority packet review v3.8.3."""

from __future__ import annotations

from pathlib import Path

from phyng.core.compatibility import normalize_status
from phyng.priority_packet_review.decision_engine import review_targets
from phyng.priority_packet_review.loader import load_priority_packet_review_inputs
from phyng.priority_packet_review.pedernales_expander import build_review_targets
from phyng.priority_packet_review.reports import write_priority_packet_review_reports
from phyng.priority_packet_review.schemas import PhiGradientPriorityPacketReviewCampaignResult, PhiGradientPriorityPacketReviewGateResult
from phyng.priority_packet_review.validation_ready_pack import build_validation_ready_pack, write_v3_8_3_outputs


def run_phi_gradient_priority_packet_review_campaign(root: str | Path = ".") -> PhiGradientPriorityPacketReviewCampaignResult:
    repo_root = Path(root)
    inputs = load_priority_packet_review_inputs(repo_root)
    blocked_claims = _blocked_claims()
    if inputs.blocked_reason:
        pack = build_validation_ready_pack([], [], [], [], inputs.blocked_reason, blocked_claims)
        gate = PhiGradientPriorityPacketReviewGateResult(
            status=inputs.blocked_reason,
            canonical_status=normalize_status(inputs.blocked_reason, domain="priority_packet_review"),
            validation_ready_pack=pack,
            allowed_claims=_allowed_claims(),
            blocked_claims=blocked_claims,
            next_actions=["Regenerate v3.8.2 priority packet artifacts before v3.8.3."],
        )
        result = PhiGradientPriorityPacketReviewCampaignResult(campaign_id="PHI-GRADIENT-PRIORITY-PACKET-REVIEW-v3_8_3", status=inputs.blocked_reason, gate_result=gate)
        result.report_paths = write_priority_packet_review_reports(result, repo_root / "reports")
        return result

    targets, expanded_pedernales = build_review_targets(inputs.priority_packet, inputs.triage_records)
    extracts, decisions, rejected, analogy, manual_review = review_targets(targets, inputs.source_hashes)
    status = _status(extracts, manual_review)
    pack = build_validation_ready_pack(extracts, manual_review, rejected, analogy, status, blocked_claims)
    output_paths = write_v3_8_3_outputs(repo_root, pack, decisions, rejected, analogy, manual_review)
    gate = PhiGradientPriorityPacketReviewGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="priority_packet_review"),
        input_priority_packet_count=len(inputs.priority_packet),
        expanded_pedernales_slot4_count=expanded_pedernales,
        review_target_count=len(targets),
        validation_ready_count=pack.validation_ready_count,
        rejected_count=len(rejected),
        manual_review_count=len(manual_review),
        analogy_only_count=len(analogy),
        ready_for_v3_9=pack.ready_for_v3_9,
        source_coverage=pack.source_coverage,
        slot_coverage=pack.slot_coverage,
        validation_ready_pack=pack,
        decisions=decisions,
        rejected_items=rejected,
        analogy_only_items=analogy,
        manual_review_queue=manual_review,
        output_paths=output_paths,
        allowed_claims=_allowed_claims(),
        blocked_claims=blocked_claims,
        next_actions=_next_actions(pack.ready_for_v3_9),
    )
    result = PhiGradientPriorityPacketReviewCampaignResult(campaign_id="PHI-GRADIENT-PRIORITY-PACKET-REVIEW-v3_8_3", status=status, gate_result=gate)
    result.report_paths = write_priority_packet_review_reports(result, repo_root / "reports")
    return result


def _status(extracts: list, manual_review: list) -> str:
    if extracts:
        return "PHI_GRADIENT_PRIORITY_PACKET_REVIEW_READY_FOR_SOURCE_PRESSURE"
    if manual_review:
        return "PHI_GRADIENT_PRIORITY_PACKET_REVIEW_MANUAL_REVIEW_REQUIRED"
    return "PHI_GRADIENT_PRIORITY_PACKET_REVIEW_NO_VALIDATION_READY_EXTRACTS"


def _allowed_claims() -> list[str]:
    return [
        "Priority packet items were reviewed.",
        "Some extracts were promoted to validation-ready status.",
        "v3.9 may run as a decision gate if validation-ready extracts exist.",
    ]


def _blocked_claims() -> list[str]:
    return [
        "Validation-ready extract supports PHI_GRADIENT.",
        "Priority packet review proves source support.",
        "Pedernales proves gradient component.",
        "Benchmark candidate grants benchmark support.",
        "PHI_GRADIENT is physically validated.",
        "Frontera C is validated.",
    ]


def _next_actions(ready_for_v3_9: bool) -> list[str]:
    if ready_for_v3_9:
        return ["Run v3.9 source-pressure decision gate; it must be allowed to support, constrain, contradict, or classify as analogy-only."]
    return ["Resolve manual review items or improve extracted text before v3.9."]
