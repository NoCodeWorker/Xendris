"""Build and serialize v3.8 validation-ready packs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.extract_candidate_review.schemas import (
    ManualReviewQueueItem,
    RejectedExtractionCandidate,
    ReviewedCandidateMapEntry,
    ReviewedExtractionCandidate,
    ValidationReadyExtract,
    ValidationReadyExtractPack,
)


OUTPUT_PATHS = {
    "validation_ready_pack": Path("data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8.json"),
    "rejected_candidates": Path("data/real_sources/extracts/phi_gradient_rejected_extraction_candidates_v3_8.json"),
    "manual_review_queue": Path("data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8.json"),
    "reviewed_candidate_map": Path("data/real_sources/extracts/phi_gradient_reviewed_candidate_map_v3_8.json"),
    "next_validation_gate_inputs": Path("data/real_sources/extracts/phi_gradient_v3_8_next_validation_gate_inputs.json"),
}


def build_validation_ready_pack(
    reviewed_candidates: list[ReviewedExtractionCandidate],
    rejected_candidates: list[RejectedExtractionCandidate],
    manual_review_queue: list[ManualReviewQueueItem],
    source_hashes: dict,
    status: str,
) -> ValidationReadyExtractPack:
    source_filename_by_id = {
        item["source_id"]: Path(item["local_path"]).name
        for item in source_hashes.get("hashes", [])
    }
    extracts = [
        ValidationReadyExtract(
            extract_id=f"VRX-{candidate.candidate_id}",
            source_id=candidate.source_id,
            sha256=candidate.sha256,
            source_filename=source_filename_by_id.get(candidate.source_id),
            page_number=candidate.page_number,
            location_type=candidate.location_type,
            location_value=candidate.location_value,
            exact_text=candidate.extracted_text,
            candidate_type=candidate.candidate_type,
            component_role=candidate.component_role,
            supported_components=[candidate.component_role],
            contradicted_components=[],
            limitations=candidate.limitations,
            review_status=candidate.review_status,
            validation_ready=True,
        )
        for candidate in reviewed_candidates
        if candidate.validation_ready
    ]
    return ValidationReadyExtractPack(
        extracts=extracts,
        rejected_count=len(rejected_candidates),
        manual_review_count=len(manual_review_queue),
        validation_ready_count=len(extracts),
        status=status,
        notes=["Validation-ready extracts are not support; they are ready for v3.9 judgment."],
    )


def write_v3_8_outputs(
    root: str | Path,
    pack: ValidationReadyExtractPack,
    rejected_candidates: list[RejectedExtractionCandidate],
    manual_review_queue: list[ManualReviewQueueItem],
    reviewed_candidate_map: list[ReviewedCandidateMapEntry],
    blocked_claims: list[str],
    status: str,
) -> dict[str, str]:
    repo_root = Path(root)
    paths = {key: repo_root / path for key, path in OUTPUT_PATHS.items()}
    paths["validation_ready_pack"].parent.mkdir(parents=True, exist_ok=True)
    _write_json(paths["validation_ready_pack"], pack.model_dump(mode="json"))
    _write_json(paths["rejected_candidates"], {"rejected_candidates": [item.model_dump(mode="json") for item in rejected_candidates]})
    _write_json(paths["manual_review_queue"], {"manual_review_queue": [item.model_dump(mode="json") for item in manual_review_queue]})
    _write_json(paths["reviewed_candidate_map"], {"reviewed_candidate_map": [item.model_dump(mode="json") for item in reviewed_candidate_map]})
    _write_json(
        paths["next_validation_gate_inputs"],
        {
            "validation_ready_pack_path": str(OUTPUT_PATHS["validation_ready_pack"]),
            "manual_review_queue_path": str(OUTPUT_PATHS["manual_review_queue"]),
            "rejected_candidates_path": str(OUTPUT_PATHS["rejected_candidates"]),
            "recommended_next_phase": "v3.9 - Validation-Ready Extract Gate & First Source-Pressure Decision",
            "status": status,
            "blocked_claims": blocked_claims,
        },
    )
    return {key: str(path.relative_to(repo_root)) for key, path in paths.items()}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
