"""Reports for v5.7 dataset expansion."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.dataset_expansion.schemas import DatasetExpansionCampaignResult


def write_dataset_expansion_reports(result: DatasetExpansionCampaignResult, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    report_dir = root / "frontera_c" / "dataset_expansion"
    campaign_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "source_pool": report_dir / "visibility_decoherence_source_pool_v5_7.md",
        "locations": report_dir / "visibility_decoherence_observable_location_candidates_v5_7.md",
        "ytrue_candidates": report_dir / "visibility_decoherence_ytrue_candidates_v5_7.md",
        "accepted_ytrue": report_dir / "visibility_decoherence_accepted_ytrue_v5_7.md",
        "rejected_ytrue": report_dir / "visibility_decoherence_rejected_ytrue_v5_7.md",
        "quality": report_dir / "visibility_decoherence_dataset_quality_v5_7.md",
        "readiness": report_dir / "visibility_decoherence_benchmark_readiness_v5_7.md",
        "campaign": campaign_dir / "FRONTERA-C-VISIBILITY-DECOHERENCE-DATASET-EXPANSION-v5_7.md",
    }
    renderers = {
        "source_pool": _render_source_pool,
        "locations": _render_locations,
        "ytrue_candidates": _render_ytrue_candidates,
        "accepted_ytrue": _render_accepted,
        "rejected_ytrue": _render_rejected,
        "quality": _render_quality,
        "readiness": _render_readiness,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    result.report_paths = {key: str(path) for key, path in paths.items()}
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(result.report_paths.values())), encoding="utf-8")
    return result.report_paths


def _canonical(markdown: str, result: DatasetExpansionCampaignResult, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="Visibility/Decoherence Dataset Expansion v5.7",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="visibility_decoherence_dataset_expansion",
        reports_generated=reports_generated or [],
        next_actions=["Continue targeted visibility/decoherence y_true expansion."],
        discipline_note="No more single-source smoke-test authority. Build the benchmark field before judging candidates again.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_source_pool(result: DatasetExpansionCampaignResult) -> str:
    lines = ["# Visibility/Decoherence Source Pool v5.7", "", f"- source_count: `{len(result.source_pool)}`", ""]
    for record in result.source_pool:
        lines.append(f"- `{record.source_id}`: status=`{record.source_status}`, hash=`{bool(record.local_pdf_hash)}`")
    return "\n".join(lines) + "\n"


def _render_locations(result: DatasetExpansionCampaignResult) -> str:
    lines = ["# Observable Location Candidates v5.7", "", f"- location_count: `{len(result.location_candidates)}`", ""]
    for record in result.location_candidates:
        lines.append(f"- `{record.location_id}`: class=`{record.observable_class}`, classification=`{record.classification}`")
    return "\n".join(lines) + "\n"


def _render_ytrue_candidates(result: DatasetExpansionCampaignResult) -> str:
    return "\n".join(
        [
            "# y_true Candidates v5.7",
            "",
            f"- candidate_count: `{len(result.ytrue_candidates)}`",
            f"- accepted_count: `{len(result.accepted_ytrue)}`",
            f"- rejected_count: `{len(result.rejected_ytrue)}`",
        ]
    ) + "\n"


def _render_accepted(result: DatasetExpansionCampaignResult) -> str:
    lines = ["# Accepted y_true v5.7", "", f"- accepted_ytrue_count: `{len(result.accepted_ytrue)}`", ""]
    for record in result.accepted_ytrue:
        lines.append(f"- `{record.ytrue_candidate_id}`: {record.conditions} -> `{record.value_numeric}` `{record.unit}`")
    return "\n".join(lines) + "\n"


def _render_rejected(result: DatasetExpansionCampaignResult) -> str:
    lines = ["# Rejected y_true v5.7", "", f"- rejected_ytrue_count: `{len(result.rejected_ytrue)}`", ""]
    for record in result.rejected_ytrue:
        lines.append(f"- `{record.ytrue_candidate_id}`: qc=`{record.qc_status}`, limitations={record.limitations}")
    return "\n".join(lines) + "\n"


def _render_quality(result: DatasetExpansionCampaignResult) -> str:
    q = result.dataset_quality
    return "\n".join(
        [
            "# Dataset Quality v5.7",
            "",
            f"- accepted_ytrue_count_total: `{q.get('accepted_ytrue_count_total')}`",
            f"- independent_source_count: `{q.get('independent_source_count')}`",
            f"- log_boundary_remains_archived: `{q.get('log_boundary_remains_archived')}`",
            f"- frontera_c_validated: `{q.get('frontera_c_validated')}`",
        ]
    ) + "\n"


def _render_readiness(result: DatasetExpansionCampaignResult) -> str:
    r = result.benchmark_readiness
    return "\n".join(
        [
            "# Benchmark Readiness v5.7",
            "",
            f"- readiness: `{r.get('readiness')}`",
            f"- accepted_ytrue_count_total: `{r.get('accepted_ytrue_count_total')}`",
            f"- independent_source_count: `{r.get('independent_source_count')}`",
            f"- out_of_source_split_possible: `{r.get('out_of_source_split_possible')}`",
            f"- allowed_next_phase: `{r.get('allowed_next_phase')}`",
        ]
    ) + "\n"


def _render_campaign(result: DatasetExpansionCampaignResult) -> str:
    return "\n".join(
        [
            "# Campaign Report - FRONTERA-C-VISIBILITY-DECOHERENCE-DATASET-EXPANSION-v5_7",
            "",
            f"- status: `{result.status}`",
            f"- inputs_loaded: `{result.inputs_loaded}`",
            f"- accepted_ytrue_count_total: `{len(result.accepted_ytrue)}`",
            f"- independent_source_count: `{result.dataset.source_count if result.dataset else 0}`",
            f"- physical_claim_created: `{result.dataset_quality.get('physical_claim_created')}`",
            f"- frontera_c_validated: `{result.dataset_quality.get('frontera_c_validated')}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"
