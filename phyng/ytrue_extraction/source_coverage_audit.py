"""Perform source-coverage audit on normalized targets."""

from __future__ import annotations

from pathlib import Path

from phyng.ytrue_extraction.schemas import SourceCoverageAuditRecord


def run_source_coverage_audit(
    targets: list[dict],
    source_hashes: dict,
    benchmark_rows: list[dict],
    root: Path = Path("."),
) -> list[SourceCoverageAuditRecord]:
    """Audit source coverage and provenance for all targets."""
    records: list[SourceCoverageAuditRecord] = []

    # Map source_id to hash record
    hash_map = {h["source_id"]: h for h in source_hashes.get("hashes", [])}

    # Map benchmark_id to row
    row_map = {r["benchmark_id"]: r for r in benchmark_rows}

    index = 1
    for t in targets:
        tid = t["target_id"]
        bid = t["benchmark_id"]
        sid = t["source_id"]
        eid = t["extract_id"]

        row = row_map.get(bid, {})
        hash_rec = hash_map.get(sid)

        # 1. Provenance checks
        hash_present = hash_rec is not None
        pdf_path = root / hash_rec["local_path"] if hash_rec else None
        local_pdf_present = pdf_path.exists() if pdf_path else False

        page_ref_present = row.get("page_number") is not None
        # We assume table/figure references from the text
        text_lower = t["source_observable_text"].lower()
        table_ref_present = "table" in text_lower
        figure_ref_present = "fig" in text_lower or "figure" in text_lower

        supp_present = "supplementary" in text_lower
        pub_ref_present = t["observable_class"] in (
            "MASS_REGIME",
            "TIME_REGIME",
            "SEPARATION_REGIME",
            "TEMPERATURE_PRESSURE_REGIME",
        )

        blockers = []
        if not hash_present:
            blockers.append("Source hash missing from manifest.")
        if not local_pdf_present and not pub_ref_present:
            blockers.append("Local source PDF file is missing.")
        if not page_ref_present and not pub_ref_present:
            blockers.append("Page reference missing from extraction record.")

        # Determine status
        if blockers:
            if not hash_present:
                status = "SOURCE_COVERAGE_BLOCKED_INSUFFICIENT_PROVENANCE"
                next_act = "Register source in hashes manifest."
            elif not local_pdf_present:
                status = "SOURCE_COVERAGE_BLOCKED_INSUFFICIENT_PROVENANCE"
                next_act = "Acquire and store local PDF copy."
            else:
                status = "SOURCE_COVERAGE_LOCAL_PDF_ONLY"
                next_act = "Identify page reference for this target."
        else:
            if pub_ref_present:
                status = "SOURCE_COVERAGE_NEEDS_PUBLIC_DATA"
                next_act = "Perform public database search."
            elif table_ref_present:
                status = "SOURCE_COVERAGE_NEEDS_TABLE_REVIEW"
                next_act = "Review table for quantitative values."
            elif figure_ref_present:
                status = "SOURCE_COVERAGE_NEEDS_FIGURE_DIGITIZATION"
                next_act = "Digitize figure to extract data points."
            elif supp_present:
                status = "SOURCE_COVERAGE_NEEDS_SUPPLEMENTARY"
                next_act = "Acquire supplementary files."
            elif page_ref_present:
                # Complete if page ref is present and hash/pdf exists
                status = "SOURCE_COVERAGE_COMPLETE"
                next_act = "Ready for data extraction."
            else:
                status = "SOURCE_COVERAGE_LOCAL_PDF_ONLY"
                next_act = "Identify exact location details."

        records.append(
            SourceCoverageAuditRecord(
                audit_id=f"AUD-v4_3-{index:03d}",
                target_id=tid,
                benchmark_id=bid,
                source_id=sid,
                extract_id=eid,
                source_hash_present=hash_present,
                local_pdf_present=local_pdf_present,
                supplementary_present=supp_present,
                public_dataset_reference_present=pub_ref_present,
                page_reference_present=page_ref_present,
                table_reference_present=table_ref_present,
                figure_reference_present=figure_ref_present,
                source_coverage_status=status,
                blockers=blockers,
                next_action=next_act,
            )
        )
        index += 1

    return records
