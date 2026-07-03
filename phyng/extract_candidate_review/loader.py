"""Load v3.7 extraction candidates for v3.8 review."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.extract_candidate_review.schemas import RawExtractionCandidate


INPUT_PATHS = {
    "text_extraction": Path("data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json"),
    "quote_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json"),
    "equation_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json"),
    "table_range_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json"),
    "negative_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json"),
    "extraction_manifest": Path("data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json"),
    "source_hashes": Path("data/real_sources/source_hashes_v3_6.json"),
}


def load_v3_7_review_inputs(root: str | Path = ".") -> tuple[list[RawExtractionCandidate], dict, dict, str | None]:
    repo_root = Path(root)
    missing = [str(path) for path in INPUT_PATHS.values() if not (repo_root / path).exists()]
    if missing:
        return [], {}, {}, "PHI_GRADIENT_EXTRACT_REVIEW_BLOCKED_MISSING_CANDIDATES"
    extraction_manifest = _load_json(repo_root / INPUT_PATHS["extraction_manifest"])
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
    return candidates, extraction_manifest, source_hashes, None


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
