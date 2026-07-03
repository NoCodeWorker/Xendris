"""Reports for PHI_GRADIENT v3.0 real source acquisition."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.real_source_acquisition.schemas import PhiGradientRealSourceAcquisitionCampaignResult


def write_phi_gradient_real_source_acquisition_reports(
    result: PhiGradientRealSourceAcquisitionCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "real_source_acquisition"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "query_plan": report_dir / "phi_gradient_query_plan_v3_0.md",
        "candidate_manifest": report_dir / "phi_gradient_source_candidate_manifest_v3_0.md",
        "extract_validation": report_dir / "phi_gradient_extract_validation_v3_0.md",
        "slot_coverage": report_dir / "phi_gradient_slot_coverage_v3_0.md",
        "negative_sources": report_dir / "phi_gradient_negative_sources_v3_0.md",
        "benchmark_comparability": report_dir / "phi_gradient_benchmark_comparability_v3_0.md",
        "real_source_gate": report_dir / "phi_gradient_real_source_gate_v3_0.md",
        "loop_feedback": report_dir / "phi_gradient_loop_feedback_v3_0.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-REAL-SOURCE-ACQUISITION-v3_0.md",
    }
    paths["query_plan"].write_text(_canonical(_render_query_plan(result), result), encoding="utf-8")
    paths["candidate_manifest"].write_text(_canonical(_render_manifest(result), result), encoding="utf-8")
    paths["extract_validation"].write_text(_canonical(_render_extracts(result), result), encoding="utf-8")
    paths["slot_coverage"].write_text(_canonical(_render_slot_coverage(result), result), encoding="utf-8")
    paths["negative_sources"].write_text(_canonical(_render_negative_sources(result), result), encoding="utf-8")
    paths["benchmark_comparability"].write_text(_canonical(_render_benchmark(result), result), encoding="utf-8")
    paths["real_source_gate"].write_text(_canonical(_render_gate(result), result), encoding="utf-8")
    paths["loop_feedback"].write_text(_canonical(_render_loop(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: PhiGradientRealSourceAcquisitionCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    acquisition = result.acquisition_result
    contract = build_report_contract(
        title="PHI_GRADIENT Real Source Acquisition v3.0",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="real_source_acquisition",
        reports_generated=reports_generated or [],
        next_actions=acquisition.next_actions,
        discipline_note="A query plan is a map. A source extract is pressure. Only validated pressure can affect candidate priority.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_query_plan(result: PhiGradientRealSourceAcquisitionCampaignResult) -> str:
    plan = result.acquisition_result.query_plan
    queries = [*plan.slot_queries, *plan.negative_queries]
    return "\n".join([
        "# PHI_GRADIENT Query Plan v3.0",
        "",
        f"- campaign_id: `{plan.campaign_id}`",
        f"- target_candidate: `{plan.target_candidate}`",
        f"- backend_status: `{result.acquisition_result.backend_status}`",
        f"- actual_real_sources_acquired: `{result.acquisition_result.actual_real_sources_acquired}`",
        "",
        "## Slot Queries",
        "",
        *[f"- `{query.slot_id}`: {query.query_text}" for query in queries],
        "",
        "## Inclusion Rules",
        "",
        *[f"- {rule}" for rule in plan.inclusion_rules],
        "",
        "## Exclusion Rules",
        "",
        *[f"- {rule}" for rule in plan.exclusion_rules],
    ]) + "\n"


def _render_manifest(result: PhiGradientRealSourceAcquisitionCampaignResult) -> str:
    manifest = result.acquisition_result.candidate_manifest
    return "\n".join([
        "# PHI_GRADIENT Source Candidate Manifest v3.0",
        "",
        f"- backend_status: `{manifest.backend_status}`",
        f"- actual_real_sources_acquired: `{manifest.actual_real_sources_acquired}`",
        "",
        "## Candidates",
        "",
        *_or_none([
            f"- `{candidate.source_id}`: `{candidate.acquisition_status}`, support=`{candidate.is_support}`, slots=`{', '.join(candidate.targeted_slots)}`"
            for candidate in manifest.candidates
        ]),
        "",
        "## Notes",
        "",
        *[f"- {note}" for note in manifest.notes],
    ]) + "\n"


def _render_extracts(result: PhiGradientRealSourceAcquisitionCampaignResult) -> str:
    acquisition = result.acquisition_result
    return "\n".join([
        "# PHI_GRADIENT Extract Validation v3.0",
        "",
        f"- backend_status: `{acquisition.backend_status}`",
        f"- actual_real_extracts_validated: `{acquisition.actual_real_extracts_validated}`",
        "",
        "## Results",
        "",
        *_or_none([
            f"- `{ingestion.source_id}`: `{ingestion.status}`, attempted=`{ingestion.attempted}`"
            for ingestion in acquisition.ingestion_results
        ]),
    ]) + "\n"


def _render_slot_coverage(result: PhiGradientRealSourceAcquisitionCampaignResult) -> str:
    coverage = result.acquisition_result.slot_coverage
    return "\n".join([
        "# PHI_GRADIENT Slot Coverage v3.0",
        "",
        f"- backend_status: `{result.acquisition_result.backend_status}`",
        f"- actual_real_sources_acquired: `{result.acquisition_result.actual_real_sources_acquired}`",
        "",
        "## Coverage",
        "",
        *[
            f"- `{record.slot_id}`: `{record.coverage_status}`, accepted=`{record.accepted_support_count}`, missing=`{', '.join(record.missing_requirements)}`"
            for record in coverage.records
        ],
        "",
        "## Missing Requirements",
        "",
        *[f"- `{slot_id}`" for slot_id in coverage.missing_slots],
    ]) + "\n"


def _render_negative_sources(result: PhiGradientRealSourceAcquisitionCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Negative Sources v3.0",
        "",
        f"- backend_status: `{result.acquisition_result.backend_status}`",
        "",
        "## Negative Records",
        "",
        *_or_none([
            f"- `{record.source_id}` contradicts `{record.contradicted_component}` in `{record.slot_id}`"
            for record in result.acquisition_result.negative_sources
        ]),
    ]) + "\n"


def _render_benchmark(result: PhiGradientRealSourceAcquisitionCampaignResult) -> str:
    benchmark = result.acquisition_result.benchmark_comparability
    return "\n".join([
        "# PHI_GRADIENT Benchmark Comparability v3.0",
        "",
        f"- status: `{benchmark.status}`",
        f"- comparable_records: `{benchmark.comparable_records}`",
        f"- backend_status: `{result.acquisition_result.backend_status}`",
        f"- actual_real_sources_acquired: `{result.acquisition_result.actual_real_sources_acquired}`",
        "",
        "## Missing Requirements",
        "",
        *_or_none([f"- {item}" for item in benchmark.missing_requirements]),
    ]) + "\n"


def _render_gate(result: PhiGradientRealSourceAcquisitionCampaignResult) -> str:
    acquisition = result.acquisition_result
    return "\n".join([
        "# PHI_GRADIENT Real Source Gate v3.0",
        "",
        f"- status: `{acquisition.status}`",
        f"- backend_status: `{acquisition.backend_status}`",
        f"- actual_real_sources_acquired: `{acquisition.actual_real_sources_acquired}`",
        f"- actual_real_extracts_validated: `{acquisition.actual_real_extracts_validated}`",
        "",
        "## Allowed Claims",
        "",
        *[f"- {claim}" for claim in acquisition.allowed_claims],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in acquisition.blocked_claims],
        "",
        "## Next Actions",
        "",
        *[f"- {action}" for action in acquisition.next_actions],
    ]) + "\n"


def _render_loop(result: PhiGradientRealSourceAcquisitionCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Loop Feedback v3.0",
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
        *[f"- {claim}" for claim in result.acquisition_result.blocked_claims],
    ]) + "\n"


def _render_campaign(result: PhiGradientRealSourceAcquisitionCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-REAL-SOURCE-ACQUISITION-v3_0",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- backend_status: `{result.acquisition_result.backend_status}`",
        f"- actual_real_sources_acquired: `{result.acquisition_result.actual_real_sources_acquired}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
