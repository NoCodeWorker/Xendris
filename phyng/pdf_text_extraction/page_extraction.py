"""Page extraction orchestration."""

from __future__ import annotations

from pathlib import Path

from phyng.pdf_text_extraction.pdf_reader import read_source_pages
from phyng.pdf_text_extraction.schemas import ExtractedPageText, RegisteredPDFSource, SourceExtractionSummary


def extract_pages_for_sources(
    sources: list[RegisteredPDFSource],
    root: str | Path = ".",
) -> tuple[list[ExtractedPageText], list[SourceExtractionSummary]]:
    pages: list[ExtractedPageText] = []
    summaries: list[SourceExtractionSummary] = []
    for source in sources:
        source_pages, summary = read_source_pages(source, root)
        pages.extend(source_pages)
        summaries.append(summary)
    return pages, summaries
