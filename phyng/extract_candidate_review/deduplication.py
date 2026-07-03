"""Deduplicate extraction candidates."""

from __future__ import annotations

from phyng.extract_candidate_review.schemas import RawExtractionCandidate


def split_unique_candidates(candidates: list[RawExtractionCandidate]) -> tuple[list[RawExtractionCandidate], list[RawExtractionCandidate]]:
    seen: set[tuple[str, int | None, str, str]] = set()
    unique: list[RawExtractionCandidate] = []
    duplicates: list[RawExtractionCandidate] = []
    for candidate in candidates:
        key = (
            candidate.source_id,
            candidate.page_number,
            candidate.candidate_type,
            candidate.normalized_text or candidate.extracted_text.strip().lower(),
        )
        if key in seen:
            duplicates.append(candidate)
            continue
        seen.add(key)
        unique.append(candidate)
    return unique, duplicates
