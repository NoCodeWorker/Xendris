"""Campaign orchestration for v5.7 visibility/decoherence dataset expansion."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.dataset_expansion.benchmark_readiness import build_benchmark_readiness
from phyng.dataset_expansion.dataset_assembly import assemble_dataset
from phyng.dataset_expansion.dataset_quality import assess_dataset_quality
from phyng.dataset_expansion.observable_location_scan import scan_observable_locations
from phyng.dataset_expansion.reports import write_dataset_expansion_reports
from phyng.dataset_expansion.schemas import DatasetExpansionCampaignResult
from phyng.dataset_expansion.source_pool import build_source_pool
from phyng.dataset_expansion.ytrue_extraction import build_ytrue_candidates, split_accepted_rejected


REQUIRED_INPUTS = [
    "docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md",
    "data/frontera_c/disposition/log_boundary_candidate_disposition_v5_6.json",
    "data/frontera_c/disposition/v5_6_next_research_direction.json",
    "data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json",
    "data/frontera_c/ytrue/log_boundary_ytrue_dataset_v5_3.json",
    "data/frontera_c/ytrue/log_boundary_ytrue_extraction_audit_trail_v5_3.json",
    "data/preflight/source_identity/source_identity_resolution_integrated_v5_1.json",
    "data/frontera_c/source_availability_matrix_v5_2.json",
    "data/real_sources/source_hashes_v3_6.json",
]


def run_frontera_c_visibility_decoherence_dataset_expansion_campaign(root: str | Path = ".") -> DatasetExpansionCampaignResult:
    repo_root = Path(root)
    missing = [path for path in REQUIRED_INPUTS if not (repo_root / path).exists()]
    if missing:
        result = DatasetExpansionCampaignResult(
            status="FRONTERA_C_REQUIRES_DATASET_EXPANSION",
            inputs_loaded=False,
            missing_inputs=missing,
        )
        result.output_paths = write_outputs(repo_root, result)
        result.report_paths = write_dataset_expansion_reports(result, repo_root / "reports")
        write_result_doc(repo_root, result)
        return result

    disposition = json.loads((repo_root / "data/frontera_c/disposition/log_boundary_candidate_disposition_v5_6.json").read_text(encoding="utf-8"))
    prior_accepted = json.loads((repo_root / "data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json").read_text(encoding="utf-8")).get("records", [])
    source_pool = build_source_pool(repo_root)
    locations = scan_observable_locations(source_pool)
    ytrue_candidates = build_ytrue_candidates(locations, source_pool, prior_accepted)
    accepted, rejected = split_accepted_rejected(ytrue_candidates)
    dataset = assemble_dataset(accepted)
    quality = assess_dataset_quality(dataset, rejected)
    readiness = build_benchmark_readiness(dataset)
    status = _final_status(dataset.accepted_ytrue_count, dataset.source_count)
    next_gate = {
        "artifact_id": "VISIBILITY-DECOHERENCE-v5_7-NEXT-GATE-DECISION",
        "final_status": status,
        "accepted_ytrue_count_total": dataset.accepted_ytrue_count,
        "independent_source_count": dataset.source_count,
        "v5_8_permitted": dataset.accepted_ytrue_count >= 10 and dataset.source_count >= 2,
        "allowed_next_phase": readiness["allowed_next_phase"],
        "log_boundary_remains_archived": disposition.get("archived_as_validation_candidate") is True,
        "dataset_expansion_is_candidate_rescue": False,
        "physical_claim_created": False,
        "frontera_c_validated": False,
        "blocked_claims": [
            "Frontera C is validated",
            "LOG_BOUNDARY is restored as active validation candidate",
            "The invariant is empirically confirmed",
            "Dataset expansion equals PredictiveGain",
            "Dataset expansion equals validation",
            "Single-source or in-source benchmark generalizes",
        ],
        "allowed_claims": [
            "visibility/decoherence source pool was expanded",
            "additional observable locations were found",
            "dataset quality was assessed",
            "benchmarking stack was hardened",
            "multi-source benchmark is not ready" if dataset.source_count < 2 else "multi-source benchmark readiness was assessed",
        ],
    }
    result = DatasetExpansionCampaignResult(
        status=status,
        inputs_loaded=True,
        source_pool=source_pool,
        location_candidates=locations,
        ytrue_candidates=ytrue_candidates,
        accepted_ytrue=accepted,
        rejected_ytrue=rejected,
        dataset=dataset,
        dataset_quality=quality,
        benchmark_readiness=readiness,
        next_gate_decision=next_gate,
    )
    result.output_paths = write_outputs(repo_root, result)
    result.report_paths = write_dataset_expansion_reports(result, repo_root / "reports")
    write_result_doc(repo_root, result)
    return result


def _final_status(accepted_count: int, source_count: int) -> str:
    if accepted_count >= 10 and source_count >= 2:
        return "VISIBILITY_DECOHERENCE_DATASET_EXPANSION_THRESHOLD_REACHED"
    if accepted_count > 0:
        return "VISIBILITY_DECOHERENCE_DATASET_EXPANSION_PARTIAL"
    return "VISIBILITY_DECOHERENCE_DATASET_EXPANSION_BLOCKED_NO_ACCEPTED_YTRUE"


def write_outputs(root: Path, result: DatasetExpansionCampaignResult) -> dict[str, str]:
    base = root / "data" / "frontera_c" / "dataset_expansion"
    base.mkdir(parents=True, exist_ok=True)
    paths = {
        "source_pool": base / "visibility_decoherence_source_pool_v5_7.json",
        "locations": base / "visibility_decoherence_observable_location_candidates_v5_7.json",
        "ytrue_candidates": base / "visibility_decoherence_ytrue_candidates_v5_7.json",
        "accepted_ytrue": base / "visibility_decoherence_accepted_ytrue_v5_7.json",
        "rejected_ytrue": base / "visibility_decoherence_rejected_ytrue_v5_7.json",
        "dataset": base / "visibility_decoherence_dataset_v5_7.json",
        "quality": base / "visibility_decoherence_dataset_quality_v5_7.json",
        "readiness": base / "visibility_decoherence_benchmark_readiness_v5_7.json",
        "next_gate": base / "v5_7_next_gate_decision.json",
    }
    payloads = {
        "source_pool": {"records": [item.model_dump() for item in result.source_pool], "source_count": len(result.source_pool)},
        "locations": {"records": [item.model_dump() for item in result.location_candidates], "location_count": len(result.location_candidates)},
        "ytrue_candidates": {"records": [item.model_dump() for item in result.ytrue_candidates], "candidate_count": len(result.ytrue_candidates)},
        "accepted_ytrue": {"records": [item.model_dump() for item in result.accepted_ytrue], "accepted_ytrue_count": len(result.accepted_ytrue)},
        "rejected_ytrue": {"records": [item.model_dump() for item in result.rejected_ytrue], "rejected_ytrue_count": len(result.rejected_ytrue)},
        "dataset": result.dataset.model_dump() if result.dataset else {"records": [], "missing_inputs": result.missing_inputs},
        "quality": result.dataset_quality,
        "readiness": result.benchmark_readiness,
        "next_gate": result.next_gate_decision,
    }
    for key, path in paths.items():
        path.write_text(json.dumps(payloads[key], indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}


def write_result_doc(root: Path, result: DatasetExpansionCampaignResult) -> None:
    path = root / "docs" / "338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phygn v5.7 - Visibility/Decoherence Dataset Expansion Results",
        "",
        "Date: 2026-07-02",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/337_PHYGN_CODEX_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_PROMPT.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{result.status}`",
        f"Inputs loaded: `{result.inputs_loaded}`",
        f"Accepted y_true count total: `{len(result.accepted_ytrue)}`",
        f"Independent source count: `{result.dataset.source_count if result.dataset else 0}`",
        "",
        "LOG_BOUNDARY remains archived as a validation candidate. Dataset expansion is not candidate rescue.",
        "",
        "No PredictiveGain was computed. No C-structure ablation was executed. No physical claim was created. Frontera C remains unvalidated.",
    ]
    contract = build_report_contract(
        title="Visibility/Decoherence Dataset Expansion Results v5.7",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="visibility_decoherence_dataset_expansion",
        next_actions=["Continue targeted visibility/decoherence dataset expansion."],
        discipline_note="No more single-source smoke-test authority. Build the benchmark field before judging candidates again.",
    )
    path.write_text(append_canonical_status_section("\n".join(lines) + "\n", contract), encoding="utf-8")
