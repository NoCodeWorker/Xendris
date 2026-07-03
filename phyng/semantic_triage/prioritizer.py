"""Build semantic triage records."""

from __future__ import annotations

import re

from phyng.extract_candidate_review.schemas import RawExtractionCandidate
from phyng.semantic_triage.schemas import SemanticTriageRecord
from phyng.semantic_triage.scoring import score_candidate
from phyng.semantic_triage.slot_rules import assign_slot


def triage_candidates(candidates: list[RawExtractionCandidate]) -> list[SemanticTriageRecord]:
    return [triage_candidate(candidate) for candidate in candidates]


def triage_candidate(candidate: RawExtractionCandidate) -> SemanticTriageRecord:
    normalized = candidate.normalized_text or _normalize(candidate.extracted_text)
    slot = assign_slot(normalized, candidate.source_id)
    scores = score_candidate(candidate, slot)
    return SemanticTriageRecord(
        candidate_id=candidate.candidate_id,
        source_id=candidate.source_id,
        sha256=candidate.sha256,
        page_number=candidate.page_number,
        candidate_type=candidate.candidate_type,
        extracted_text=candidate.extracted_text,
        normalized_text=normalized,
        assigned_slot=slot,
        semantic_score=float(scores["semantic_score"]),
        source_priority_score=float(scores["source_priority_score"]),
        slot_relevance_score=float(scores["slot_relevance_score"]),
        cleanliness_score=float(scores["cleanliness_score"]),
        specificity_score=float(scores["specificity_score"]),
        risk_score=float(scores["risk_score"]),
        triage_score=float(scores["triage_score"]),
        priority=str(scores["priority"]),
        include_in_priority_packet=bool(scores["include_in_priority_packet"]),
        review_question=_review_question(slot),
        decision_needed=_decision_needed(slot),
        notes=list(scores["notes"]),
    )


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _review_question(slot: str) -> str:
    return f"Does this candidate provide exact, source-faithful material for {slot} without overclaiming?"


def _decision_needed(slot: str) -> str:
    return f"Classify this candidate for {slot}: validation-ready extract, manual review, analogy-only, negative constraint, or reject."
