"""Strict y_true QC for v4.8."""

from __future__ import annotations

from phyng.phi_curvature_minimal_campaign.schemas import (
    PhiCurvatureAcceptedYTrue,
    PhiCurvatureCandidateObservable,
    PhiCurvatureRejectedYTrue,
    PhiCurvatureYTrueCandidate,
)


def build_ytrue_candidates(observables: list[PhiCurvatureCandidateObservable], source_hashes: dict[str, str | None] | None = None) -> list[PhiCurvatureYTrueCandidate]:
    source_hashes = source_hashes or {}
    candidates: list[PhiCurvatureYTrueCandidate] = []
    for index, observable in enumerate(observables, start=1):
        source_hash = source_hashes.get(observable.source_id)
        value = None
        provenance = "PROVENANCE_INCOMPLETE"
        qc_status = "FAIL"
        rejection = _rejection_reason(observable, value, source_hash)
        can_enter = rejection is None
        if can_enter:
            provenance = "PROVENANCE_COMPLETE"
            qc_status = "PASS"
        candidates.append(
            PhiCurvatureYTrueCandidate(
                candidate_id=f"PHICURV-YTRUE-CAND-v4_8-{index:03d}",
                observable_id=observable.observable_id,
                source_id=observable.source_id,
                source_hash=source_hash,
                observable_class=observable.observable_class,
                variable_name=observable.variable_name,
                value=value,
                unit=observable.expected_unit,
                source_location_type=observable.source_location_type,
                source_location_value=observable.source_location_value,
                extraction_method="MINIMAL_LOCAL_SOURCE_SCAN",
                provenance_status=provenance,
                qc_status=qc_status,
                matched_prediction_placeholder=True,
                can_enter_dataset=can_enter,
                rejection_reason=rejection,
            )
        )
    return candidates


def split_ytrue(candidates: list[PhiCurvatureYTrueCandidate]) -> tuple[list[PhiCurvatureAcceptedYTrue], list[PhiCurvatureRejectedYTrue]]:
    accepted: list[PhiCurvatureAcceptedYTrue] = []
    rejected: list[PhiCurvatureRejectedYTrue] = []
    for candidate in candidates:
        if candidate.can_enter_dataset and candidate.value is not None and candidate.unit and candidate.source_hash and candidate.source_location_type and candidate.source_location_value:
            accepted.append(
                PhiCurvatureAcceptedYTrue(
                    y_true_id=candidate.candidate_id.replace("CAND", "ACCEPTED"),
                    candidate_id=candidate.candidate_id,
                    observable_id=candidate.observable_id,
                    source_id=candidate.source_id,
                    source_hash=candidate.source_hash,
                    observable_class=candidate.observable_class,
                    variable_name=candidate.variable_name,
                    value=candidate.value,
                    unit=candidate.unit,
                    uncertainty=candidate.uncertainty,
                    source_location_type=candidate.source_location_type,
                    source_location_value=candidate.source_location_value,
                    extraction_method=candidate.extraction_method,
                    limitations=["Pre-benchmark y_true; matched prediction is placeholder only."],
                )
            )
        else:
            rejected.append(
                PhiCurvatureRejectedYTrue(
                    candidate_id=candidate.candidate_id,
                    observable_id=candidate.observable_id,
                    source_id=candidate.source_id,
                    rejection_reason=candidate.rejection_reason or "PROVENANCE_INCOMPLETE",
                    claim_impact="Does not permit PredictiveGain, physical validation, or empirical support claim.",
                    required_next_action=_next_action(candidate.rejection_reason),
                )
            )
    return accepted, rejected


def ytrue_candidate_passes_qc(candidate: PhiCurvatureYTrueCandidate, source_identity_resolved: bool = True) -> bool:
    if candidate.value is None:
        return False
    if candidate.unit is None and candidate.observable_class not in {"VISIBILITY", "CONTRAST_DECAY", "CURVATURE_PROXY", "BOUNDARY_RESPONSE"}:
        return False
    if not candidate.source_hash or not candidate.source_location_type or not candidate.source_location_value:
        return False
    return source_identity_resolved and candidate.provenance_status == "PROVENANCE_COMPLETE" and candidate.qc_status in {"PASS", "PASS_WITH_LIMITATIONS"}


def _rejection_reason(observable: PhiCurvatureCandidateObservable, value: float | None, source_hash: str | None) -> str | None:
    if "SOURCE_UNRESOLVED" in observable.blockers:
        return "SOURCE_UNRESOLVED"
    if "SOURCE_NOT_AVAILABLE" in observable.blockers:
        return "SOURCE_NOT_AVAILABLE"
    if value is None:
        return "NO_NUMERIC_VALUE"
    if observable.expected_unit is None:
        return "MISSING_UNIT"
    if not observable.source_location_type or not observable.source_location_value:
        return "MISSING_LOCATION"
    if not source_hash:
        return "MISSING_HASH"
    return None


def _next_action(reason: str | None) -> str:
    if reason in {"SOURCE_UNRESOLVED", "SOURCE_NOT_AVAILABLE"}:
        return "Resolve source identity and acquire local PDF/supplementary/public dataset."
    if reason == "NO_NUMERIC_VALUE":
        return "Perform human table/figure review on exact source object."
    return "Complete provenance fields before y_true acceptance."
