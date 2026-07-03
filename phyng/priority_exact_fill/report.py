"""Reports for PHI_GRADIENT priority exact fill v3.5."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.priority_exact_fill.schemas import PhiGradientPriorityExactFillCampaignResult


def write_priority_exact_fill_reports(
    result: PhiGradientPriorityExactFillCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "priority_exact_fill"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "source_review": report_dir / "phi_gradient_priority_source_review_v3_5.md",
        "exact_extracts": report_dir / "phi_gradient_priority_exact_extracts_v3_5.md",
        "locations": report_dir / "phi_gradient_priority_locations_v3_5.md",
        "equation_observable_map": report_dir / "phi_gradient_priority_equation_observable_map_v3_5.md",
        "parameter_ranges": report_dir / "phi_gradient_priority_parameter_ranges_v3_5.md",
        "risk_and_negative_pressure": report_dir / "phi_gradient_priority_risk_and_negative_pressure_v3_5.md",
        "next_gate": report_dir / "phi_gradient_priority_next_gate_v3_5.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5.md",
    }
    renderers = {
        "source_review": _render_source_review,
        "exact_extracts": _render_exact_extracts,
        "locations": _render_locations,
        "equation_observable_map": _render_equation_map,
        "parameter_ranges": _render_parameter_ranges,
        "risk_and_negative_pressure": _render_risk,
        "next_gate": _render_next_gate,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: PhiGradientPriorityExactFillCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Priority Exact Fill v3.5",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="priority_exact_fill",
        reports_generated=reports_generated or [],
        next_actions=gate.next_actions,
        discipline_note="The smallest useful exact extract is worth more than a large decorative bibliography.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_source_review(result: PhiGradientPriorityExactFillCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# PHI_GRADIENT Priority Source Review v3.5",
            "",
            f"- status: `{gate.status}`",
            f"- priority_sources_processed: `{gate.priority_source_count}`",
            f"- validation_ready_count: `{gate.validation_ready_count}`",
            f"- unresolved_count: `{gate.unresolved_count}`",
            "",
            "## Priority Sources Processed",
            "",
            *_or_none(
                [
                    f"- `{item.priority_source_id}` -> `{item.matched_source_id}`: `{item.source_text_status}`"
                    for item in gate.source_availability
                ]
            ),
            "",
            "## Source Text Availability",
            "",
            *_or_none([f"- `{item.priority_source_id}`: `{item.source_text_status}`" for item in gate.source_availability]),
        ]
    ) + "\n"


def _render_exact_extracts(result: PhiGradientPriorityExactFillCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# PHI_GRADIENT Priority Exact Extracts v3.5",
            "",
            f"- validation_ready_count: `{gate.validation_ready_count}`",
            f"- unresolved_count: `{gate.unresolved_count}`",
            "",
            "## Exact Fill Records",
            "",
            *_or_none(
                [
                    f"- `{record.priority_source_id}`: `{record.review_status}`, ready=`{record.validation_ready}`"
                    for record in gate.priority_records
                ]
            ),
        ]
    ) + "\n"


def _render_locations(result: PhiGradientPriorityExactFillCampaignResult) -> str:
    return "\n".join(
        [
            "# PHI_GRADIENT Priority Locations v3.5",
            "",
            *_or_none(
                [
                    f"- `{item.priority_source_id}`: `{item.status}`, missing=`{', '.join(item.missing_requirements)}`"
                    for item in result.gate_result.location_records
                ]
            ),
        ]
    ) + "\n"


def _render_equation_map(result: PhiGradientPriorityExactFillCampaignResult) -> str:
    entries = result.gate_result.equation_observable_map.entries
    return "\n".join(
        [
            "# PHI_GRADIENT Priority Equation Observable Map v3.5",
            "",
            f"- mapped_entries: `{len(entries)}`",
            "",
            *_or_none([f"- `{entry.priority_source_id}`: `{entry.candidate_relevance}`" for entry in entries]),
        ]
    ) + "\n"


def _render_parameter_ranges(result: PhiGradientPriorityExactFillCampaignResult) -> str:
    entries = result.gate_result.parameter_range_map.entries
    return "\n".join(
        [
            "# PHI_GRADIENT Priority Parameter Ranges v3.5",
            "",
            f"- mapped_entries: `{len(entries)}`",
            "",
            *_or_none([f"- `{entry.priority_source_id}`: `{entry.comparability_status}`" for entry in entries]),
        ]
    ) + "\n"


def _render_risk(result: PhiGradientPriorityExactFillCampaignResult) -> str:
    gate = result.gate_result
    negative = [record for record in gate.priority_records if record.negative_constraint_text or record.contradicted_components]
    return "\n".join(
        [
            "# PHI_GRADIENT Priority Risk and Negative Pressure v3.5",
            "",
            f"- risk_flags: `{sum(len(record.risk_flags) for record in gate.priority_records)}`",
            f"- negative_candidates: `{gate.negative_candidate_count}`",
            "",
            "## Risk Flags",
            "",
            *_or_none([f"- `{record.priority_source_id}`: `{', '.join(record.risk_flags)}`" for record in gate.priority_records]),
            "",
            "## Negative Candidates",
            "",
            *_or_none([f"- `{record.priority_source_id}`: `{', '.join(record.contradicted_components)}`" for record in negative]),
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in gate.blocked_claims],
        ]
    ) + "\n"


def _render_next_gate(result: PhiGradientPriorityExactFillCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# PHI_GRADIENT Priority Next Gate v3.5",
            "",
            f"- status: `{gate.status}`",
            f"- validation_ready_count: `{gate.validation_ready_count}`",
            f"- unresolved_count: `{gate.unresolved_count}`",
            "",
            "## Next Actions",
            "",
            *[f"- {action}" for action in gate.next_actions],
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in gate.blocked_claims],
        ]
    ) + "\n"


def _render_campaign(result: PhiGradientPriorityExactFillCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join(
        [
            "# Campaign Report - PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5",
            "",
            f"- campaign_id: `{result.campaign_id}`",
            f"- status: `{result.status}`",
            f"- priority_sources_processed: `{gate.priority_source_count}`",
            f"- validation_ready_count: `{gate.validation_ready_count}`",
            f"- unresolved_count: `{gate.unresolved_count}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
