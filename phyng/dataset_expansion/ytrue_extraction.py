"""Strict y_true extraction for v5.7 expansion."""

from __future__ import annotations

from phyng.dataset_expansion.schemas import ObservableLocationCandidate, SourcePoolRecord, YTrueCandidate


def build_ytrue_candidates(
    locations: list[ObservableLocationCandidate],
    source_pool: list[SourcePoolRecord],
    prior_accepted: list[dict],
) -> list[YTrueCandidate]:
    source_by_id = {source.source_id: source for source in source_pool}
    candidates: list[YTrueCandidate] = []
    for prior in prior_accepted:
        candidates.append(
            YTrueCandidate(
                ytrue_candidate_id=prior["y_true_id"].replace("YTRUE-v5_3", "YTRUE-CAND-v5_7"),
                source_id=prior["source_id"],
                source_title=prior["source_title"],
                source_year=prior["source_year"],
                external_identity=prior["source_doi_or_arxiv_or_url"],
                local_pdf_path=prior["local_pdf_path"],
                local_pdf_hash=prior["local_pdf_hash"],
                page_number=prior["page_number"],
                location_label=prior["figure_id"],
                observable_class=prior["observable_class"],
                variable_name=prior["variable_name"],
                value_numeric=prior["value"],
                original_value_text=prior["original_value_text"],
                unit=prior["unit"],
                conditions={prior["experimental_condition_name"]: prior["experimental_condition_value"], "unit": prior["experimental_condition_unit"]},
                extraction_method="carried forward from v5.3 strict accepted y_true",
                provenance_status=prior["provenance_status"],
                qc_status=prior["qc_status"],
                limitations=list(prior.get("limitations", [])) + ["v5.7 dataset expansion did not create candidate rescue."],
            )
        )
    for location in locations:
        if location.classification == "OBSERVED_MEASUREMENT_CANDIDATE":
            continue
        source = source_by_id[location.source_id]
        candidates.append(
            YTrueCandidate(
                ytrue_candidate_id=f"YTRUE-CAND-v5_7-REJECT-{location.location_id}",
                source_id=location.source_id,
                source_title=source.title,
                source_year=source.year,
                external_identity=source.external_identity,
                local_pdf_path=location.local_pdf_path,
                local_pdf_hash=location.local_pdf_hash,
                page_number=location.page_number,
                location_label=location.figure_id or location.table_id or location.equation_id or location.section_id or "UNKNOWN",
                observable_class=location.observable_class,
                variable_name=location.variable_name or "unknown",
                value_numeric=None,
                original_value_text=location.numeric_value_text or "",
                unit=location.unit_text,
                conditions={"condition_text": location.condition_text},
                extraction_method="v5.7 location scan rejection",
                provenance_status="LOCAL_SOURCE_WITH_LOCATION_BUT_NO_ACCEPTED_YTRUE",
                qc_status="REQUIRES_FIGURE_REVIEW" if "REQUIRES_VISUAL_REVIEW" in location.extraction_blockers or "REQUIRES_VISUAL_FIGURE_REVIEW" in location.extraction_blockers else "REJECT",
                limitations=list(location.extraction_blockers),
            )
        )
    return candidates


def split_accepted_rejected(candidates: list[YTrueCandidate]) -> tuple[list[YTrueCandidate], list[YTrueCandidate]]:
    accepted = [item for item in candidates if item.qc_status in {"PASS", "PASS_WITH_LIMITATIONS"} and item.value_numeric is not None]
    rejected = [item for item in candidates if item not in accepted]
    return accepted, rejected
