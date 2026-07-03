"""Campaign orchestration for v5.7.1 targeted source acquisition."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.source_acquisition.candidate_sources import build_candidate_sources
from phyng.source_acquisition.download_queue import build_download_queue
from phyng.source_acquisition.identity_matrix import build_identity_matrix
from phyng.source_acquisition.observable_target_matrix import build_observable_target_matrix
from phyng.source_acquisition.rejection_log import build_rejection_log
from phyng.source_acquisition.reports import write_source_acquisition_reports
from phyng.source_acquisition.schemas import SourceAcquisitionCampaignResult


REQUIRED_INPUTS = [
    "docs/338_PHYGN_V5_7_VISIBILITY_DECOHERENCE_DATASET_EXPANSION_RESULTS.md",
    "docs/332_PHYGN_V5_6_LOG_BOUNDARY_CONTROL_FAILURE_REVIEW_RESULTS.md",
    "data/frontera_c/dataset_expansion/visibility_decoherence_dataset_v5_7.json",
    "data/frontera_c/dataset_expansion/visibility_decoherence_dataset_quality_v5_7.json",
    "data/frontera_c/dataset_expansion/visibility_decoherence_benchmark_readiness_v5_7.json",
    "data/frontera_c/dataset_expansion/v5_7_next_gate_decision.json",
    "data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json",
    "data/preflight/source_identity/source_identity_resolution_integrated_v5_1.json",
    "data/real_sources/source_hashes_v3_6.json",
]


def run_frontera_c_targeted_visibility_decoherence_literature_acquisition_campaign(root: str | Path = ".") -> SourceAcquisitionCampaignResult:
    repo_root = Path(root)
    missing = [path for path in REQUIRED_INPUTS if not (repo_root / path).exists()]
    if missing:
        result = SourceAcquisitionCampaignResult(
            status="FRONTERA_C_REQUIRES_TARGETED_DATASET_EXPANSION",
            inputs_loaded=False,
            missing_inputs=missing,
        )
        result.output_paths = write_outputs(repo_root, result)
        result.report_paths = write_source_acquisition_reports(result, repo_root / "reports")
        write_result_doc(repo_root, result)
        return result

    queue = build_candidate_sources()
    identity = build_identity_matrix(queue)
    observable = build_observable_target_matrix(queue)
    download = build_download_queue(queue)
    rejection = build_rejection_log()
    resolved_count = sum(1 for item in identity if item.identity_complete)
    high_priority_count = sum(1 for item in queue if item.priority in {"CRITICAL", "HIGH"})
    likely_observable_count = sum(1 for item in queue if item.likely_observable_location)
    download_required_count = len(download)
    human_lookup_required_count = sum(1 for item in queue if item.source_identity_status != "RESOLVED_COMPLETE")
    status = (
        "TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_REQUIRES_DOWNLOAD"
        if resolved_count >= 3
        else "TARGETED_VISIBILITY_DECOHERENCE_SOURCE_ACQUISITION_REQUIRES_HUMAN_LOOKUP"
    )
    next_gate = {
        "artifact_id": "TARGETED-VISIBILITY-DECOHERENCE-v5_7_1-NEXT-GATE-DECISION",
        "final_status": status,
        "resolved_candidate_source_count": resolved_count,
        "high_priority_source_count": high_priority_count,
        "likely_observable_source_count": likely_observable_count,
        "download_required_count": download_required_count,
        "human_lookup_required_count": human_lookup_required_count,
        "allowed_next_phase": "v5.7.2 - Targeted Source Download & Observable Location Review" if resolved_count >= 3 else None,
        "blocked_next_phases": ["y_true extraction", "PredictiveGain computation", "Frontera C validation"],
        "rationale": "At least three resolved candidate source identities were found; source files must be acquired before observable review.",
        "log_boundary_reactivated": False,
        "source_acquisition_is_evidence": False,
        "no_ytrue_extracted": True,
        "no_predictive_gain_computed": True,
        "physical_claim_created": False,
        "frontera_c_validated": False,
        "blocked_claims": [
            "Frontera C is validated",
            "LOG_BOUNDARY is reactivated",
            "literature acquisition equals evidence",
            "source identity equals y_true",
            "source relevance equals benchmark readiness",
        ],
        "allowed_claims": [
            "targeted acquisition queue was created",
            "candidate sources were resolved",
            "candidate sources require download",
            "observable targets were prioritized",
        ],
    }
    result = SourceAcquisitionCampaignResult(
        status=status,
        inputs_loaded=True,
        acquisition_queue=queue,
        identity_matrix=identity,
        observable_matrix=observable,
        download_queue=download,
        rejection_log=rejection,
        next_gate_decision=next_gate,
    )
    result.output_paths = write_outputs(repo_root, result)
    result.report_paths = write_source_acquisition_reports(result, repo_root / "reports")
    write_result_doc(repo_root, result)
    return result


def write_outputs(root: Path, result: SourceAcquisitionCampaignResult) -> dict[str, str]:
    base = root / "data" / "frontera_c" / "source_acquisition"
    base.mkdir(parents=True, exist_ok=True)
    paths = {
        "queue": base / "visibility_decoherence_source_acquisition_queue_v5_7_1.json",
        "identity": base / "visibility_decoherence_candidate_source_identity_matrix_v5_7_1.json",
        "observable": base / "visibility_decoherence_observable_target_matrix_v5_7_1.json",
        "download": base / "visibility_decoherence_download_priority_queue_v5_7_1.json",
        "rejection": base / "visibility_decoherence_source_rejection_log_v5_7_1.json",
        "next_gate": base / "v5_7_1_next_gate_decision.json",
    }
    payloads = {
        "queue": {"records": [item.model_dump() for item in result.acquisition_queue], "queue_count": len(result.acquisition_queue)},
        "identity": {"records": [item.model_dump() for item in result.identity_matrix], "resolved_candidate_source_count": sum(1 for item in result.identity_matrix if item.identity_complete)},
        "observable": {"records": [item.model_dump() for item in result.observable_matrix], "target_count": len(result.observable_matrix)},
        "download": {"records": [item.model_dump() for item in result.download_queue], "download_count": len(result.download_queue)},
        "rejection": {"records": [item.model_dump() for item in result.rejection_log], "rejection_count": len(result.rejection_log)},
        "next_gate": result.next_gate_decision,
    }
    for key, path in paths.items():
        path.write_text(json.dumps(payloads[key], indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}


def write_result_doc(root: Path, result: SourceAcquisitionCampaignResult) -> None:
    path = root / "docs" / "344_PHYGN_V5_7_1_TARGETED_VISIBILITY_DECOHERENCE_LITERATURE_ACQUISITION_RESULTS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phygn v5.7.1 - Targeted Visibility/Decoherence Literature Acquisition Results",
        "",
        "Date: 2026-07-02",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/343_PHYGN_CODEX_V5_7_1_TARGETED_LITERATURE_ACQUISITION_PROMPT.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{result.status}`",
        f"Inputs loaded: `{result.inputs_loaded}`",
        f"Resolved candidate sources: `{result.next_gate_decision.get('resolved_candidate_source_count')}`",
        f"Download required: `{result.next_gate_decision.get('download_required_count')}`",
        f"Allowed next phase: `{result.next_gate_decision.get('allowed_next_phase')}`",
        "",
        "This phase created a source acquisition queue only. It did not extract y_true, compute PredictiveGain, reactivate LOG_BOUNDARY, validate Frontera C, or create physical claims.",
    ]
    contract = build_report_contract(
        title="Targeted Visibility/Decoherence Literature Acquisition Results v5.7.1",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="targeted_visibility_decoherence_source_acquisition",
        next_actions=["Download resolved source PDFs before observable location review."],
        discipline_note="A source queue is not evidence. It is a map toward possible evidence.",
    )
    path.write_text(append_canonical_status_section("\n".join(lines) + "\n", contract), encoding="utf-8")
