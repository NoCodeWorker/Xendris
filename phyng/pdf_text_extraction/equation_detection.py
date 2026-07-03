"""Equation-like candidate detection."""

from __future__ import annotations

import re

from phyng.pdf_text_extraction.candidate_detection import _candidate, _snippets
from phyng.pdf_text_extraction.schemas import ExtractedPageText, PDFExtractionCandidate


EQUATION_RE = re.compile(r"(=|≈|~|\bexp\b|\blog\b|\blambda\b|\bLambda\b|\bCSL\b|\bvisibility\b|\brate\b|γ|Γ|λ|Δ|∂|∇)")


def detect_equation_candidates(pages: list[ExtractedPageText], limit_per_page: int = 4) -> list[PDFExtractionCandidate]:
    candidates: list[PDFExtractionCandidate] = []
    for page in pages:
        lines = re.split(r"\n+|(?<=[.;])\s+", page.text)
        selected = [line for line in lines if len(line.strip()) >= 8 and EQUATION_RE.search(line)]
        for index, line in enumerate(selected[:limit_per_page], start=1):
            candidates.append(
                _candidate(
                    page,
                    index,
                    "EQUATION_CANDIDATE",
                    line,
                    confidence="LOW",
                    notes=["Equation-like or formula-adjacent text detected; PDF extraction may lose formatting."],
                )
            )
    return candidates
