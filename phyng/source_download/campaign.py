"""Campaign helpers for v5.7.2 source download outputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.source_download.manifest import build_source_download_records
from phyng.source_download.reports import write_source_download_reports
from phyng.source_download.schemas import SourceDownloadCampaignResult


def run_source_download_campaign(root: str | Path = ".") -> SourceDownloadCampaignResult:
    repo_root = Path(root)
    manifest, hashes, failures = build_source_download_records(repo_root)
    verified_count = sum(1 for item in manifest if item.file_verified)
    status = "TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_COMPLETED" if verified_count else "TARGETED_SOURCE_DOWNLOAD_BLOCKED_NO_LOCAL_SOURCES"
    result = SourceDownloadCampaignResult(status=status, manifest_records=manifest, hash_records=hashes, failure_records=failures)
    result.output_paths = write_source_download_outputs(repo_root, result)
    result.report_paths = write_source_download_reports(result, repo_root / "reports")
    return result


def write_source_download_outputs(root: Path, result: SourceDownloadCampaignResult) -> dict[str, str]:
    base = root / "data" / "frontera_c" / "source_download"
    base.mkdir(parents=True, exist_ok=True)
    paths = {
        "manifest": base / "source_download_manifest_v5_7_2.json",
        "hashes": base / "source_hash_registry_update_v5_7_2.json",
        "failures": base / "source_download_failures_v5_7_2.json",
    }
    payloads = {
        "manifest": {
            "source_count": len(result.manifest_records),
            "verified_source_object_count": sum(1 for item in result.manifest_records if item.file_verified),
            "records": [item.model_dump() for item in result.manifest_records],
        },
        "hashes": {
            "hash_count": sum(1 for item in result.hash_records if item.sha256),
            "records": [item.model_dump() for item in result.hash_records],
        },
        "failures": {
            "failure_count": len(result.failure_records),
            "records": [item.model_dump() for item in result.failure_records],
        },
    }
    for key, path in paths.items():
        path.write_text(json.dumps(payloads[key], indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}
