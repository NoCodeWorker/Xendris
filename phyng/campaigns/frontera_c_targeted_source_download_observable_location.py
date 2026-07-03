"""Campaign wrapper for v5.7.2 targeted source download and observable-location review."""

from __future__ import annotations

from pathlib import Path

from phyng.observable_location.campaign import run_observable_location_campaign
from phyng.source_download.campaign import run_source_download_campaign
from phyng.targeted_source_download_observable_location import (
    TargetedSourceDownloadObservableLocationCampaignResult,
    write_combined_campaign_report,
    write_final_result_doc,
)


def run_frontera_c_targeted_source_download_observable_location_campaign(root: str | Path = ".") -> TargetedSourceDownloadObservableLocationCampaignResult:
    repo_root = Path(root)
    source_result = run_source_download_campaign(repo_root)
    observable_result = run_observable_location_campaign(repo_root)
    final_status = _final_status(source_result, observable_result)
    result = TargetedSourceDownloadObservableLocationCampaignResult(
        status=final_status,
        source_download_status=source_result.status,
        observable_location_status=observable_result.status,
        source_manifest_records=source_result.manifest_records,
        hash_records=source_result.hash_records,
        failure_records=source_result.failure_records,
        location_candidates=observable_result.location_candidates,
        observed_measurement_candidates=observable_result.observed_measurement_candidates,
        rejected_location_records=observable_result.rejected_location_records,
        next_gate_decision=observable_result.next_gate_decision,
        output_paths={**source_result.output_paths, **observable_result.output_paths},
        report_paths={**source_result.report_paths, **observable_result.report_paths},
    )
    result.report_paths["campaign"] = write_combined_campaign_report(repo_root, result)
    write_final_result_doc(repo_root, result)
    return result


def run(root: str | Path = "."):
    return run_frontera_c_targeted_source_download_observable_location_campaign(root)


def _final_status(source_result, observable_result) -> str:
    verified_count = sum(1 for item in source_result.manifest_records if item.file_verified)
    if verified_count == 0:
        if len(source_result.failure_records) == len(source_result.manifest_records):
            return "TARGETED_SOURCE_DOWNLOAD_REQUIRES_MANUAL_DOWNLOAD"
        return "TARGETED_SOURCE_DOWNLOAD_BLOCKED_NO_LOCAL_SOURCES"
    if observable_result.observed_measurement_candidates:
        return "TARGETED_SOURCE_DOWNLOAD_PARTIAL_OBSERVABLE_LOCATION_FOUND"
    return observable_result.status


if __name__ == "__main__":
    campaign_result = run_frontera_c_targeted_source_download_observable_location_campaign(root=".")
    print(
        {
            "status": campaign_result.status,
            "verified_source_object_count": campaign_result.verified_source_object_count,
            "hash_count": campaign_result.hash_count,
            "candidate_location_count": len(campaign_result.location_candidates),
            "observed_measurement_candidate_count": len(campaign_result.observed_measurement_candidates),
            "allowed_next_phase": campaign_result.next_gate_decision.get("allowed_next_phase"),
        }
    )
