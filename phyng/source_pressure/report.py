"""Report writers for PHI_GRADIENT source and benchmark pressure."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.source_pressure.schemas import PhiGradientSourceBenchmarkCampaignResult


def write_phi_gradient_source_pressure_reports(
    result: PhiGradientSourceBenchmarkCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    source_dir = root / "source_pressure"
    campaigns_dir = root / "campaigns"
    source_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "slots": source_dir / "phi_gradient_source_slots_v2_8.md",
        "source_gate": source_dir / "phi_gradient_source_support_gate_v2_8.md",
        "benchmark": source_dir / "phi_gradient_benchmark_pressure_v2_8.md",
        "negative_sources": source_dir / "phi_gradient_negative_sources_v2_8.md",
        "loop_feedback": source_dir / "phi_gradient_source_benchmark_loop_feedback_v2_8.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-SOURCE-BENCHMARK-PRESSURE-v2_8.md",
    }
    paths["slots"].write_text(_canonical(_render_slots(result), result, status=result.source_result.status), encoding="utf-8")
    paths["source_gate"].write_text(_canonical(_render_source_gate(result), result, status=result.source_result.status), encoding="utf-8")
    paths["benchmark"].write_text(_canonical(_render_benchmark(result), result), encoding="utf-8")
    paths["negative_sources"].write_text(_canonical(_render_negative(result), result, status=result.source_result.status), encoding="utf-8")
    paths["loop_feedback"].write_text(_canonical(_render_loop(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: PhiGradientSourceBenchmarkCampaignResult,
    reports_generated: list[str] | None = None,
    status: str | None = None,
) -> str:
    contract = build_report_contract(
        title="PHI_GRADIENT Source Benchmark Pressure v2.8",
        campaign_id=result.campaign_id,
        domain_status=status or result.status,
        domain="source_pressure",
        reports_generated=reports_generated or [],
        discipline_note="A source is useful when it can constrain or hurt the candidate; analogy is not support.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_slots(result: PhiGradientSourceBenchmarkCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Source Slots v2.8",
        "",
        *[
            f"- `{slot.slot_id}`: {slot.required_component}; acceptable=`{', '.join(slot.acceptable_support_types)}`"
            for slot in result.source_result.slots
        ],
    ]) + "\n"


def _render_source_gate(result: PhiGradientSourceBenchmarkCampaignResult) -> str:
    lines = ["# PHI_GRADIENT Source Support Gate v2.8", ""]
    lines.extend([
        f"- status: `{result.source_result.status}`",
        f"- fixture_based: `{result.source_result.fixture_based}`",
        "",
        "## Assessments",
        "",
    ])
    for assessment in result.source_result.assessments:
        lines.append(f"- `{assessment.source_id}`: `{assessment.status}`, counts_as_support=`{assessment.counts_as_support}`")
    lines.extend([
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in result.source_result.blocked_claims],
    ])
    return "\n".join(lines) + "\n"


def _render_benchmark(result: PhiGradientSourceBenchmarkCampaignResult) -> str:
    lines = ["# PHI_GRADIENT Benchmark Pressure v2.8", ""]
    for benchmark in result.benchmark_results:
        lines.append(f"- `{benchmark.benchmark_id}`: `{benchmark.status}`, counts_as_benchmark_support=`{benchmark.counts_as_benchmark_support}`")
    return "\n".join(lines) + "\n"


def _render_negative(result: PhiGradientSourceBenchmarkCampaignResult) -> str:
    lines = ["# PHI_GRADIENT Negative Sources v2.8", ""]
    if not result.source_result.negative_sources:
        lines.append("- No unaddressed negative fixture source in campaign seed set.")
    for assessment in result.source_result.negative_sources:
        lines.append(f"- `{assessment.source_id}`: `{', '.join(assessment.contradicted_components)}`")
    return "\n".join(lines) + "\n"


def _render_loop(result: PhiGradientSourceBenchmarkCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Source Benchmark Loop Feedback v2.8",
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
        *[f"- {claim}" for claim in result.source_result.blocked_claims],
        "",
        "## Next Actions",
        "",
        *[f"- {action}" for action in result.source_result.next_actions],
    ]) + "\n"


def _render_campaign(result: PhiGradientSourceBenchmarkCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-SOURCE-BENCHMARK-PRESSURE-v2_8",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- source_status: `{result.source_result.status}`",
        f"- benchmark_statuses: `{', '.join(item.status for item in result.benchmark_results)}`",
        "- fixture_based: `True`",
        "- real_literature_acquisition_required: `True`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
