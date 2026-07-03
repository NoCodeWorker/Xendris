"""Reports for PHI_GRADIENT source-pack population v3.2."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.source_pack_population.schemas import PhiGradientSourcePackPopulationCampaignResult


def write_source_pack_population_reports(
    result: PhiGradientSourcePackPopulationCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "source_pack_population"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "manifest": report_dir / "phi_gradient_source_pack_manifest_v3_2.md",
        "extracts": report_dir / "phi_gradient_source_pack_extracts_v3_2.md",
        "slot_targets": report_dir / "phi_gradient_source_pack_slot_targets_v3_2.md",
        "risk_flags": report_dir / "phi_gradient_source_pack_risk_flags_v3_2.md",
        "next_gate": report_dir / "phi_gradient_source_pack_next_gate_v3_2.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-REVIEWED-REAL-SOURCE-PACK-v3_2.md",
    }
    renderers = {
        "manifest": _render_manifest,
        "extracts": _render_extracts,
        "slot_targets": _render_slot_targets,
        "risk_flags": _render_risk_flags,
        "next_gate": _render_next_gate,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(markdown: str, result: PhiGradientSourcePackPopulationCampaignResult, reports_generated: list[str] | None = None) -> str:
    population = result.population_result
    contract = build_report_contract(
        title="PHI_GRADIENT Reviewed Real Source Pack v3.2",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="source_pack_population",
        reports_generated=reports_generated or [],
        next_actions=population.next_actions,
        discipline_note="A source pack can only become positive by surviving validation. Until then, it is organized pressure waiting to happen.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_manifest(result: PhiGradientSourcePackPopulationCampaignResult) -> str:
    population = result.population_result
    manifest = population.manifest
    validation = population.validation
    return "\n".join([
        "# PHI_GRADIENT Source Pack Manifest v3.2",
        "",
        f"- manifest_path: `{population.manifest_path}`",
        f"- manifest_entry_count: `{validation.manifest_entry_count}`",
        f"- traceable_identifier_coverage: `{validation.traceable_entry_count}/{validation.manifest_entry_count}`",
        "",
        "## Entries",
        "",
        *[
            f"- `{entry.source_id}`: {entry.title}; evidence_status=`{entry.evidence_status}`; slots=`{', '.join(entry.target_slots)}`"
            for entry in manifest.entries
        ],
    ]) + "\n"


def _render_extracts(result: PhiGradientSourcePackPopulationCampaignResult) -> str:
    population = result.population_result
    pack = population.extract_pack
    validation = population.validation
    return "\n".join([
        "# PHI_GRADIENT Source Pack Extracts v3.2",
        "",
        f"- extract_pack_path: `{population.extract_pack_path}`",
        f"- extract_count: `{validation.extract_count}`",
        f"- manual_review_extract_count: `{validation.manual_review_extract_count}`",
        "",
        "## Extract Candidates",
        "",
        *[
            f"- `{extract.extract_id}`: `{extract.source_id}` -> `{extract.slot_id}`, initial_validation_status=`{extract.initial_validation_status}`, manual_review_required=`{extract.manual_review_required}`"
            for extract in pack.extracts
        ],
    ]) + "\n"


def _render_slot_targets(result: PhiGradientSourcePackPopulationCampaignResult) -> str:
    entries = result.population_result.manifest.entries
    slots = sorted({slot for entry in entries for slot in entry.target_slots})
    return "\n".join([
        "# PHI_GRADIENT Source Pack Slot Targets v3.2",
        "",
        *[
            f"- `{slot}`: `{sum(1 for entry in entries if slot in entry.target_slots)}` candidate sources"
            for slot in slots
        ],
    ]) + "\n"


def _render_risk_flags(result: PhiGradientSourcePackPopulationCampaignResult) -> str:
    entries = result.population_result.manifest.entries
    flags = sorted({flag for entry in entries for flag in entry.risk_flags})
    return "\n".join([
        "# PHI_GRADIENT Source Pack Risk Flags v3.2",
        "",
        *[
            f"- `{flag}`: `{sum(1 for entry in entries if flag in entry.risk_flags)}` sources"
            for flag in flags
        ],
        "",
        "## Negative Source Candidates",
        "",
        *[
            f"- `{entry.source_id}`"
            for entry in entries
            if "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES" in entry.target_slots
        ],
        "",
        "## Benchmark Candidate Sources",
        "",
        *[
            f"- `{entry.source_id}`"
            for entry in entries
            if "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS" in entry.target_slots
        ],
    ]) + "\n"


def _render_next_gate(result: PhiGradientSourcePackPopulationCampaignResult) -> str:
    population = result.population_result
    return "\n".join([
        "# PHI_GRADIENT Source Pack Next Gate v3.2",
        "",
        f"- status: `{population.status}`",
        f"- validation_errors: `{len(population.validation.errors)}`",
        "",
        "## Allowed Claims",
        "",
        *[f"- {claim}" for claim in population.allowed_claims],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in population.blocked_claims],
        "",
        "## Next Actions",
        "",
        *[f"- {action}" for action in population.next_actions],
    ]) + "\n"


def _render_campaign(result: PhiGradientSourcePackPopulationCampaignResult) -> str:
    validation = result.population_result.validation
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-REVIEWED-REAL-SOURCE-PACK-v3_2",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- manifest_entry_count: `{validation.manifest_entry_count}`",
        f"- extract_count: `{validation.extract_count}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
