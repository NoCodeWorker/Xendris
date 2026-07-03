"""Candidate detection from extracted page text."""

from __future__ import annotations

import re

from phyng.pdf_text_extraction.schemas import ExtractedPageText, PDFExtractionCandidate


OBSERVABLE_KEYWORDS = ("visibility", "fringe", "contrast", "decoherence", "coherence", "interference", "rate", "loss")


def detect_quote_candidates(pages: list[ExtractedPageText], limit_per_page: int = 3) -> list[PDFExtractionCandidate]:
    candidates: list[PDFExtractionCandidate] = []
    for page in pages:
        snippets = _snippets(page.text)
        selected = [snippet for snippet in snippets if _contains_any(snippet, OBSERVABLE_KEYWORDS)]
        for index, snippet in enumerate(selected[:limit_per_page], start=1):
            candidates.append(
                _candidate(
                    page,
                    index,
                    "QUOTE_CANDIDATE",
                    snippet,
                    confidence="MEDIUM" if len(snippet) <= 320 else "LOW",
                    notes=["Localized extracted text candidate; review required before source pressure."],
                )
            )
    return candidates


def detect_observable_candidates(pages: list[ExtractedPageText], limit_per_page: int = 2) -> list[PDFExtractionCandidate]:
    candidates: list[PDFExtractionCandidate] = []
    for page in pages:
        selected = [snippet for snippet in _snippets(page.text) if _contains_any(snippet, OBSERVABLE_KEYWORDS)]
        for index, snippet in enumerate(selected[:limit_per_page], start=1):
            candidates.append(
                _candidate(
                    page,
                    index,
                    "OBSERVABLE_CANDIDATE",
                    snippet,
                    confidence="LOW",
                    notes=["Observable-like text detected from keyword match."],
                )
            )
    return candidates


def _candidate(
    page: ExtractedPageText,
    index: int,
    candidate_type: str,
    text: str,
    confidence: str = "LOW",
    notes: list[str] | None = None,
) -> PDFExtractionCandidate:
    return PDFExtractionCandidate(
        candidate_id=f"{candidate_type}-{page.source_id}-P{page.page_number:03d}-{index:03d}",
        source_id=page.source_id,
        sha256=page.sha256,
        page_number=page.page_number,
        location_type="PAGE_TEXT",
        location_value=f"page={page.page_number}; candidate_index={index}",
        candidate_type=candidate_type,
        extracted_text=_trim(text),
        normalized_text=_normalize(text),
        confidence=confidence,
        requires_manual_review=True,
        notes=notes or [],
    )


def _snippets(text: str) -> list[str]:
    rough = re.split(r"(?<=[.!?])\s+|\n+", text)
    snippets = [_trim(item) for item in rough if len(item.strip()) >= 35]
    if snippets:
        return snippets
    return [_trim(text)] if text.strip() else []


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(keyword.lower() in lower for keyword in keywords)


def _trim(text: str, limit: int = 500) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    return clean[: limit - 3] + "..." if len(clean) > limit else clean


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()
