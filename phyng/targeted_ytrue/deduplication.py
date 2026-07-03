"""Deduplication for v5.7.3 targeted y_true records."""

from __future__ import annotations

import json

from phyng.targeted_ytrue.schemas import AcceptedTargetedYTrue, RejectedTargetedYTrue, TargetedYTrueCandidate, YTrueAuditRecord


def existing_keys(existing_records: list[dict]) -> set[str]:
    keys: set[str] = set()
    for record in existing_records:
        source_id = str(record.get("source_id"))
        page = str(record.get("page_number"))
        location = str(record.get("figure_id") or record.get("location_label") or record.get("section_id"))
        observable = str(record.get("observable_class"))
        variable = str(record.get("variable_name"))
        value = str(record.get("value", record.get("value_numeric")))
        conditions = {
            record.get("experimental_condition_name"): record.get("experimental_condition_value")
        } if record.get("experimental_condition_name") else record.get("conditions", {})
        keys.add(_key(source_id, page, location, observable, variable, value, conditions))
    return keys


def accept_with_dedup(candidates: list[TargetedYTrueCandidate], existing: list[dict], audit: list[YTrueAuditRecord]) -> tuple[list[AcceptedTargetedYTrue], list[RejectedTargetedYTrue]]:
    keys = existing_keys(existing)
    accepted: list[AcceptedTargetedYTrue] = []
    rejected: list[RejectedTargetedYTrue] = []
    for candidate in candidates:
        if candidate.qc_status not in {"PASS", "PASS_WITH_LIMITATIONS"} or candidate.rejection_reason:
            continue
        key = _key(
            candidate.source_id,
            str(candidate.page_number),
            candidate.location_label,
            candidate.observable_class,
            candidate.variable_name,
            str(candidate.numeric_value),
            candidate.conditions,
        )
        semantic_key = _key(candidate.source_id, str(candidate.page_number), candidate.location_label, "VISIBILITY_EQUIVALENT", candidate.variable_name, str(candidate.numeric_value), candidate.conditions)
        if key in keys or semantic_key in keys:
            rejected.append(
                RejectedTargetedYTrue(
                    ytrue_candidate_id=candidate.ytrue_candidate_id,
                    input_location_id=candidate.input_location_id,
                    source_id=candidate.source_id,
                    rejection_reason="DUPLICATE_YTRUE",
                    qc_status="REJECT",
                    notes=["Duplicate within existing or current accepted y_true set."],
                )
            )
            _mark_duplicate(audit, candidate.ytrue_candidate_id)
            continue
        keys.add(key)
        keys.add(semantic_key)
        accepted.append(_accepted_from_candidate(candidate, len(accepted) + 1))
    return accepted, rejected


def _accepted_from_candidate(candidate: TargetedYTrueCandidate, index: int) -> AcceptedTargetedYTrue:
    authors = candidate.source_identity.get("authors") or []
    authority = "; ".join(authors) if authors else candidate.source_title
    return AcceptedTargetedYTrue(
        y_true_id=f"YTRUE-v5_7_3-TARGETED-{index:03d}",
        source_id=candidate.source_id,
        source_title=candidate.source_title,
        source_authors_or_authority=authority,
        source_year=int(candidate.source_year or 0),
        source_doi_or_arxiv_or_url=str(candidate.source_identity.get("external_identity")),
        local_pdf_path=candidate.local_pdf_path,
        local_pdf_hash=candidate.local_pdf_hash,
        page_number=int(candidate.page_number or 0),
        location_label=candidate.location_label,
        observable_class=candidate.observable_class,
        variable_name=candidate.variable_name,
        value_numeric=float(candidate.numeric_value or 0.0),
        original_value_text=str(candidate.original_value_text),
        unit=str(candidate.unit),
        normalized_unit=str(candidate.normalized_unit),
        conditions=candidate.conditions,
        extraction_method=candidate.extraction_method,
        provenance_status=candidate.provenance_status,
        qc_status=candidate.qc_status,
        limitations=candidate.limitations,
    )


def _key(source_id: str, page: str, location: str, observable: str, variable: str, value: str, conditions: dict) -> str:
    return "|".join([source_id, page, location, observable, variable, value, json.dumps(conditions, sort_keys=True)])


def _mark_duplicate(audit: list[YTrueAuditRecord], candidate_id: str) -> None:
    for record in audit:
        if record.candidate_id == candidate_id:
            record.decision = "REJECT"
            record.decision_reason = "DUPLICATE_YTRUE"
            record.deduplication_actions.append("Rejected duplicate y_true key.")
