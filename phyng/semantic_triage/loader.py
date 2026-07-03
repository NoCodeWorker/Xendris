"""Load v3.8.2 semantic triage inputs."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.extract_candidate_review.schemas import RawExtractionCandidate
from phyng.semantic_triage.schemas import SemanticTriageInputs


INPUT_PATHS = {
    "text_extraction": Path("data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json"),
    "quote_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json"),
    "equation_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json"),
    "table_range_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json"),
    "negative_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json"),
    "extraction_manifest": Path("data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json"),
    "manual_review_queue": Path("data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8.json"),
    "rejected_candidates": Path("data/real_sources/extracts/phi_gradient_rejected_extraction_candidates_v3_8.json"),
    "reviewed_candidate_map": Path("data/real_sources/extracts/phi_gradient_reviewed_candidate_map_v3_8.json"),
    "validation_ready_pack": Path("data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8.json"),
    "source_hashes": Path("data/real_sources/source_hashes_v3_6.json"),
}


def load_semantic_triage_inputs(root: str | Path = ".") -> SemanticTriageInputs:
    repo_root = Path(root)
    missing = [str(path) for path in INPUT_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return SemanticTriageInputs(blocked_reason="PHI_GRADIENT_SEMANTIC_TRIAGE_BLOCKED_MISSING_INPUTS")

    source_hashes = _load_json(repo_root / INPUT_PATHS["source_hashes"])
    valid_hashes = {item["source_id"]: item["sha256"] for item in source_hashes.get("hashes", [])}
    candidates: list[RawExtractionCandidate] = []
    for key in ("quote_candidates", "equation_candidates", "table_range_candidates", "negative_candidates"):
        payload = _load_json(repo_root / INPUT_PATHS[key])
        for raw in payload.get("candidates", []):
            source_id = raw.get("source_id")
            if source_id not in valid_hashes:
                continue
            if raw.get("sha256") != valid_hashes[source_id]:
                continue
            candidates.append(RawExtractionCandidate(**raw))

    return SemanticTriageInputs(
        candidates=candidates,
        extraction_manifest=_load_json(repo_root / INPUT_PATHS["extraction_manifest"]),
        manual_review_queue=_load_json(repo_root / INPUT_PATHS["manual_review_queue"]).get("manual_review_queue", []),
        rejected_candidates=_load_json(repo_root / INPUT_PATHS["rejected_candidates"]).get("rejected_candidates", []),
        reviewed_candidate_map=_load_json(repo_root / INPUT_PATHS["reviewed_candidate_map"]).get("reviewed_candidate_map", []),
        validation_ready_pack=_load_json(repo_root / INPUT_PATHS["validation_ready_pack"]),
        source_hashes=source_hashes,
    )


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
