"""Semantic scoring for v3.8.2 triage."""

from __future__ import annotations

import re

from phyng.extract_candidate_review.schemas import RawExtractionCandidate
from phyng.semantic_triage.slot_rules import (
    SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE,
    SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS,
    SLOT_5_PARAMETER_CONSTRAINTS,
    SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS,
    SLOT_8_ANALOGY_ONLY_OR_BACKGROUND,
    slot_keyword_hit_ratio,
)


SOURCE_PRIORITY = {
    "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING": 1.0,
    "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS": 0.95,
    "SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST": 0.90,
    "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE": 0.85,
    "SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE": 0.85,
}


def score_candidate(candidate: RawExtractionCandidate, assigned_slot: str) -> dict[str, float | str | bool | list[str]]:
    text = candidate.extracted_text or ""
    lowered = text.lower()
    semantic_score = _semantic_score(lowered, assigned_slot)
    source_priority_score = SOURCE_PRIORITY.get(candidate.source_id, 0.5)
    slot_relevance_score = _slot_relevance_score(lowered, assigned_slot)
    cleanliness_score = _cleanliness_score(text)
    specificity_score = _specificity_score(text)
    risk_score = _risk_score(lowered)
    triage_score = round(
        0.25 * semantic_score
        + 0.20 * slot_relevance_score
        + 0.20 * source_priority_score
        + 0.15 * specificity_score
        + 0.10 * cleanliness_score
        + 0.10 * risk_score,
        4,
    )
    priority = _priority(candidate, assigned_slot, triage_score, cleanliness_score)
    notes: list[str] = []
    if priority == "EXCLUDE":
        notes.append("Excluded by low semantic triage score or obvious low-value text.")
    if _pedernales_slot4(candidate, assigned_slot):
        notes.append("Pedernales SLOT_4 minimum HIGH priority override applied.")
    return {
        "semantic_score": semantic_score,
        "source_priority_score": source_priority_score,
        "slot_relevance_score": slot_relevance_score,
        "cleanliness_score": cleanliness_score,
        "specificity_score": specificity_score,
        "risk_score": risk_score,
        "triage_score": triage_score,
        "priority": priority,
        "include_in_priority_packet": priority in {"CRITICAL", "HIGH", "MEDIUM"},
        "notes": notes,
    }


def _semantic_score(text: str, slot: str) -> float:
    base = slot_keyword_hit_ratio(text, slot)
    if slot in {SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS, SLOT_5_PARAMETER_CONSTRAINTS, SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS}:
        base += 0.15
    if slot == SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE:
        base += 0.10
    if slot == SLOT_8_ANALOGY_ONLY_OR_BACKGROUND:
        base -= 0.10
    return _clamp(base)


def _slot_relevance_score(text: str, slot: str) -> float:
    return _clamp(0.35 + 0.65 * slot_keyword_hit_ratio(text, slot))


def _cleanliness_score(text: str) -> float:
    stripped = re.sub(r"\s+", " ", text).strip()
    if len(stripped) < 20:
        return 0.15
    alpha = sum(char.isalpha() for char in stripped)
    symbols = sum((not char.isalnum() and not char.isspace()) for char in stripped)
    alpha_ratio = alpha / max(len(stripped), 1)
    symbol_ratio = symbols / max(len(stripped), 1)
    repeated = len(re.findall(r"\b(\w+)\b(?:\s+\1\b){2,}", stripped.lower()))
    return _clamp(0.25 + alpha_ratio - symbol_ratio - 0.15 * repeated)


def _specificity_score(text: str) -> float:
    patterns = [
        r"\b\d+(\.\d+)?\s?(amu|mbar|nm|pm|k|s|ms|hz|khz|mhz)\b",
        r"\b(eq\.?|equation|fig\.?|table)\s?\d+",
        r"\b(lambda|r_c|csl|mmm|hamiltonian|visibility|contrast|pressure|temperature)\b",
        r"[=<>≤≥]",
    ]
    lowered = text.lower()
    hits = sum(1 for pattern in patterns if re.search(pattern, lowered))
    return _clamp(0.25 + hits * 0.22)


def _risk_score(text: str) -> float:
    risky_terms = [
        "negligible",
        "dominates",
        "excluded",
        "ruled out",
        "limitation",
        "noise",
        "background",
        "incompatible",
        "falsify",
        "constraint",
        "bound",
    ]
    return _clamp(0.25 + 0.15 * sum(1 for term in risky_terms if term in text))


def _priority(candidate: RawExtractionCandidate, slot: str, triage_score: float, cleanliness_score: float) -> str:
    if _pedernales_slot4(candidate, slot) and cleanliness_score >= 0.25:
        return "HIGH" if triage_score < 0.82 else "CRITICAL"
    if candidate.source_id == "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS" and slot in {SLOT_5_PARAMETER_CONSTRAINTS, SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS} and cleanliness_score >= 0.25:
        return "HIGH" if triage_score < 0.82 else "CRITICAL"
    if candidate.source_id == "SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST" and slot == SLOT_5_PARAMETER_CONSTRAINTS and cleanliness_score >= 0.25:
        return "HIGH" if triage_score < 0.82 else "CRITICAL"
    if cleanliness_score < 0.20 or triage_score < 0.35:
        return "EXCLUDE"
    if triage_score >= 0.82 and slot in {SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS, SLOT_5_PARAMETER_CONSTRAINTS, SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS, SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE}:
        return "CRITICAL"
    if triage_score >= 0.68:
        return "HIGH"
    if triage_score >= 0.50:
        return "MEDIUM"
    if triage_score >= 0.35:
        return "LOW"
    return "EXCLUDE"


def _pedernales_slot4(candidate: RawExtractionCandidate, slot: str) -> bool:
    return candidate.source_id == "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING" and slot == SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS


def _clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 4)
