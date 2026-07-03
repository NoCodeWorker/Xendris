"""Build v5.7.3 y_true candidates from v5.7.2 observed locations."""

from __future__ import annotations

from phyng.targeted_ytrue.qc import evaluate_candidate
from phyng.targeted_ytrue.schemas import RejectedTargetedYTrue, TargetedYTrueCandidate, YTrueAuditRecord
from phyng.targeted_ytrue.unit_normalization import extract_conditions, normalize_visibility_value


def build_candidates(inputs: dict) -> tuple[list[TargetedYTrueCandidate], list[RejectedTargetedYTrue], list[YTrueAuditRecord]]:
    manifest_by_source = {item["source_candidate_id"]: item for item in inputs["source_manifest"]}
    candidates: list[TargetedYTrueCandidate] = []
    rejected: list[RejectedTargetedYTrue] = []
    audit: list[YTrueAuditRecord] = []
    for index, observed in enumerate(inputs["observed"], start=1):
        source = manifest_by_source.get(observed["source_candidate_id"], {})
        value, original_text, unit, normalization = normalize_visibility_value(observed.get("numeric_value_text"), observed.get("snippet", ""))
        conditions, condition_actions = extract_conditions(observed.get("condition_text"), observed.get("snippet", ""))
        location_label = _location_label(observed)
        limitations = [
            "Accepted y_true records do not validate Frontera C or any physical claim.",
            "Extraction is from PDF text stream, not independent visual digitization.",
        ]
        if "predicted" in observed.get("snippet", "").lower() and "interference contrast of" not in observed.get("snippet", "").lower():
            limitations.append("model-only context detected")
        candidate = TargetedYTrueCandidate(
            ytrue_candidate_id=f"YTRUE-CAND-v5_7_3-{index:03d}",
            input_location_id=observed["location_id"],
            source_id=observed["source_id"],
            source_title=source.get("title") or observed["source_id"],
            source_year=source.get("year"),
            source_identity={
                "authors": source.get("authors", []),
                "external_identity": source.get("external_identity"),
                "identity_complete": bool(source.get("source_identity_complete")),
            },
            local_pdf_path=observed.get("local_pdf_path") or "",
            local_pdf_hash=observed.get("local_pdf_hash") or "",
            page_number=observed.get("page_number"),
            location_label=location_label,
            observable_class=observed.get("observable_class") or "",
            variable_name=observed.get("variable_name") or "visibility_fraction",
            numeric_value=value,
            original_value_text=original_text,
            unit=unit,
            normalized_unit=unit,
            conditions=conditions,
            extraction_method="v5.7.3 strict extraction from v5.7.2 source-located PDF text candidate",
            provenance_status="LOCAL_HASHED_PDF_WITH_SOURCE_IDENTITY_AND_TEXT_LOCATION",
            qc_status="REJECT",
            limitations=limitations,
        )
        qc_status, reason, checks_passed, checks_failed = evaluate_candidate(candidate)
        candidate.qc_status = qc_status
        candidate.rejection_reason = reason
        candidates.append(candidate)
        decision = "ACCEPT_CANDIDATE_FOR_DEDUP" if reason is None else "REJECT"
        if reason is not None:
            rejected.append(
                RejectedTargetedYTrue(
                    ytrue_candidate_id=candidate.ytrue_candidate_id,
                    input_location_id=candidate.input_location_id,
                    source_id=candidate.source_id,
                    rejection_reason=reason,
                    qc_status=qc_status,
                    notes=candidate.limitations,
                )
            )
        audit.append(
            YTrueAuditRecord(
                candidate_id=candidate.ytrue_candidate_id,
                input_location_id=candidate.input_location_id,
                source_id=candidate.source_id,
                decision=decision,
                decision_reason=reason or "QC_PASS_WITH_LIMITATIONS",
                checks_passed=checks_passed,
                checks_failed=checks_failed,
                normalization_actions=normalization + condition_actions,
                reviewer_notes=candidate.limitations,
            )
        )
    return candidates, rejected, audit


def _location_label(observed: dict) -> str:
    if observed.get("figure_id"):
        return observed["figure_id"]
    if observed.get("table_id"):
        return observed["table_id"]
    if observed.get("section_id"):
        return observed["section_id"]
    return f"PAGE_{observed.get('page_number')}"
