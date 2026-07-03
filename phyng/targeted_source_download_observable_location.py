"""Combined reporting for v5.7.2 targeted source download and observable-location review."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.observable_location.schemas import TargetedObservableLocationCandidate
from phyng.source_download.schemas import (
    SourceDownloadFailureRecord,
    SourceDownloadManifestRecord,
    SourceHashRegistryUpdateRecord,
)


class TargetedSourceDownloadObservableLocationCampaignResult(BaseModel):
    campaign_id: str = "FRONTERA-C-TARGETED-SOURCE-DOWNLOAD-OBSERVABLE-LOCATION-v5_7_2"
    status: str
    source_download_status: str
    observable_location_status: str
    source_manifest_records: list[SourceDownloadManifestRecord] = Field(default_factory=list)
    hash_records: list[SourceHashRegistryUpdateRecord] = Field(default_factory=list)
    failure_records: list[SourceDownloadFailureRecord] = Field(default_factory=list)
    location_candidates: list[TargetedObservableLocationCandidate] = Field(default_factory=list)
    observed_measurement_candidates: list[TargetedObservableLocationCandidate] = Field(default_factory=list)
    rejected_location_records: list[TargetedObservableLocationCandidate] = Field(default_factory=list)
    next_gate_decision: dict = Field(default_factory=dict)
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)

    @property
    def verified_source_object_count(self) -> int:
        return sum(1 for item in self.source_manifest_records if item.file_verified)

    @property
    def hash_count(self) -> int:
        return sum(1 for item in self.hash_records if item.sha256)


def write_combined_campaign_report(root: Path, result: TargetedSourceDownloadObservableLocationCampaignResult) -> str:
    path = root / "reports" / "campaigns" / "FRONTERA-C-TARGETED-SOURCE-DOWNLOAD-OBSERVABLE-LOCATION-v5_7_2.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    markdown = "\n".join(
        [
            "# Campaign Report - FRONTERA-C-TARGETED-SOURCE-DOWNLOAD-OBSERVABLE-LOCATION-v5_7_2",
            "",
            f"- status: `{result.status}`",
            f"- source_download_status: `{result.source_download_status}`",
            f"- observable_location_status: `{result.observable_location_status}`",
            f"- source_count: `{len(result.source_manifest_records)}`",
            f"- verified_source_object_count: `{result.verified_source_object_count}`",
            f"- hash_count: `{result.hash_count}`",
            f"- failure_count: `{len(result.failure_records)}`",
            f"- candidate_location_count: `{len(result.location_candidates)}`",
            f"- observed_measurement_candidate_count: `{len(result.observed_measurement_candidates)}`",
            f"- allowed_next_phase: `{result.next_gate_decision.get('allowed_next_phase')}`",
            f"- no_ytrue_extracted: `{result.next_gate_decision.get('no_ytrue_extracted')}`",
            f"- no_predictive_gain_computed: `{result.next_gate_decision.get('no_predictive_gain_computed')}`",
            "",
            "## Blocked Claims",
            "",
            "- Frontera C is validated.",
            "- LOG_BOUNDARY is reactivated.",
            "- Downloaded sources are evidence.",
            "- Observable location equals y_true.",
            "- Source support equals PredictiveGain.",
            "- Physical claim.",
            "- Invariant confirmation.",
        ]
    ) + "\n"
    path.write_text(_canonical(markdown, result), encoding="utf-8")
    return path.relative_to(root).as_posix()


def write_final_result_doc(root: Path, result: TargetedSourceDownloadObservableLocationCampaignResult) -> str:
    path = root / "docs" / "350_PHYGN_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_RESULTS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    missing = [item.expected_filename for item in result.source_manifest_records if not item.file_verified]
    lines = [
        "# Phygn v5.7.2 - Targeted Source Download & Observable Location Review Results",
        "",
        "Date: 2026-07-02",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/349_PHYGN_CODEX_V5_7_2_TARGETED_SOURCE_DOWNLOAD_OBSERVABLE_LOCATION_PROMPT.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{result.status}`",
        f"Verified source objects: `{result.verified_source_object_count}`",
        f"SHA256 hashes generated: `{result.hash_count}`",
        f"Download failures: `{len(result.failure_records)}`",
        f"Observable location candidates: `{len(result.location_candidates)}`",
        f"Observed measurement candidates: `{len(result.observed_measurement_candidates)}`",
        f"Allowed next phase: `{result.next_gate_decision.get('allowed_next_phase')}`",
        "",
        "No y_true was extracted. No PredictiveGain was computed. No benchmark was built. No Frontera C or physical claim was upgraded.",
        "",
        "## Missing or Unverified Source Objects",
        "",
        *([f"- `{name}`" for name in missing] if missing else ["- None"]),
        "",
        "## Created Artifacts",
        "",
        *[f"- `{path_value}`" for path_value in result.output_paths.values()],
        *[f"- `{path_value}`" for path_value in result.report_paths.values()],
        "",
        "## Next Gate",
        "",
        "```txt",
        str(result.next_gate_decision.get("allowed_next_phase")),
        "```",
        "",
        "## Blocked Claims",
        "",
        "- Frontera C is validated.",
        "- LOG_BOUNDARY is reactivated.",
        "- Downloaded sources are evidence.",
        "- Observable location equals y_true.",
        "- Source support equals PredictiveGain.",
        "- Physical claim.",
        "- Invariant confirmation.",
        "",
        "## Allowed Claims",
        "",
        "- Source objects were checked and hashed when verified.",
        "- Missing or invalid source objects were reported.",
        "- Observable location candidates were scanned from verified source objects.",
        "- v5.7.3 is permitted only if observed measurement candidates exist.",
        "",
        "Final discipline:",
        "",
        "```txt",
        "No source object, no observable review.",
        "No observable location, no y_true.",
        "```",
    ]
    path.write_text(_canonical("\n".join(lines) + "\n", result), encoding="utf-8")
    return path.relative_to(root).as_posix()


def _canonical(markdown: str, result: TargetedSourceDownloadObservableLocationCampaignResult) -> str:
    contract = build_report_contract(
        title="Targeted Source Download & Observable Location Review v5.7.2",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="targeted_source_download_observable_location",
        reports_generated=list(result.report_paths.values()),
        next_actions=[result.next_gate_decision.get("allowed_next_phase") or "Resolve source or observable-location blockers."],
        discipline_note="No source object, no observable review. No observable location, no y_true.",
    )
    return append_canonical_status_section(markdown, contract)
