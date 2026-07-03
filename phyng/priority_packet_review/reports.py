"""Reports for PHI_GRADIENT priority packet review v3.8.3."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.priority_packet_review.schemas import PhiGradientPriorityPacketReviewCampaignResult


def write_priority_packet_review_reports(
    result: PhiGradientPriorityPacketReviewCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "priority_packet_review"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "summary": report_dir / "phi_gradient_priority_packet_review_summary_v3_8_3.md",
        "validation_ready_pack": report_dir / "phi_gradient_validation_ready_extract_pack_v3_8_3.md",
        "review_decisions": report_dir / "phi_gradient_review_decisions_v3_8_3.md",
        "rejected_priority_items": report_dir / "phi_gradient_rejected_priority_items_v3_8_3.md",
        "analogy_only_items": report_dir / "phi_gradient_analogy_only_items_v3_8_3.md",
        "manual_review_queue": report_dir / "phi_gradient_manual_review_queue_v3_8_3.md",
        "next_source_pressure_gate": report_dir / "phi_gradient_next_source_pressure_gate_v3_8_3.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-PRIORITY-PACKET-REVIEW-v3_8_3.md",
    }
    renderers = {
        "summary": _render_summary,
        "validation_ready_pack": _render_pack,
        "review_decisions": _render_decisions,
        "rejected_priority_items": _render_rejected,
        "analogy_only_items": _render_analogy,
        "manual_review_queue": _render_manual,
        "next_source_pressure_gate": _render_next_gate,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: PhiGradientPriorityPacketReviewCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Priority Packet Review v3.8.3",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="priority_packet_review",
        reports_generated=reports_generated or [],
        next_actions=gate.next_actions,
        discipline_note="Promotion means ready to be judged, not judged.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_summary(result: PhiGradientPriorityPacketReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# PHI_GRADIENT Priority Packet Review Summary v3.8.3",
            "",
            f"- status: `{gate.status}`",
            f"- input_priority_packet_count: `{gate.input_priority_packet_count}`",
            f"- expanded_pedernales_slot4_count: `{gate.expanded_pedernales_slot4_count}`",
            f"- review_target_count: `{gate.review_target_count}`",
            f"- validation_ready_count: `{gate.validation_ready_count}`",
            f"- rejected_count: `{gate.rejected_count}`",
            f"- manual_review_count: `{gate.manual_review_count}`",
            f"- analogy_only_count: `{gate.analogy_only_count}`",
            f"- ready_for_v3_9: `{gate.ready_for_v3_9}`",
            "",
            "## Slot Coverage",
            "",
            *_or_none([f"- `{slot}`: `{count}`" for slot, count in sorted(gate.slot_coverage.items())]),
            "",
            "## Source Coverage",
            "",
            *_or_none([f"- `{source}`: `{count}`" for source, count in sorted(gate.source_coverage.items())]),
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in gate.blocked_claims],
        ]
    ) + "\n"


def _render_pack(result: PhiGradientPriorityPacketReviewCampaignResult) -> str:
    extracts = result.gate_result.validation_ready_pack.extracts
    return "\n".join(
        [
            "# PHI_GRADIENT Validation-Ready Extract Pack v3.8.3",
            "",
            f"- validation_ready_count: `{len(extracts)}`",
            f"- ready_for_v3_9: `{result.gate_result.ready_for_v3_9}`",
            "",
            *_or_none([f"- `{item.extract_id}`: source=`{item.source_id}`, slot=`{item.assigned_slot}`, role=`{item.component_role}`, page=`{item.page_number}`" for item in extracts[:80]]),
        ]
    ) + "\n"


def _render_decisions(result: PhiGradientPriorityPacketReviewCampaignResult) -> str:
    return "\n".join(
        [
            "# PHI_GRADIENT Review Decisions v3.8.3",
            "",
            f"- decision_count: `{len(result.gate_result.decisions)}`",
            "",
            *_or_none([f"- `{item.review_item_id}`: decision=`{item.decision}`, source=`{item.source_id}`, reason={item.reason}" for item in result.gate_result.decisions[:100]]),
        ]
    ) + "\n"


def _render_rejected(result: PhiGradientPriorityPacketReviewCampaignResult) -> str:
    return "\n".join(["# PHI_GRADIENT Rejected Priority Items v3.8.3", "", f"- rejected_count: `{len(result.gate_result.rejected_items)}`", ""]) + "\n"


def _render_analogy(result: PhiGradientPriorityPacketReviewCampaignResult) -> str:
    return "\n".join(["# PHI_GRADIENT Analogy-Only Items v3.8.3", "", f"- analogy_only_count: `{len(result.gate_result.analogy_only_items)}`", ""]) + "\n"


def _render_manual(result: PhiGradientPriorityPacketReviewCampaignResult) -> str:
    return "\n".join(["# PHI_GRADIENT Manual Review Queue v3.8.3", "", f"- manual_review_count: `{len(result.gate_result.manual_review_queue)}`", ""]) + "\n"


def _render_next_gate(result: PhiGradientPriorityPacketReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# PHI_GRADIENT Next Source Pressure Gate v3.8.3",
            "",
            f"- ready_for_v3_9: `{gate.ready_for_v3_9}`",
            f"- validation_ready_count: `{gate.validation_ready_count}`",
            f"- recommended_next_phase: `v3.9 - Source Pressure Decision Gate`",
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in gate.blocked_claims],
        ]
    ) + "\n"


def _render_campaign(result: PhiGradientPriorityPacketReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# Campaign Report - PHI-GRADIENT-PRIORITY-PACKET-REVIEW-v3_8_3",
            "",
            f"- campaign_id: `{result.campaign_id}`",
            f"- status: `{result.status}`",
            f"- input_priority_packet_count: `{gate.input_priority_packet_count}`",
            f"- expanded_pedernales_slot4_count: `{gate.expanded_pedernales_slot4_count}`",
            f"- validation_ready_count: `{gate.validation_ready_count}`",
            f"- rejected_count: `{gate.rejected_count}`",
            f"- manual_review_count: `{gate.manual_review_count}`",
            f"- analogy_only_count: `{gate.analogy_only_count}`",
            f"- ready_for_v3_9: `{gate.ready_for_v3_9}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
