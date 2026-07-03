"""Deterministic text readers for local source files."""

from __future__ import annotations

import importlib
import importlib.util
import re
import zlib
from pathlib import Path

from phyng.pdf_text_extraction.schemas import ExtractedPageText, RegisteredPDFSource, SourceExtractionSummary


def read_source_pages(source: RegisteredPDFSource, root: str | Path = ".") -> tuple[list[ExtractedPageText], SourceExtractionSummary]:
    repo_root = Path(root)
    path = repo_root / source.local_path
    availability = pdf_reader_availability()
    if not path.exists():
        return [], _summary(source, "EXTRACTION_BLOCKED_MISSING_FILE", "Registered file is missing.", True, reader_availability=availability)
    if source.file_type in {".txt", ".md", ".html"}:
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        return _pages_from_text(source, text, "plain_text_file"), _summary(source, "TEXT_EXTRACTED_PLAIN_TEXT", None, False, 1 if text else 0, reader_used="plain_text_file", reader_availability=availability)
    if source.file_type != ".pdf":
        return [], _summary(source, "EXTRACTION_BLOCKED_UNSUPPORTED_FILE_TYPE", "Unsupported file type.", True, reader_availability=availability)

    pages, reader_used, attempted_readers = _read_pdf_with_available_library(path, source)
    if pages:
        return pages, _summary(source, f"TEXT_EXTRACTED_{reader_used.upper()}", None, False, len(pages), reader_used=reader_used, reader_availability=availability)

    pages = _read_pdf_with_internal_stream_parser(path, source)
    if pages:
        note = None
        if attempted_readers:
            note = "Installed PDF readers were attempted first but returned no usable text; internal parser produced review-only text."
        return pages, _summary(source, "TEXT_EXTRACTED_INTERNAL_PDF_STREAMS", note, True, len(pages), reader_used="internal_pdf_stream_parser", reader_availability=availability)

    readers_available = any(availability.values())
    if readers_available:
        return [], _summary(
            source,
            "EXTRACTION_REQUIRES_PDF_READER_OR_MANUAL_REVIEW",
            "PDF_READERS_AVAILABLE_BUT_NO_USABLE_TEXT_EXTRACTED",
            True,
            reader_used=None,
            reader_availability=availability,
        )

    return [], _summary(
        source,
        "EXTRACTION_REQUIRES_PDF_READER_OR_MANUAL_REVIEW",
        "No installed PDF reader extracted text and internal stream parsing found no usable text.",
        True,
        reader_availability=availability,
    )


def pdf_reader_availability() -> dict[str, bool]:
    return {
        "pymupdf": _module_importable("fitz"),
        "fitz": _module_importable("fitz"),
        "pdfplumber": _module_importable("pdfplumber"),
        "pypdf": _module_importable("pypdf"),
    }


def _module_importable(name: str) -> bool:
    if importlib.util.find_spec(name) is None:
        return False
    try:
        importlib.import_module(name)
        return True
    except Exception:
        return False


def _read_pdf_with_available_library(path: Path, source: RegisteredPDFSource) -> tuple[list[ExtractedPageText], str | None, list[str]]:
    readers = [
        ("pymupdf", "fitz", _read_pdf_with_pymupdf),
        ("pdfplumber", "pdfplumber", _read_pdf_with_pdfplumber),
        ("pypdf", "pypdf", _read_pdf_with_pypdf),
    ]
    attempted: list[str] = []
    for reader_name, module_name, reader in readers:
        if not _module_importable(module_name):
            continue
        attempted.append(reader_name)
        pages = reader(path, source)
        if pages:
            return pages, reader_name, attempted
    return [], None, attempted


def _read_pdf_with_pymupdf(path: Path, source: RegisteredPDFSource) -> list[ExtractedPageText]:
    try:
        import fitz  # type: ignore

        pages = []
        with fitz.open(path) as doc:
            for index, page in enumerate(doc, start=1):
                text = (page.get_text("text") or "").strip()
                if text:
                    pages.append(_page(source, index, text, "pymupdf"))
        return pages
    except Exception:
        return []


def _read_pdf_with_pdfplumber(path: Path, source: RegisteredPDFSource) -> list[ExtractedPageText]:
    try:
        import pdfplumber  # type: ignore

        pages = []
        with pdfplumber.open(path) as pdf:
            for index, page in enumerate(pdf.pages, start=1):
                text = (page.extract_text() or "").strip()
                if text:
                    pages.append(_page(source, index, text, "pdfplumber"))
        return pages
    except Exception:
        return []


def _read_pdf_with_pypdf(path: Path, source: RegisteredPDFSource) -> list[ExtractedPageText]:
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        pages = []
        for index, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append(_page(source, index, text, "pypdf"))
        return pages
    except Exception:
        return []


def _read_pdf_with_internal_stream_parser(path: Path, source: RegisteredPDFSource) -> list[ExtractedPageText]:
    data = path.read_bytes()
    pages: list[ExtractedPageText] = []
    for stream_index, match in enumerate(re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S), start=1):
        raw_stream = match.group(1).strip(b"\r\n")
        dictionary_window = data[max(0, match.start() - 600) : match.start()]
        decoded_streams = [raw_stream]
        if b"FlateDecode" in dictionary_window:
            try:
                decoded_streams.insert(0, zlib.decompress(raw_stream))
            except Exception:
                pass
        text_parts: list[str] = []
        for stream in decoded_streams:
            stream_text = stream.decode("latin-1", errors="ignore")
            text_parts.extend(_extract_pdf_text_operands(stream_text))
        text = _normalize_text(" ".join(text_parts))
        if _usable_text(text):
            pages.append(_page(source, stream_index, text, "internal_pdf_stream_parser"))
    return pages


def _extract_pdf_text_operands(stream_text: str) -> list[str]:
    parts: list[str] = []
    parts.extend(_decode_pdf_literal(item) for item in re.findall(r"\((?:\\.|[^\\)])*\)\s*(?:Tj|'|\")", stream_text))
    for array_body in re.findall(r"\[(.*?)\]\s*TJ", stream_text, flags=re.S):
        parts.extend(_decode_pdf_literal(item) for item in re.findall(r"\((?:\\.|[^\\)])*\)", array_body))
    for hex_text in re.findall(r"<([0-9A-Fa-f\s]{4,})>\s*Tj", stream_text):
        decoded = _decode_hex_text(hex_text)
        if decoded:
            parts.append(decoded)
    return [part for part in parts if part.strip()]


def _decode_pdf_literal(token: str) -> str:
    value = token[1:-1] if token.startswith("(") and token.endswith(")") else token
    value = re.sub(r"\\([0-7]{1,3})", lambda match: chr(int(match.group(1), 8)), value)
    value = value.replace(r"\(", "(").replace(r"\)", ")").replace(r"\\", "\\")
    value = value.replace(r"\n", " ").replace(r"\r", " ").replace(r"\t", " ")
    value = "".join(char if char == "\n" or char == "\t" or ord(char) >= 32 else " " for char in value)
    return value


def _decode_hex_text(hex_text: str) -> str:
    cleaned = re.sub(r"\s+", "", hex_text)
    try:
        data = bytes.fromhex(cleaned)
    except ValueError:
        return ""
    if b"\x00" in data:
        return data.decode("utf-16-be", errors="ignore")
    return data.decode("latin-1", errors="ignore")


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _usable_text(text: str) -> bool:
    if len(text) < 20:
        return False
    alpha_count = sum(char.isalpha() for char in text)
    return alpha_count >= 12


def _pages_from_text(source: RegisteredPDFSource, text: str, method: str) -> list[ExtractedPageText]:
    if not text.strip():
        return []
    return [_page(source, 1, text.strip(), method)]


def _page(source: RegisteredPDFSource, page_number: int, text: str, method: str) -> ExtractedPageText:
    return ExtractedPageText(
        source_id=source.source_id,
        sha256=source.sha256,
        local_path=source.local_path,
        page_number=page_number,
        text=text,
        extraction_method=method,
        extraction_status="TEXT_EXTRACTED",
    )


def _summary(
    source: RegisteredPDFSource,
    status: str,
    note: str | None,
    requires_manual_review: bool,
    pages: int = 0,
    reader_used: str | None = None,
    reader_availability: dict[str, bool] | None = None,
) -> SourceExtractionSummary:
    return SourceExtractionSummary(
        source_id=source.source_id,
        sha256=source.sha256,
        local_path=source.local_path,
        extraction_status=status,
        reader_used=reader_used,
        pages_extracted=pages,
        blocked_reason=note,
        requires_manual_review=requires_manual_review,
        reader_availability=reader_availability or {},
        notes=[note] if note else [],
    )
