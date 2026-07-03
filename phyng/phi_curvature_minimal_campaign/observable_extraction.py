"""Candidate observable extraction for v4.8."""

from __future__ import annotations

from phyng.phi_curvature_minimal_campaign.schemas import (
    PhiCurvatureCandidateObservable,
    SourceAvailabilityRecord,
    SourceResolutionRecord,
)


ALLOWED_CLASSES = {
    "CURVATURE_PROXY",
    "DECOHERENCE_RATE",
    "PHASE_DECAY_RATE",
    "VISIBILITY",
    "CONTRAST_DECAY",
    "PHASE_SHIFT",
    "NOISE_SPECTRUM",
    "BOUNDARY_RESPONSE",
}


def extract_candidate_observables(
    resolutions: list[SourceResolutionRecord],
    availability: list[SourceAvailabilityRecord],
    observable_screen: dict,
) -> list[PhiCurvatureCandidateObservable]:
    availability_by_source = {record.source_id: record for record in availability}
    observable_classes = [cls for cls in observable_screen.get("observable_classes", []) if cls in ALLOWED_CLASSES]
    variable_names = observable_screen.get("proposed_observables", []) or ["phi_curvature_observable"]
    observables: list[PhiCurvatureCandidateObservable] = []
    index = 1
    for source in resolutions:
        source_id = source.source_id or "UNRESOLVED_SOURCE"
        availability_record = availability_by_source.get(source_id)
        for cls in observable_classes:
            variable = variable_names[min(len(variable_names) - 1, observable_classes.index(cls) if cls in observable_classes else 0)]
            blockers = []
            extraction_status = "NO_NUMERIC_VALUE"
            if source.resolution_status not in {"RESOLVED_EXACT", "RESOLVED_PROBABLE"}:
                extraction_status = "SOURCE_NOT_EXTRACTION_READY"
                blockers.append("SOURCE_UNRESOLVED")
            elif not availability_record or not availability_record.local_pdf_available:
                extraction_status = "SOURCE_NOT_AVAILABLE"
                blockers.append("SOURCE_NOT_AVAILABLE")
            observables.append(
                PhiCurvatureCandidateObservable(
                    observable_id=f"PHICURV-OBS-v4_8-{index:03d}",
                    source_id=source_id,
                    observable_class=cls,
                    variable_name=variable,
                    expected_unit=_expected_unit(cls),
                    candidate_text=None,
                    numeric_candidate_present=False,
                    extraction_status=extraction_status,
                    blockers=blockers or ["NO_NUMERIC_VALUE"],
                )
            )
            index += 1
    return observables


def _expected_unit(observable_class: str) -> str | None:
    if observable_class in {"VISIBILITY", "CONTRAST_DECAY", "CURVATURE_PROXY", "BOUNDARY_RESPONSE"}:
        return "dimensionless"
    if observable_class in {"DECOHERENCE_RATE", "PHASE_DECAY_RATE"}:
        return "s^-1"
    if observable_class == "PHASE_SHIFT":
        return "rad"
    if observable_class == "NOISE_SPECTRUM":
        return "Hz^-1"
    return None
