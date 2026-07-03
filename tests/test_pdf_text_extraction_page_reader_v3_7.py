from __future__ import annotations

import hashlib
from pathlib import Path

from phyng.pdf_text_extraction import pdf_reader
from phyng.pdf_text_extraction.pdf_reader import pdf_reader_availability, read_source_pages
from phyng.pdf_text_extraction.schemas import ExtractedPageText, RegisteredPDFSource


def test_page_text_extraction_records_source_hash(tmp_path: Path) -> None:
    pdf_path = tmp_path / "data" / "real_sources" / "pdfs" / "source.pdf"
    pdf_path.parent.mkdir(parents=True)
    pdf_path.write_bytes(_minimal_pdf_with_text("Visibility decoherence rate equals lambda for 10 amu."))
    sha256 = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    source = RegisteredPDFSource(
        source_id="SRC-TEST",
        local_path="data/real_sources/pdfs/source.pdf",
        sha256=sha256,
        size_bytes=pdf_path.stat().st_size,
        file_type=".pdf",
    )

    pages, summary = read_source_pages(source, tmp_path)

    assert summary.extraction_status.startswith("TEXT_EXTRACTED")
    assert pages
    assert pages[0].source_id == "SRC-TEST"
    assert pages[0].sha256 == sha256
    assert "Visibility decoherence" in pages[0].text


def test_reader_availability_detects_installed_libraries() -> None:
    availability = pdf_reader_availability()

    assert availability["pymupdf"] is True
    assert availability["fitz"] is True
    assert availability["pdfplumber"] is True
    assert availability["pypdf"] is True


def test_pymupdf_reader_attempted_before_internal_parser(tmp_path: Path, monkeypatch) -> None:
    source = _source_with_file(tmp_path)
    calls: list[str] = []

    def pymupdf_reader(path: Path, source: RegisteredPDFSource) -> list[ExtractedPageText]:
        calls.append("pymupdf")
        return [_page(source, "PyMuPDF extracted decoherence visibility text.")]

    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pymupdf", pymupdf_reader)
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_internal_stream_parser", lambda path, source: (_ for _ in ()).throw(AssertionError("internal parser should not run")))

    pages, summary = read_source_pages(source, tmp_path)

    assert calls == ["pymupdf"]
    assert pages
    assert summary.reader_used == "pymupdf"
    assert summary.extraction_status == "TEXT_EXTRACTED_PYMUPDF"


def test_pdfplumber_reader_attempted_before_internal_parser(tmp_path: Path, monkeypatch) -> None:
    source = _source_with_file(tmp_path)
    calls: list[str] = []

    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pymupdf", lambda path, source: calls.append("pymupdf") or [])

    def pdfplumber_reader(path: Path, source: RegisteredPDFSource) -> list[ExtractedPageText]:
        calls.append("pdfplumber")
        return [_page(source, "pdfplumber extracted thermal decoherence text.")]

    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pdfplumber", pdfplumber_reader)
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_internal_stream_parser", lambda path, source: (_ for _ in ()).throw(AssertionError("internal parser should not run")))

    pages, summary = read_source_pages(source, tmp_path)

    assert calls == ["pymupdf", "pdfplumber"]
    assert pages
    assert summary.reader_used == "pdfplumber"
    assert summary.extraction_status == "TEXT_EXTRACTED_PDFPLUMBER"


def test_pypdf_reader_attempted_before_internal_parser(tmp_path: Path, monkeypatch) -> None:
    source = _source_with_file(tmp_path)
    calls: list[str] = []

    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pymupdf", lambda path, source: calls.append("pymupdf") or [])
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pdfplumber", lambda path, source: calls.append("pdfplumber") or [])

    def pypdf_reader(path: Path, source: RegisteredPDFSource) -> list[ExtractedPageText]:
        calls.append("pypdf")
        return [_page(source, "pypdf extracted matter-wave benchmark text.")]

    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pypdf", pypdf_reader)
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_internal_stream_parser", lambda path, source: (_ for _ in ()).throw(AssertionError("internal parser should not run")))

    pages, summary = read_source_pages(source, tmp_path)

    assert calls == ["pymupdf", "pdfplumber", "pypdf"]
    assert pages
    assert summary.reader_used == "pypdf"
    assert summary.extraction_status == "TEXT_EXTRACTED_PYPDF"


def test_internal_parser_only_used_as_fallback(tmp_path: Path, monkeypatch) -> None:
    source = _source_with_file(tmp_path)
    calls: list[str] = []
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pymupdf", lambda path, source: calls.append("pymupdf") or [])
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pdfplumber", lambda path, source: calls.append("pdfplumber") or [])
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pypdf", lambda path, source: calls.append("pypdf") or [])
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_internal_stream_parser", lambda path, source: calls.append("internal") or [_page(source, "internal extracted fallback decoherence text.")])

    pages, summary = read_source_pages(source, tmp_path)

    assert calls == ["pymupdf", "pdfplumber", "pypdf", "internal"]
    assert pages
    assert summary.reader_used == "internal_pdf_stream_parser"
    assert summary.extraction_status == "TEXT_EXTRACTED_INTERNAL_PDF_STREAMS"


def test_pedernales_block_reason_distinguishes_missing_reader_from_failed_reader(tmp_path: Path, monkeypatch) -> None:
    source = _source_with_file(tmp_path)
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pymupdf", lambda path, source: [])
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pdfplumber", lambda path, source: [])
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_pypdf", lambda path, source: [])
    monkeypatch.setattr(pdf_reader, "_read_pdf_with_internal_stream_parser", lambda path, source: [])

    pages, summary = read_source_pages(source, tmp_path)

    assert pages == []
    assert summary.blocked_reason == "PDF_READERS_AVAILABLE_BUT_NO_USABLE_TEXT_EXTRACTED"
    assert summary.reader_availability["pymupdf"] is True
    assert summary.reader_availability["pdfplumber"] is True
    assert summary.reader_availability["pypdf"] is True


def _minimal_pdf_with_text(text: str) -> bytes:
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET"
    return f"""%PDF-1.4
1 0 obj
<< /Length {len(stream)} >>
stream
{stream}
endstream
endobj
%%EOF
""".encode("latin-1")


def _source_with_file(tmp_path: Path) -> RegisteredPDFSource:
    pdf_path = tmp_path / "data" / "real_sources" / "pdfs" / "source.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.write_bytes(b"%PDF-1.4\n")
    return RegisteredPDFSource(
        source_id="SRC-TEST",
        local_path="data/real_sources/pdfs/source.pdf",
        sha256="abc123",
        size_bytes=pdf_path.stat().st_size,
        file_type=".pdf",
    )


def _page(source: RegisteredPDFSource, text: str) -> ExtractedPageText:
    return ExtractedPageText(
        source_id=source.source_id,
        sha256=source.sha256,
        local_path=source.local_path,
        page_number=1,
        text=text,
        extraction_method="test",
        extraction_status="TEXT_EXTRACTED",
    )
