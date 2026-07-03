"""Reports for PHI_GRADIENT source-pack validation v3.3."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.source_pack_validation.schemas import PhiGradientSourcePackValidationCampaignResult


def write_source_pack_validation_reports(
    result: PhiGradientSourcePackValidationCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "source_pack_validation"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "extract_validation": report_dir / "phi_gradient_extract_validation_v3_3.md",
        "slot_coverage": report_dir / "phi_gradient_slot_coverage_v3_3.md",
        "analogy_rejections": report_dir / "phi_gradient_analogy_rejections_v3_3.md",
        "negative_pressure": report_dir / "phi_gradient_negative_pressure_v3_3.md",
        "benchmark_comparability": report_dir / "phi_gradient_benchmark_comparability_v3_3.md",
        "final_gate": report_dir / "phi_gradient_final_gate_v3_3.md",
        "loop_feedback": report_dir / "phi_gradient_loop_feedback_v3_3.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-SOURCE-PACK-VALIDATION-v3_3.md",
    }
    renderers = {
        "extract_validation": _render_extract_validation,
        "slot_coverage": _render_slot_coverage,
        "analogy_rejections": _render_analogy,
        "negative_pressure": _render_negative,
        "benchmark_comparability": _render_benchmark,
        "final_gate": _render_gate,
        "loop_feedback": _render_loop,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: PhiGradientSourcePackValidationCampaignResult, reports_generated: list[str] | None = None) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Source Pack Validation v3.3",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="source_pack_validation",
        reports_generated=reports_generated or [],
        next_actions=gate.next_actions,
        discipline_note="A candidate source becomes evidence pressure only when its extract survives the gate.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_extract_validation(result: PhiGradientSourcePackValidationCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# PHI_GRADIENT Extract Validation v3.3",
        "",
        f"- extract_candidate_count: `{len(gate.extract_validations)}`",
        f"- validated_support_count: `{gate.validated_support_count}`",
        f"- manual_review_count: `{gate.manual_review_count}`",
        f"- rejected_analogy_count: `{gate.rejected_analogy_count}`",
        "",
        "## Results",
        "",
        *[f"- `{item.extract_id}`: `{item.status}`, support=`{item.counts_as_real_support}`" for item in gate.extract_validations],
    ]) + "\n"


def _render_slot_coverage(result: PhiGradientSourcePackValidationCampaignResult) -> str:
    coverage = result.gate_result.slot_coverage
    return "\n".join([
        "# PHI_GRADIENT Slot Coverage v3.3",
        "",
        f"- source_pressure_score: `{coverage.source_pressure_score}`",
        f"- manual_review_debt: `{coverage.manual_review_debt}`",
        "",
        "## Matrix",
        "",
        *[
            f"- `{record.slot_id}`: `{record.coverage_status}`, candidates=`{record.candidate_source_count}`, extracts=`{record.extract_count}`, validated=`{record.validated_support_count}`, manual_review=`{record.manual_review_count}`"
            for record in coverage.records
        ],
    ]) + "\n"


def _render_analogy(result: PhiGradientSourcePackValidationCampaignResult) -> str:
    rejected = [item for item in result.gate_result.extract_validations if item.status == "EXTRACT_REJECTED_ANALOGY_ONLY"]
    return "\n".join([
        "# PHI_GRADIENT Analogy Rejections v3.3",
        "",
        f"- rejected_analogy_count: `{len(rejected)}`",
        "",
        *_or_none([f"- `{item.extract_id}`" for item in rejected]),
    ]) + "\n"


def _render_negative(result: PhiGradientSourcePackValidationCampaignResult) -> str:
    negative = result.gate_result.negative_pressure
    return "\n".join([
        "# PHI_GRADIENT Negative Pressure v3.3",
        "",
        f"- status: `{negative.status}`",
        f"- negative_pressure_count: `{negative.negative_pressure_count}`",
        "",
        *_or_none([f"- `{extract_id}`" for extract_id in negative.negative_extract_ids]),
    ]) + "\n"


def _render_benchmark(result: PhiGradientSourcePackValidationCampaignResult) -> str:
    benchmark = result.gate_result.benchmark_scoring
    return "\n".join([
        "# PHI_GRADIENT Benchmark Comparability v3.3",
        "",
        f"- status: `{benchmark.status}`",
        f"- benchmark_comparable_count: `{benchmark.benchmark_comparable_count}`",
        f"- benchmark_score: `{benchmark.benchmark_score}`",
        "",
        "## Missing Requirements",
        "",
        *_or_none([f"- {item}" for item in benchmark.missing_requirements]),
    ]) + "\n"


def _render_gate(result: PhiGradientSourcePackValidationCampaignResult) -> str:
    gate = result.gate_result
    manifest_count = len(gate.manifest.entries) if gate.manifest else 0
    extract_count = len(gate.extract_pack.extracts) if gate.extract_pack else 0
    return "\n".join([
        "# PHI_GRADIENT Final Gate v3.3",
        "",
        f"- status: `{gate.status}`",
        f"- manifest_source_count: `{manifest_count}`",
        f"- extract_candidate_count: `{extract_count}`",
        f"- validated_support_count: `{gate.validated_support_count}`",
        f"- manual_review_count: `{gate.manual_review_count}`",
        f"- negative_pressure_count: `{gate.negative_pressure.negative_pressure_count}`",
        f"- benchmark_comparable_count: `{gate.benchmark_scoring.benchmark_comparable_count}`",
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


def _render_loop(result: PhiGradientSourcePackValidationCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Loop Feedback v3.3",
        "",
        f"- loop_event_id: `{result.loop_result.audit_event_id}`",
        f"- result_status: `{result.status}`",
        "",
        "## Update Proposals",
        "",
        *[f"- `{proposal.proposal_type}`: {proposal.description}" for proposal in result.update_proposals],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in result.gate_result.blocked_claims],
    ]) + "\n"


def _render_campaign(result: PhiGradientSourcePackValidationCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-SOURCE-PACK-VALIDATION-v3_3",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- validated_support_count: `{gate.validated_support_count}`",
        f"- manual_review_count: `{gate.manual_review_count}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
