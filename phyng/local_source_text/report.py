"""Reports for PHI_GRADIENT local source text registry v3.6."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.local_source_text.schemas import PhiGradientLocalSourceTextRegistryCampaignResult


def write_local_source_text_reports(
    result: PhiGradientLocalSourceTextRegistryCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "local_source_text"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "registry": report_dir / "phi_gradient_local_source_registry_v3_6.md",
        "file_manifest": report_dir / "phi_gradient_source_file_manifest_v3_6.md",
        "hashes": report_dir / "phi_gradient_source_hashes_v3_6.md",
        "availability": report_dir / "phi_gradient_source_availability_v3_6.md",
        "manual_download_tasks": report_dir / "phi_gradient_manual_download_tasks_v3_6.md",
        "next_exact_extraction": report_dir / "phi_gradient_next_exact_extraction_v3_6.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6.md",
    }
    renderers = {
        "registry": _render_registry,
        "file_manifest": _render_file_manifest,
        "hashes": _render_hashes,
        "availability": _render_availability,
        "manual_download_tasks": _render_download_tasks,
        "next_exact_extraction": _render_next_extraction,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: PhiGradientLocalSourceTextRegistryCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    registry_result = result.registry_result
    contract = build_report_contract(
        title="PHI_GRADIENT Local Source Text Registry v3.6",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="local_source_text",
        reports_generated=reports_generated or [],
        next_actions=registry_result.next_actions,
        discipline_note="A source becomes machine-reviewable only when its text is locally registered and hashable.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_registry(result: PhiGradientLocalSourceTextRegistryCampaignResult) -> str:
    gate = result.registry_result
    return "\n".join(
        [
            "# PHI_GRADIENT Local Source Registry v3.6",
            "",
            f"- status: `{gate.status}`",
            f"- priority_source_count: `{len(gate.priority_sources)}`",
            f"- available_file_count: `{gate.available_file_count}`",
            f"- missing_file_count: `{gate.missing_file_count}`",
            f"- hash_count: `{gate.hash_count}`",
            f"- unsupported_file_count: `{gate.unsupported_file_count}`",
            f"- manual_download_task_count: `{gate.manual_download_task_count}`",
            "",
            "## Source ID to Path Mapping",
            "",
            *_or_none([f"- `{record.source_id}` -> `{record.local_path}`" for record in gate.registry.source_records]),
            "",
            "## Blocked Claims",
            "",
            *[f"- {claim}" for claim in gate.blocked_claims],
        ]
    ) + "\n"


def _render_file_manifest(result: PhiGradientLocalSourceTextRegistryCampaignResult) -> str:
    records = result.registry_result.file_manifest.source_files
    return "\n".join(
        [
            "# PHI_GRADIENT Source File Manifest v3.6",
            "",
            *_or_none(
                [
                    f"- `{record.source_id}`: exists=`{record.exists}`, type=`{record.file_type}`, size=`{record.size_bytes}`"
                    for record in records
                ]
            ),
        ]
    ) + "\n"


def _render_hashes(result: PhiGradientLocalSourceTextRegistryCampaignResult) -> str:
    hashes = result.registry_result.hash_manifest.hashes
    return "\n".join(
        [
            "# PHI_GRADIENT Source Hashes v3.6",
            "",
            f"- hash_count: `{len(hashes)}`",
            "",
            "## Source ID to SHA256 Mapping",
            "",
            *_or_none([f"- `{item.source_id}` -> `{item.sha256}`" for item in hashes]),
        ]
    ) + "\n"


def _render_availability(result: PhiGradientLocalSourceTextRegistryCampaignResult) -> str:
    availability = result.registry_result.availability_manifest.availability
    return "\n".join(
        [
            "# PHI_GRADIENT Source Availability v3.6",
            "",
            f"- available_file_count: `{result.registry_result.available_file_count}`",
            f"- missing_file_count: `{result.registry_result.missing_file_count}`",
            "",
            *_or_none([f"- `{item.source_id}`: `{item.availability_status}`" for item in availability]),
        ]
    ) + "\n"


def _render_download_tasks(result: PhiGradientLocalSourceTextRegistryCampaignResult) -> str:
    tasks = result.registry_result.download_tasks.tasks
    return "\n".join(
        [
            "# PHI_GRADIENT Manual Download Tasks v3.6",
            "",
            f"- manual_download_task_count: `{len(tasks)}`",
            "",
            *_or_none(
                [
                    f"- `{task.task_id}`: `{task.source_id}` -> `{task.target_path}`, status=`{task.status}`"
                    for task in tasks
                ]
            ),
        ]
    ) + "\n"


def _render_next_extraction(result: PhiGradientLocalSourceTextRegistryCampaignResult) -> str:
    gate = result.registry_result
    readiness = "FULL_LOCAL_SOURCE_TEXT_READY" if gate.status == "PHI_GRADIENT_LOCAL_SOURCE_FILES_READY" else "PARTIAL_LOCAL_SOURCE_TEXT_READY" if gate.available_file_count else "LOCAL_SOURCE_TEXT_NOT_READY"
    return "\n".join(
        [
            "# PHI_GRADIENT Next Exact Extraction v3.6",
            "",
            f"- status: `{gate.status}`",
            f"- next_extraction_readiness: `{readiness}`",
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


def _render_campaign(result: PhiGradientLocalSourceTextRegistryCampaignResult) -> str:
    gate = result.registry_result
    return "\n".join(
        [
            "# Campaign Report - PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6",
            "",
            f"- campaign_id: `{result.campaign_id}`",
            f"- status: `{result.status}`",
            f"- available_file_count: `{gate.available_file_count}`",
            f"- missing_file_count: `{gate.missing_file_count}`",
            f"- hash_count: `{gate.hash_count}`",
            f"- manual_download_task_count: `{gate.manual_download_task_count}`",
            "",
            "## Reports Generated",
            "",
            *[f"- `{path}`" for path in result.report_paths.values()],
        ]
    ) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
