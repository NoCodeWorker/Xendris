"""Garbage/noise filters for raw extraction candidates."""

from __future__ import annotations

import re

from phyng.extract_candidate_review.schemas import RawExtractionCandidate


def garbage_reason(candidate: RawExtractionCandidate) -> str | None:
    text = candidate.extracted_text or ""
    clean = text.strip()
    if not clean:
        return "empty extracted text"
    if len(clean) > 900:
        return "candidate text exceeds review length limit"
    if _control_ratio(clean) > 0.04:
        return "candidate contains excessive control or binary-looking characters"
    if _alpha_ratio(clean) < 0.28:
        return "candidate lacks enough readable alphabetic content"
    if _spaced_letter_ratio(clean) > 0.45 and len(clean) > 120:
        return "candidate text is heavily damaged by PDF character spacing"
    lower = clean.lower()
    if lower.startswith("references") or lower in {"abstract", "introduction"}:
        return "candidate appears to be header/footer/reference noise"
    if not _has_scientific_signal(lower):
        return "candidate lacks reviewable scientific signal"
    return None


def short_preview(text: str, limit: int = 220) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    return clean[: limit - 3] + "..." if len(clean) > limit else clean


def _control_ratio(text: str) -> float:
    if not text:
        return 1.0
    bad = sum(1 for char in text if ord(char) < 32 or 127 <= ord(char) <= 159)
    return bad / len(text)


def _alpha_ratio(text: str) -> float:
    if not text:
        return 0.0
    return sum(1 for char in text if char.isalpha()) / len(text)


def _spaced_letter_ratio(text: str) -> float:
    tokens = text.split()
    if not tokens:
        return 0.0
    single_letters = sum(1 for token in tokens if len(token) == 1 and token.isalpha())
    return single_letters / len(tokens)


def _has_scientific_signal(text: str) -> bool:
    signals = (
        "decoherence",
        "coherence",
        "visibility",
        "interference",
        "matter",
        "wave",
        "csl",
        "collapse",
        "mass",
        "temperature",
        "scattering",
        "rate",
        "constraint",
        "hypothesis",
        "gradient",
        "thermal",
    )
    return any(signal in text for signal in signals)
