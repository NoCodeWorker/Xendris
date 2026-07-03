"""Campaign orchestration for v5.7.2 observable-location review."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.observable_location.observed_measurement_candidates import build_observable_location_records
from phyng.observable_location.reports import write_observable_location_reports
from phyng.observable_location.schemas import ObservableLocationCampaignResult


def run_observable_location_campaign(root: str | Path = ".") -> ObservableLocationCampaignResult:
    repo_root = Path(root)
    candidates, observed, rejected = build_observable_location_records(repo_root)
    manifest_path = repo_root / "data/frontera_c/source_download/source_download_manifest_v5_7_2.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"verified_source_object_count": 0}
    verified_count = int(manifest.get("verified_source_object_count", 0))
    human_review_count = sum(1 for item in observed if "REQUIRES_HUMAN_FIGURE_REVIEW" in item.extraction_blockers)
    supplementary_count = sum(1 for item in candidates if item.classification == "SUPPLEMENTARY_POINTER")
    if verified_count == 0:
        status = "TARGETED_SOURCE_DOWNLOAD_BLOCKED_NO_LOCAL_SOURCES"
        allowed_next_phase = None
        rationale = "No verified local source objects exist; observable review is blocked."
    elif observed:
        status = "TARGETED_SOURCE_DOWNLOAD_PARTIAL_OBSERVABLE_LOCATION_FOUND"
        allowed_next_phase = "v5.7.3 - Targeted y_true Extraction"
        rationale = "At least one observed measurement candidate was source-located; strict y_true extraction review may proceed."
    elif human_review_count:
        status = "TARGETED_SOURCE_DOWNLOAD_REQUIRES_HUMAN_FIGURE_REVIEW"
        allowed_next_phase = None
        rationale = "Observable candidates require human figure/table review before y_true extraction."
    elif supplementary_count:
        status = "TARGETED_OBSERVABLE_LOCATION_REQUIRES_SUPPLEMENTARY_DATA"
        allowed_next_phase = None
        rationale = "Observable review points to supplementary data only."
    else:
        status = "TARGETED_OBSERVABLE_LOCATION_BLOCKED_NO_OBSERVED_MEASUREMENTS"
        allowed_next_phase = None
        rationale = "Verified source objects were scanned but no observed measurement candidate was found."
    next_gate = {
        "final_status": status,
        "downloaded_source_count": verified_count,
        "verified_source_object_count": verified_count,
        "candidate_location_count": len(candidates),
        "observed_measurement_candidate_count": len(observed),
        "human_figure_review_required_count": human_review_count,
        "supplementary_required_count": supplementary_count,
        "allowed_next_phase": allowed_next_phase,
        "blocked_next_phases": ["PredictiveGain computation", "Frontera C validation", "physical claim"],
        "rationale": rationale,
        "no_ytrue_extracted": True,
        "no_predictive_gain_computed": True,
        "frontera_c_validated": False,
        "physical_claim_created": False,
    }
    result = ObservableLocationCampaignResult(
        status=status,
        location_candidates=candidates,
        observed_measurement_candidates=observed,
        rejected_location_records=rejected,
        next_gate_decision=next_gate,
    )
    result.output_paths = write_observable_location_outputs(repo_root, result)
    result.report_paths = write_observable_location_reports(result, repo_root / "reports")
    return result


def write_observable_location_outputs(root: Path, result: ObservableLocationCampaignResult) -> dict[str, str]:
    base = root / "data" / "frontera_c" / "observable_location"
    base.mkdir(parents=True, exist_ok=True)
    paths = {
        "candidates": base / "targeted_observable_location_candidates_v5_7_2.json",
        "observed": base / "targeted_observed_measurement_candidates_v5_7_2.json",
        "rejected": base / "targeted_rejected_location_records_v5_7_2.json",
        "next_gate": base / "v5_7_2_next_gate_decision.json",
    }
    payloads = {
        "candidates": {"candidate_location_count": len(result.location_candidates), "records": [item.model_dump() for item in result.location_candidates]},
        "observed": {"observed_measurement_candidate_count": len(result.observed_measurement_candidates), "records": [item.model_dump() for item in result.observed_measurement_candidates]},
        "rejected": {"rejected_location_count": len(result.rejected_location_records), "records": [item.model_dump() for item in result.rejected_location_records]},
        "next_gate": result.next_gate_decision,
    }
    for key, path in paths.items():
        path.write_text(json.dumps(payloads[key], indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}
