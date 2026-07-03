"""Extract data candidates from normalized targets."""

from __future__ import annotations

import re
from phyng.ytrue_extraction.schemas import YTrueExtractionCandidate


def extract_candidates(targets: list[dict]) -> list[YTrueExtractionCandidate]:
    """Scan targets and extract potential y_true candidates."""
    candidates: list[YTrueExtractionCandidate] = []

    index = 1
    for t in targets:
        tid = t["target_id"]
        c = t["observable_class"]
        sid = t["source_id"]
        eid = t["extract_id"]
        text = t["source_observable_text"]

        numeric_val = _find_numeric(text)
        unit = t.get("unit")

        blockers = []
        is_outcome = c in ("DECOHERENCE_RATE", "VISIBILITY", "COHERENCE_LOSS", "CONTRAST_DECAY")

        if not is_outcome:
            blockers.append("Parameter constraints, limitation flags, and regimes are not observed outcomes.")
        if numeric_val is None:
            blockers.append("No explicit numeric value found in extract text.")
        if is_outcome and numeric_val is None:
            blockers.append("Target requires manual table review or figure digitization.")

        can_enter = len(blockers) == 0

        candidates.append(
            YTrueExtractionCandidate(
                candidate_id=f"CAN-v4_3-{index:03d}",
                target_id=tid,
                observable_class=c,
                source_id=sid,
                extract_id=eid,
                candidate_value_text=text,
                numeric_value=numeric_val,
                unit=unit,
                uncertainty=None,
                extraction_method="AUTOMATIC_TEXT_SCAN" if numeric_val is not None else "BLOCKED",
                source_location="prose text",
                provenance_status="INCOMPLETE" if not can_enter else "COMPLETE",
                qc_status="FAIL_NO_NUMERIC_VALUE" if numeric_val is None else ("FAIL_CONSTRAINT_ONLY" if not is_outcome else "PASS"),
                can_enter_dataset=can_enter,
                blockers=blockers,
            )
        )
        index += 1

    return candidates


def _find_numeric(text: str) -> float | None:
    # Replace unicode minus and times characters
    clean_text = text.replace("−", "-").replace("×", "x").replace("≤", "<=")
    # Regex to match float or int
    matches = re.findall(r'-?\d+(?:\.\d+)?', clean_text)
    if matches:
        for m in matches:
            val = float(m)
            # Avoid matching year or small indices
            if 1990 <= val <= 2030:
                continue
            return val
    return None
