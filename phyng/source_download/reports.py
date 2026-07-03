"""Markdown reports for v5.7.2 source download."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.source_download.schemas import SourceDownloadCampaignResult


def write_source_download_reports(result: SourceDownloadCampaignResult, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    report_dir = root / "frontera_c" / "source_download"
    report_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "manifest": report_dir / "source_download_manifest_v5_7_2.md",
        "hashes": report_dir / "source_hash_registry_update_v5_7_2.md",
        "failures": report_dir / "source_download_failures_v5_7_2.md",
    }
    paths["manifest"].write_text(_canonical(_render_manifest(result), result), encoding="utf-8")
    paths["hashes"].write_text(_canonical(_render_hashes(result), result), encoding="utf-8")
    paths["failures"].write_text(_canonical(_render_failures(result), result), encoding="utf-8")
    return {key: str(path) for key, path in paths.items()}


def _canonical(markdown: str, result: SourceDownloadCampaignResult) -> str:
    contract = build_report_contract(
        title="Targeted Source Download v5.7.2",
        campaign_id="FRONTERA-C-TARGETED-SOURCE-DOWNLOAD-OBSERVABLE-LOCATION-v5_7_2",
        domain_status=result.status,
        domain="targeted_source_download_observable_location",
        next_actions=["Run observable-location review only for verified source objects."],
        discipline_note="A downloaded source is not y_true.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_manifest(result: SourceDownloadCampaignResult) -> str:
    lines = ["# Source Download Manifest v5.7.2", "", f"- source_count: `{len(result.manifest_records)}`", f"- verified_source_object_count: `{sum(1 for item in result.manifest_records if item.file_verified)}`", ""]
    for item in result.manifest_records:
        lines.append(f"- `{item.source_candidate_id}`: status=`{item.download_status}`, verified=`{item.file_verified}`, hash=`{bool(item.local_pdf_hash)}`")
    return "\n".join(lines) + "\n"


def _render_hashes(result: SourceDownloadCampaignResult) -> str:
    lines = ["# Source Hash Registry Update v5.7.2", "", f"- hash_count: `{sum(1 for item in result.hash_records if item.sha256)}`", ""]
    for item in result.hash_records:
        lines.append(f"- `{item.source_id}`: status=`{item.hash_status}`, sha256=`{item.sha256 or 'None'}`")
    return "\n".join(lines) + "\n"


def _render_failures(result: SourceDownloadCampaignResult) -> str:
    lines = ["# Source Download Failures v5.7.2", "", f"- failure_count: `{len(result.failure_records)}`", ""]
    for item in result.failure_records:
        lines.append(f"- `{item.source_candidate_id}`: reason=`{item.reason}`, next=`{item.required_next_action}`")
    return "\n".join(lines) + "\n"
