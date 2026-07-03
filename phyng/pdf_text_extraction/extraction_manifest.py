"""Build and write v3.7 extraction manifests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.pdf_text_extraction.schemas import (
    ExtractedPageText,
    PDFExtractionCandidate,
    PDFExtractionCandidateSet,
    PDFExtractionManifest,
    RegisteredPDFSource,
    SourceExtractionSummary,
)
from phyng.pdf_text_extraction.pdf_reader import pdf_reader_availability


OUTPUT_PATHS = {
    "text_extraction": Path("data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json"),
    "quote_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json"),
    "equation_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json"),
    "table_range_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json"),
    "negative_constraint_candidates": Path("data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json"),
    "manifest": Path("data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json"),
}


def build_extraction_manifest(
    input_registry_id: str | None,
    sources: list[RegisteredPDFSource],
    pages: list[ExtractedPageText],
    summaries: list[SourceExtractionSummary],
    quote_candidates: list[PDFExtractionCandidate],
    equation_candidates: list[PDFExtractionCandidate],
    table_range_candidates: list[PDFExtractionCandidate],
    negative_candidates: list[PDFExtractionCandidate],
    blocked_reason: str | None = None,
) -> PDFExtractionManifest:
    all_candidates = quote_candidates + equation_candidates + table_range_candidates + negative_candidates
    extracted_sources = {page.source_id for page in pages}
    manual_review_count = sum(1 for candidate in all_candidates if candidate.requires_manual_review) + sum(1 for item in summaries if item.requires_manual_review)
    if blocked_reason:
        status = blocked_reason
    elif not sources:
        status = "PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_NO_HASHED_FILES"
    elif not pages:
        status = "PHI_GRADIENT_PDF_EXTRACTION_REQUIRES_MANUAL_REVIEW"
    elif not all_candidates:
        status = "PHI_GRADIENT_PDF_EXTRACTION_NO_TEXT_FOUND"
    elif len(extracted_sources) < len(sources):
        status = "PHI_GRADIENT_PDF_EXTRACTION_PARTIAL"
    else:
        status = "PHI_GRADIENT_PDF_EXTRACTION_COMPLETED"
    return PDFExtractionManifest(
        input_registry_id=input_registry_id,
        reader_availability=pdf_reader_availability(),
        hashed_sources_seen=len(sources),
        sources_extracted=len(extracted_sources),
        sources_blocked=len(sources) - len(extracted_sources),
        total_pages_extracted=len(pages),
        total_candidates=len(all_candidates),
        quote_candidate_count=len(quote_candidates),
        equation_candidate_count=len(equation_candidates),
        table_range_candidate_count=len(table_range_candidates),
        negative_candidate_count=len(negative_candidates),
        manual_review_count=manual_review_count,
        status=status,
        source_summaries=summaries,
        notes=["Extraction candidates require review and validation before source pressure."],
    )


def write_extraction_outputs(
    root: str | Path,
    manifest: PDFExtractionManifest,
    pages: list[ExtractedPageText],
    quote_candidates: list[PDFExtractionCandidate],
    equation_candidates: list[PDFExtractionCandidate],
    table_range_candidates: list[PDFExtractionCandidate],
    negative_candidates: list[PDFExtractionCandidate],
) -> dict[str, str]:
    repo_root = Path(root)
    output_paths = {key: repo_root / path for key, path in OUTPUT_PATHS.items()}
    output_paths["manifest"].parent.mkdir(parents=True, exist_ok=True)
    _write_json(output_paths["manifest"], manifest.model_dump(mode="json"))
    _write_json(
        output_paths["text_extraction"],
        {
            "manifest_id": "PHI-GRADIENT-PDF-TEXT-EXTRACTION-v3_7",
            "pages": [page.model_dump(mode="json") for page in pages],
            "manifest": manifest.model_dump(mode="json"),
        },
    )
    _write_json(output_paths["quote_candidates"], PDFExtractionCandidateSet(manifest_id="PHI-GRADIENT-PDF-QUOTE-CANDIDATES-v3_7", candidates=quote_candidates).model_dump(mode="json"))
    _write_json(output_paths["equation_candidates"], PDFExtractionCandidateSet(manifest_id="PHI-GRADIENT-PDF-EQUATION-CANDIDATES-v3_7", candidates=equation_candidates).model_dump(mode="json"))
    _write_json(output_paths["table_range_candidates"], PDFExtractionCandidateSet(manifest_id="PHI-GRADIENT-PDF-TABLE-RANGE-CANDIDATES-v3_7", candidates=table_range_candidates).model_dump(mode="json"))
    _write_json(output_paths["negative_constraint_candidates"], PDFExtractionCandidateSet(manifest_id="PHI-GRADIENT-PDF-NEGATIVE-CONSTRAINT-CANDIDATES-v3_7", candidates=negative_candidates).model_dump(mode="json"))
    return {key: str(path.relative_to(repo_root)) for key, path in output_paths.items()}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
