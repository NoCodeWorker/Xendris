"""Reports for PHI_GRADIENT real source ingestion."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.real_source_ingestion.schemas import PhiGradientRealLiteratureCampaignResult


def write_phi_gradient_real_source_reports(
    result: PhiGradientRealLiteratureCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "real_source_ingestion"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "manifest": report_dir / "phi_gradient_real_source_manifest_v2_9.md",
        "extract_validation": report_dir / "phi_gradient_real_extract_validation_v2_9.md",
        "source_gate": report_dir / "phi_gradient_real_source_gate_v2_9.md",
        "benchmark_records": report_dir / "phi_gradient_real_benchmark_records_v2_9.md",
        "loop_feedback": report_dir / "phi_gradient_real_source_loop_feedback_v2_9.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-REAL-LITERATURE-INGESTION-v2_9.md",
    }
    paths["manifest"].write_text(_canonical(_render_manifest(result), result), encoding="utf-8")
    paths["extract_validation"].write_text(_canonical(_render_extracts(result), result), encoding="utf-8")
    paths["source_gate"].write_text(_canonical(_render_gate(result), result), encoding="utf-8")
    paths["benchmark_records"].write_text(_canonical(_render_benchmarks(result), result), encoding="utf-8")
    paths["loop_feedback"].write_text(_canonical(_render_loop(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: PhiGradientRealLiteratureCampaignResult, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="PHI_GRADIENT Real Literature Ingestion v2.9",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="real_source_ingestion",
        reports_generated=reports_generated or [],
        discipline_note="Real sources may raise pressure; Only experiments can raise physical truth.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_manifest(result: PhiGradientRealLiteratureCampaignResult) -> str:
    manifest = result.gate_result.manifest
    return "\n".join([
        "# PHI_GRADIENT Real Source Manifest v2.9",
        "",
        f"- actual_real_sources_ingested: `{manifest.actual_real_sources_ingested}`",
        f"- fixture_entries: `{', '.join(manifest.fixture_entries)}`",
        f"- test_double_entries: `{', '.join(manifest.test_double_entries)}`",
        f"- real_entries: `{', '.join(manifest.real_entries)}`",
        "",
        "## Fixture Separation",
        "",
        "- `FIXTURE_ONLY_DOES_NOT_COUNT_AS_REAL_SUPPORT`",
        "- `TEST_DOUBLE_REAL_SOURCE_FORMAT` validates ingestion shape only.",
    ]) + "\n"


def _render_extracts(result: PhiGradientRealLiteratureCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Real Extract Validation v2.9",
        "",
        *[
            f"- `{validation.extract_id}`: `{validation.status}`, counts_as_real_support=`{validation.counts_as_real_support}`"
            for validation in result.gate_result.validations
        ],
        "",
        "## Rejected Analogies",
        "",
        *[f"- `{extract_id}`" for extract_id in result.gate_result.rejected_analogy_extracts],
        "",
        "## Negative Sources",
        "",
        *[f"- `{extract_id}`" for extract_id in result.gate_result.negative_extracts],
    ]) + "\n"


def _render_gate(result: PhiGradientRealLiteratureCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# PHI_GRADIENT Real Source Gate v2.9",
        "",
        f"- status: `{gate.status}`",
        f"- actual_real_sources_ingested: `{gate.actual_real_sources_ingested}`",
        f"- accepted_real_support_extracts: `{', '.join(gate.accepted_real_support_extracts)}`",
        f"- missing_requirements: `{', '.join(gate.missing_requirements)}`",
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in gate.blocked_claims],
        "",
        "## Next Actions",
        "",
        *[f"- {action}" for action in gate.next_actions],
    ]) + "\n"


def _render_benchmarks(result: PhiGradientRealLiteratureCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Real Benchmark Records v2.9",
        "",
        *[
            f"- `{record.benchmark_id}`: comparable=`{record.comparable_to_phi_gradient}`, test_double=`{record.is_test_double}`, fixture=`{record.is_fixture}`"
            for record in result.gate_result.benchmarks
        ],
    ]) + "\n"


def _render_loop(result: PhiGradientRealLiteratureCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Real Source Loop Feedback v2.9",
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


def _render_campaign(result: PhiGradientRealLiteratureCampaignResult) -> str:
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-REAL-LITERATURE-INGESTION-v2_9",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- actual_real_sources_ingested: `{result.gate_result.actual_real_sources_ingested}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
