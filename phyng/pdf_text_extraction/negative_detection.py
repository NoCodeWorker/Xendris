"""Negative or limitation candidate detection."""

from __future__ import annotations

from phyng.pdf_text_extraction.candidate_detection import _candidate, _snippets
from phyng.pdf_text_extraction.schemas import ExtractedPageText, PDFExtractionCandidate


NEGATIVE_KEYWORDS = (
    "dominates",
    "negligible",
    "excluded",
    "ruled out",
    "background",
    "environmental",
    "thermal",
    "scattering",
    "limitation",
    "limited",
)


def detect_negative_candidates(pages: list[ExtractedPageText], limit_per_page: int = 4) -> list[PDFExtractionCandidate]:
    candidates: list[PDFExtractionCandidate] = []
    for page in pages:
        selected = [snippet for snippet in _snippets(page.text) if _contains_negative(snippet)]
        for index, snippet in enumerate(selected[:limit_per_page], start=1):
            lower = snippet.lower()
            candidate_type = "LIMITATION_CANDIDATE" if "limitation" in lower or "limited" in lower else "NEGATIVE_CONSTRAINT_CANDIDATE"
            candidates.append(
                _candidate(
                    page,
                    index,
                    candidate_type,
                    snippet,
                    confidence="LOW",
                    notes=["Negative-pressure or limitation keyword detected; manual review required before gate impact."],
                )
            )
    return candidates


def _contains_negative(text: str) -> bool:
    lower = text.lower()
    return any(keyword in lower for keyword in NEGATIVE_KEYWORDS)
