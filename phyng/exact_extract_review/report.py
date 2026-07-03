"""Reports for exact extract review v3.4."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.exact_extract_review.schemas import PhiGradientExactExtractReviewCampaignResult


def write_exact_extract_review_reports(
    result: PhiGradientExactExtractReviewCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "exact_extract_review"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "exact_extracts": report_dir / "phi_gradient_exact_extracts_v3_4.md",
        "locations": report_dir / "phi_gradient_exact_extract_locations_v3_4.md",
        "equation_observable_map": report_dir / "phi_gradient_equation_observable_map_v3_4.md",
        "parameter_ranges": report_dir / "phi_gradient_parameter_ranges_v3_4.md",
        "manual_review_resolution": report_dir / "phi_gradient_manual_review_resolution_v3_4.md",
        "next_gate": report_dir / "phi_gradient_next_gate_v3_4.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-EXACT-EXTRACT-REVIEW-v3_4.md",
    }
    renderers = {
        "exact_extracts": _render_extracts,
        "locations": _render_locations,
        "equation_observable_map": _render_equation_map,
        "parameter_ranges": _render_parameter_ranges,
        "manual_review_resolution": _render_manual_review,
        "next_gate": _render_next_gate,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: PhiGradientExactExtractReviewCampaignResult, reports_generated: list[str] | None = None) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Exact Extract Review v3.4",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="exact_extract_review",
        reports_generated=reports_generated or [],
        next_actions=gate.next_actions,
        discipline_note="Exactness is the price a source pays to become pressure.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_extracts(result: PhiGradientExactExtractReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# PHI_GRADIENT Exact Extracts v3.4",
        "",
        f"- exact_extracts_acquired: `{gate.exact_extract_count}`",
        f"- validation_ready_extracts: `{gate.validation_ready_count}`",
        f"- unresolved_extracts: `{gate.unresolved_extract_count}`",
        "",
        "## Extracts",
        "",
        *[f"- `{extract.exact_extract_id}`: `{extract.review_status}`, location=`{extract.location_type}:{extract.location_value}`" for extract in gate.exact_extract_pack.extracts],
    ]) + "\n"


def _render_locations(result: PhiGradientExactExtractReviewCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Exact Extract Locations v3.4",
        "",
        *[f"- `{item.exact_extract_id}`: `{item.status}`, ready=`{item.validation_ready}`, missing=`{', '.join(item.missing_requirements)}`" for item in result.gate_result.location_results],
    ]) + "\n"


def _render_equation_map(result: PhiGradientExactExtractReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# PHI_GRADIENT Equation Observable Map v3.4",
        "",
        f"- equation_map_count: `{gate.equation_map_count}`",
        f"- observable_map_count: `{gate.observable_map_count}`",
        "",
        *_or_none([f"- `{entry.exact_extract_id}`: `{entry.model_role}`" for entry in gate.equation_observable_map.entries]),
    ]) + "\n"


def _render_parameter_ranges(result: PhiGradientExactExtractReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# PHI_GRADIENT Parameter Ranges v3.4",
        "",
        f"- parameter_range_count: `{gate.parameter_range_count}`",
        f"- benchmark_range_count: `{gate.benchmark_range_count}`",
        f"- negative_constraint_count: `{gate.negative_constraint_count}`",
        "",
        *_or_none([f"- `{entry.exact_extract_id}`: `{entry.comparability_status}`" for entry in gate.parameter_range_map.entries]),
    ]) + "\n"


def _render_manual_review(result: PhiGradientExactExtractReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# PHI_GRADIENT Manual Review Resolution v3.4",
        "",
        f"- manual_review_debt_before: `{gate.manual_review_debt_before}`",
        f"- manual_review_debt_after: `{gate.manual_review_debt_after}`",
        f"- validation_ready_extracts: `{gate.validation_ready_count}`",
        f"- unresolved_extracts: `{gate.unresolved_extract_count}`",
    ]) + "\n"


def _render_next_gate(result: PhiGradientExactExtractReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# PHI_GRADIENT Next Gate v3.4",
        "",
        f"- status: `{gate.status}`",
        "",
        "## Allowed Claims",
        "",
        *[f"- {claim}" for claim in gate.allowed_claims],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in gate.blocked_claims],
        "",
        "## Next Actions",
        "",
        *[f"- {action}" for action in gate.next_actions],
    ]) + "\n"


def _render_campaign(result: PhiGradientExactExtractReviewCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-EXACT-EXTRACT-REVIEW-v3_4",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- manual_review_debt_before: `{gate.manual_review_debt_before}`",
        f"- manual_review_debt_after: `{gate.manual_review_debt_after}`",
        f"- validation_ready_extracts: `{gate.validation_ready_count}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
