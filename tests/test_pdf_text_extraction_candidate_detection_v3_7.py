from __future__ import annotations

from phyng.pdf_text_extraction.candidate_detection import detect_quote_candidates
from phyng.pdf_text_extraction.equation_detection import detect_equation_candidates
from phyng.pdf_text_extraction.negative_detection import detect_negative_candidates
from phyng.pdf_text_extraction.range_detection import detect_range_candidates
from phyng.pdf_text_extraction.schemas import ExtractedPageText


def _page(text: str) -> ExtractedPageText:
    return ExtractedPageText(
        source_id="SRC-TEST",
        sha256="abc123",
        local_path="data/real_sources/pdfs/source.pdf",
        page_number=2,
        text=text,
        extraction_method="test",
        extraction_status="TEXT_EXTRACTED",
    )


def test_candidate_contains_location_and_source_id() -> None:
    candidates = detect_quote_candidates([_page("The observed visibility loss is caused by decoherence in the interferometer.")])

    assert candidates
    assert candidates[0].source_id == "SRC-TEST"
    assert candidates[0].page_number == 2
    assert candidates[0].location_type == "PAGE_TEXT"
    assert candidates[0].sha256 == "abc123"


def test_equation_candidate_requires_extracted_text() -> None:
    candidates = detect_equation_candidates([_page("The rate equation is Gamma = lambda times mass.")])

    assert candidates
    assert candidates[0].candidate_type == "EQUATION_CANDIDATE"
    assert candidates[0].extracted_text


def test_range_candidate_requires_units_or_numbers() -> None:
    candidates = detect_range_candidates([_page("The benchmark mass range was 10 amu to 100 amu with visibility 0.4.")])

    assert candidates
    assert candidates[0].candidate_type in {"PARAMETER_RANGE_CANDIDATE", "BENCHMARK_RANGE_CANDIDATE"}
    assert any(char.isdigit() for char in candidates[0].extracted_text)


def test_negative_candidate_requires_negative_keywords() -> None:
    candidates = detect_negative_candidates([_page("Thermal scattering dominates the background and the candidate effect is negligible.")])

    assert candidates
    assert candidates[0].candidate_type == "NEGATIVE_CONSTRAINT_CANDIDATE"
    assert candidates[0].requires_manual_review is True
