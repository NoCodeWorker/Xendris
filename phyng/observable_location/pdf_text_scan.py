"""PDF text scanning helpers for v5.7.2 observable locations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PageText:
    page_number: int
    text: str


def extract_pages(path: str | Path) -> list[PageText]:
    try:
        import fitz  # type: ignore
    except Exception:
        return []
    pages: list[PageText] = []
    try:
        with fitz.open(str(path)) as doc:
            for index, page in enumerate(doc, start=1):
                text = page.get_text("text") or ""
                pages.append(PageText(page_number=index, text=text))
    except Exception:
        return []
    return pages
