"""Table review logic for Track A."""

from __future__ import annotations

from pathlib import Path
from phyng.external_evidence.schemas import TableReviewResult


def run_table_review(inputs: dict, root: str | Path = ".") -> list[TableReviewResult]:
    root_path = Path(root)
    review_records = inputs.get("manual_extraction_review_records_v4_4", {}).get("review_records", [])
    hashes = inputs.get("source_hashes_v3_6", {}).get("hashes", [])
    hash_by_source = {h["source_id"]: h for h in hashes}

    results: list[TableReviewResult] = []
    for idx, item in enumerate(review_records, start=1):
        target_id = item.get("target_id", "")
        source_id = item.get("source_id", "")
        observable_class = item.get("observable_class", "")

        # Find PDF path
        pdf_info = hash_by_source.get(source_id)
        local_pdf_path = None
        pdf_exists = False
        if pdf_info:
            rel_pdf = pdf_info.get("local_path", "")
            abs_pdf = root_path / rel_pdf
            local_pdf_path = str(rel_pdf)
            pdf_exists = abs_pdf.exists()

        # Check location
        page_number = item.get("page_number")
        table_number = item.get("table_number")
        figure_number = item.get("figure_number")

        blockers = []
        evidence_status = "TABLE_VALUE_FOUND"
        next_action = "None"

        if not pdf_exists:
            evidence_status = "PDF_NOT_AVAILABLE"
            blockers.append("PDF_NOT_AVAILABLE")
            next_action = "Acquire local PDF file."
        elif page_number is None and table_number is None and figure_number is None:
            evidence_status = "PAGE_LOCATION_MISSING"
            blockers.append("PAGE_LOCATION_MISSING")
            next_action = "Locate exact page/table/figure before accepting y_true."
        elif table_number is None:
            evidence_status = "TABLE_NOT_FOUND"
            blockers.append("TABLE_NOT_FOUND")
            next_action = "Locate exact table/figure within PDF."
        
        # If it was rejected or has non y-true class
        if observable_class in {"PARAMETER_BOUND", "LIMITATION_FLAG"}:
            evidence_status = "VALUE_AMBIGUOUS"
            blockers.append("NOT_OBSERVED_YTRUE")
            next_action = "Keep as constraint, not observed y_true."

        results.append(
            TableReviewResult(
                review_id=f"TABLE-REVIEW-v4_5-{idx:03d}",
                target_id=target_id,
                source_id=source_id,
                local_pdf_path=local_pdf_path,
                page_number=page_number,
                table_number=table_number,
                candidate_value_text=item.get("extracted_value_text"),
                numeric_value=item.get("numeric_value"),
                unit=item.get("unit"),
                uncertainty=item.get("uncertainty"),
                evidence_status=evidence_status,
                blockers=blockers,
                next_action=next_action,
            )
        )
    return results
