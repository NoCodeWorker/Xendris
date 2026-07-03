"""Range, table, and figure candidate detection."""

from __future__ import annotations

import re

from phyng.pdf_text_extraction.candidate_detection import _candidate, _snippets
from phyng.pdf_text_extraction.schemas import ExtractedPageText, PDFExtractionCandidate


UNITS_RE = re.compile(r"\b\d+(?:\.\d+)?(?:\s*(?:-|to|–)\s*\d+(?:\.\d+)?)?\s*(amu|kg|m|nm|s|ms|K|Pa|mbar|Hz|s\^-1)\b", re.I)
CAPTION_RE = re.compile(r"\b(table|fig\.|figure)\s*\d*", re.I)
BENCHMARK_RE = re.compile(r"\b(visibility|decoherence rate|mass|separation|distance|time|temperature|pressure|benchmark)\b", re.I)


def detect_range_candidates(pages: list[ExtractedPageText], limit_per_page: int = 4) -> list[PDFExtractionCandidate]:
    candidates: list[PDFExtractionCandidate] = []
    for page in pages:
        selected = [snippet for snippet in _snippets(page.text) if UNITS_RE.search(snippet) or (BENCHMARK_RE.search(snippet) and re.search(r"\d", snippet))]
        for index, snippet in enumerate(selected[:limit_per_page], start=1):
            candidate_type = "BENCHMARK_RANGE_CANDIDATE" if BENCHMARK_RE.search(snippet) else "PARAMETER_RANGE_CANDIDATE"
            candidates.append(
                _candidate(
                    page,
                    index,
                    candidate_type,
                    snippet,
                    confidence="MEDIUM" if UNITS_RE.search(snippet) else "LOW",
                    notes=["Numeric or unit-bearing range candidate detected."],
                )
            )
    return candidates


def detect_caption_candidates(pages: list[ExtractedPageText], limit_per_page: int = 3) -> list[PDFExtractionCandidate]:
    candidates: list[PDFExtractionCandidate] = []
    for page in pages:
        selected = [snippet for snippet in _snippets(page.text) if CAPTION_RE.search(snippet)]
        for index, snippet in enumerate(selected[:limit_per_page], start=1):
            lower = snippet.lower()
            candidate_type = "TABLE_CAPTION_CANDIDATE" if "table" in lower else "FIGURE_CAPTION_CANDIDATE"
            candidates.append(
                _candidate(
                    page,
                    index,
                    candidate_type,
                    snippet,
                    confidence="LOW",
                    notes=["Caption-like text detected; table/figure role requires review."],
                )
            )
    return candidates
