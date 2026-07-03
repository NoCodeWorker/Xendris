"""Manual table-review rules for v4.4 y_true extraction."""

from __future__ import annotations

import re
from pathlib import Path

from phyng.manual_data_extraction.schemas import ManualExtractionReviewRecord


DIMENSIONAL_CLASSES = {"DECOHERENCE_RATE", "CONTRAST_DECAY"}
ACCEPTABLE_CLASSES = {"VISIBILITY", "DECOHERENCE_RATE", "CONTRAST_DECAY", "COHERENCE_LOSS"}
NON_YTRUE_CLASSES = {"PARAMETER_BOUND", "LIMITATION_FLAG"}


def review_queue_item(
    item: dict,
    index: int,
    target_by_id: dict[str, dict],
    hash_by_source: dict[str, dict],
    extracted_value_text: str | None = None,
) -> ManualExtractionReviewRecord:
    target = target_by_id.get(item.get("target_id"), {})
    source_id = item.get("source_id", "")
    source_hash_record = hash_by_source.get(source_id, {})
    source_hash = source_hash_record.get("sha256")
    local_pdf_path = source_hash_record.get("local_path")
    text = extracted_value_text if extracted_value_text is not None else target.get("source_observable_text") or item.get("expected_measurement") or ""
    page_number, table_number, figure_number = _parse_location(item.get("source_location_hint", ""))
    numeric_value, unit = _parse_value_and_unit(text, item.get("observable_class", ""))
    blockers: list[str] = []
    notes = ["Manual extraction review is not permission to lower y_true standards."]
    decision = "ACCEPT_AS_YTRUE"
    qc_status = "PASS"

    if not source_hash:
        blockers.append("MISSING_SOURCE_HASH")
        decision = "SEND_TO_HUMAN_REVIEW"
        qc_status = "FAIL_MISSING_SOURCE_HASH"
    elif item.get("observable_class") in NON_YTRUE_CLASSES:
        blockers.append("NOT_OBSERVED_YTRUE")
        decision = "REJECT_CONSTRAINT_NOT_YTRUE" if item.get("observable_class") == "PARAMETER_BOUND" else "REJECT_LIMITATION_NOT_YTRUE"
        qc_status = "FAIL_NOT_YTRUE"
    elif page_number is None and table_number is None and figure_number is None:
        blockers.append("MISSING_SOURCE_LOCATION")
        decision = "REJECT_MISSING_LOCATION"
        qc_status = "FAIL_MISSING_LOCATION"
    elif item.get("observable_class") not in ACCEPTABLE_CLASSES:
        blockers.append("UNSUPPORTED_OBSERVABLE_CLASS")
        decision = "SEND_TO_HUMAN_REVIEW"
        qc_status = "FAIL_UNSUPPORTED_OBSERVABLE_CLASS"
    elif numeric_value is None:
        blockers.append("NO_NUMERIC_VALUE")
        decision = "REJECT_PROSE_ONLY" if _looks_prose_only(text) else "REJECT_NO_NUMERIC_VALUE"
        qc_status = "FAIL_NO_NUMERIC_VALUE"
    elif item.get("observable_class") in DIMENSIONAL_CLASSES and not unit:
        blockers.append("MISSING_UNIT")
        decision = "REJECT_MISSING_UNIT"
        qc_status = "FAIL_MISSING_UNIT"
    elif item.get("observable_class") == "VISIBILITY" and not (0 <= numeric_value <= 1):
        blockers.append("VISIBILITY_OUT_OF_RANGE")
        decision = "REJECT_NO_NUMERIC_VALUE"
        qc_status = "FAIL_QC_RANGE"
    elif item.get("observable_class") == "DECOHERENCE_RATE" and numeric_value < 0:
        blockers.append("NEGATIVE_RATE")
        decision = "REJECT_NO_NUMERIC_VALUE"
        qc_status = "FAIL_QC_RANGE"

    unit = unit or ("dimensionless" if item.get("observable_class") in {"VISIBILITY", "COHERENCE_LOSS"} and numeric_value is not None else None)
    return ManualExtractionReviewRecord(
        review_id=f"MANUAL-REVIEW-v4_4-{index:03d}",
        queue_item_id=f"MANUAL-QUEUE-v4_3-{index:03d}",
        target_id=item.get("target_id", ""),
        benchmark_id=target.get("benchmark_id", ""),
        source_id=source_id,
        source_hash=source_hash,
        observable_class=item.get("observable_class", ""),
        expected_measurement=item.get("expected_measurement", ""),
        local_pdf_path=local_pdf_path,
        page_number=page_number,
        table_number=table_number,
        figure_number=figure_number,
        extracted_value_text=text,
        numeric_value=numeric_value,
        unit=unit,
        uncertainty=None,
        extraction_method="MANUAL_TABLE_EXTRACTION",
        reviewer_decision=decision,
        qc_status=qc_status,
        blockers=blockers,
        notes=notes,
    )


def can_accept(review: ManualExtractionReviewRecord) -> bool:
    return (
        review.reviewer_decision == "ACCEPT_AS_YTRUE"
        and review.qc_status in {"PASS", "PASS_WITH_LIMITATIONS"}
        and bool(review.source_hash)
        and bool(review.benchmark_id)
        and bool(review.target_id)
        and review.numeric_value is not None
        and bool(review.unit)
        and (review.page_number is not None or review.table_number is not None or review.figure_number is not None)
    )


def _parse_location(hint: str) -> tuple[int | None, str | None, str | None]:
    lowered = hint.lower()
    page_match = re.search(r"page\s*(\d+)", lowered)
    table_match = re.search(r"table\s*([a-z0-9.\-]+)", lowered)
    figure_match = re.search(r"(?:fig\.?|figure)\s*([a-z0-9.\-]+)", lowered)
    if "unknown" in lowered:
        return None, None, None
    return (
        int(page_match.group(1)) if page_match else None,
        table_match.group(1) if table_match else None,
        figure_match.group(1) if figure_match else None,
    )


def _parse_value_and_unit(text: str, observable_class: str) -> tuple[float | None, str | None]:
    normalized = text.replace("−", "-").replace("×", "x")
    match = re.search(r"([-+]?\d+(?:\.\d+)?(?:\s*x\s*10\^?[-+]?\d+)?)\s*([a-zA-Z/%^\-0-9]+)?", normalized)
    if not match:
        return None, None
    value = _parse_float(match.group(1))
    unit = match.group(2)
    if observable_class == "VISIBILITY" and unit is None:
        unit = "dimensionless"
    return value, unit


def _parse_float(raw: str) -> float | None:
    try:
        if "x 10" in raw:
            base, exp = re.split(r"\s*x\s*10\^?", raw)
            return float(base) * (10 ** int(exp))
        return float(raw)
    except Exception:
        return None


def _looks_prose_only(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in ["halve", "reduce", "enhance", "suppress", "visibility", "decoherence"]) and re.search(r"\d", text) is None


def location_value(review: ManualExtractionReviewRecord) -> str:
    parts = []
    if review.page_number is not None:
        parts.append(f"page={review.page_number}")
    if review.table_number:
        parts.append(f"table={review.table_number}")
    if review.figure_number:
        parts.append(f"figure={review.figure_number}")
    return "; ".join(parts)


def local_path_name(path: str | None) -> str | None:
    return Path(path).name if path else None
