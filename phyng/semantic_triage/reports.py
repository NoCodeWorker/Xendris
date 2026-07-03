"""Reports for PHI_GRADIENT semantic triage v3.8.2."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.semantic_triage.schemas import PhiGradientSemanticTriageCampaignResult


def write_semantic_triage_reports(
    result: PhiGradientSemanticTriageCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "semantic_triage"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "summary": report_dir / "phi_gradient_semantic_triage_summary_v3_8_2.md",
        "priority_review_packet": report_dir / "phi_gradient_priority_review_packet_v3_8_2.md",
        "slot_review_queues": report_dir / "phi_gradient_slot_review_queues_v3_8_2.md",
        "low_value_exclusions": report_dir / "phi_gradient_low_value_exclusions_v3_8_2.md",
        "next_gate_readiness": report_dir / "phi_gradient_next_gate_readiness_v3_8_2.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-SEMANTIC-TRIAGE-v3_8_2.md",
    }
    renderers = {
        "summary": _render_summary,
        "priority_review_packet": _render_packet,
        "slot_review_queues": _render_slot_queues,
        "low_value_exclusions": _render_exclusions,
        "next_gate_readiness": _render_next_gate,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: PhiGradientSemanticTriageCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Semantic Triage v3.8.2",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="semantic_triage",
        reports_generated=reports_generated or [],
        next_actions=gate.next_actions,
        discipline_note="v3.8.2 chooses what deserves attention. v3.8.3 reviews it. v3.9 judges it.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_summary(result: PhiGradientSemanticTriageCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# PHI_GRADIENT Semantic Triage Summary v3.8.2",
            "",
            f"- status: `{gate.status}`",
            f"- input_candidate_count: `{gate.input_candidate_count}`",
            f"- triaged_candidate_count: `{gate.triaged_candidate_count}`",
            f"- priority_packet_count: `{gate.priority_packet_count}`",
            f"- critical_count: `{gate.critical_count}`",
            f"- high_count: `{gate.high_count}`",
            f"- validation_ready_count_inherited: `{gate.validation_ready_count}`",
            f"- pedernales_slot4_count: `{gate.pedernales_slot4_count}`",
            f"- ready_for_v3_9: `{gate.next_gate_readiness.ready_for_v3_9}`",
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


def _render_packet(result: PhiGradientSemanticTriageCampaignResult) -> str:
    packet = result.gate_result.priority_packet
    return "\n".join(
        [
            "# PHI_GRADIENT Priority Review Packet v3.8.2",
            "",
            f"- packet_count: `{len(packet)}`",
            "",
            *_or_none(
                [
                    f"- `{item.review_item_id}`: priority=`{item.priority}`, slot=`{item.assigned_slot}`, source=`{item.source_id}`, page=`{item.page_number}`"
                    for item in packet
                ]
            ),
            "",
            "Packet items are review targets only; they are not source support.",
        ]
    ) + "\n"


def _render_slot_queues(result: PhiGradientSemanticTriageCampaignResult) -> str:
    queues = result.gate_result.slot_review_queues
    lines = ["# PHI_GRADIENT Slot Review Queues v3.8.2", ""]
    for queue in queues:
        lines.extend(
            [
                f"## {queue.slot_id}",
                "",
                f"- item_count: `{len(queue.items)}`",
                f"- critical_count: `{queue.critical_count}`",
                f"- high_count: `{queue.high_count}`",
                f"- medium_count: `{queue.medium_count}`",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def _render_exclusions(result: PhiGradientSemanticTriageCampaignResult) -> str:
    exclusions = result.gate_result.low_value_exclusions
    return "\n".join(
        [
            "# PHI_GRADIENT Low-Value Exclusions v3.8.2",
            "",
            f"- low_value_count: `{len(exclusions)}`",
            "",
            *_or_none([f"- `{item.candidate_id}`: score=`{item.triage_score}`, reason={item.reason}" for item in exclusions[:80]]),
        ]
    ) + "\n"


def _render_next_gate(result: PhiGradientSemanticTriageCampaignResult) -> str:
    readiness = result.gate_result.next_gate_readiness
    return "\n".join(
        [
            "# PHI_GRADIENT Next Gate Readiness v3.8.2",
            "",
            f"- status: `{readiness.status}`",
            f"- priority_packet_count: `{readiness.priority_packet_count}`",
            f"- critical_count: `{readiness.critical_count}`",
            f"- high_count: `{readiness.high_count}`",
            f"- manual_review_required: `{readiness.manual_review_required}`",
            f"- ready_for_v3_9: `{readiness.ready_for_v3_9}`",
            f"- reason: {readiness.reason}",
            f"- recommended_next_action: {readiness.recommended_next_action}",
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in readiness.blocked_claims],
        ]
    ) + "\n"


def _render_campaign(result: PhiGradientSemanticTriageCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# Campaign Report - PHI-GRADIENT-SEMANTIC-TRIAGE-v3_8_2",
            "",
            f"- campaign_id: `{result.campaign_id}`",
            f"- status: `{result.status}`",
            f"- input_candidate_count: `{gate.input_candidate_count}`",
            f"- triaged_candidate_count: `{gate.triaged_candidate_count}`",
            f"- priority_packet_count: `{gate.priority_packet_count}`",
            f"- critical_count: `{gate.critical_count}`",
            f"- high_count: `{gate.high_count}`",
            f"- validation_ready_count_inherited: `{gate.validation_ready_count}`",
            f"- ready_for_v3_9: `{gate.next_gate_readiness.ready_for_v3_9}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
