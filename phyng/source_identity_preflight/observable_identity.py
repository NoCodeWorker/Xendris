"""Observable identity matrix for v4.9."""

from __future__ import annotations

from phyng.source_identity_preflight.schemas import ObservableIdentityRecord, SourceIdentityResolutionRecord


FAMILY_OBSERVABLES = {
    "PHI_CURVATURE": [("CURVATURE_PROXY", "curvature_coefficient"), ("DECOHERENCE_RATE", "phase_decay_rate")],
    "PHI_LOCALIZED_WINDOW": [("LOCALIZATION_WIDTH", "window_width")],
    "PHI_BANDPASS": [("BANDPASS_RESPONSE", "bandpass_response")],
    "PHI_GRADIENT": [("PARAMETER_BOUND", "gradient_component_bound")],
    "B_SUPPRESSED": [("BOUNDARY_RESPONSE", "boundary_suppression")],
    "QB_STRUCTURAL": [("PARAMETER_BOUND", "structural_qb_parameter")],
    "LOG_BOUNDARY": [("BOUNDARY_RESPONSE", "log_boundary_response")],
    "THRESHOLD_SATURATION": [("PARAMETER_BOUND", "threshold_saturation")],
}


def build_observable_identity_matrix(identity_matrix: list[SourceIdentityResolutionRecord]) -> list[ObservableIdentityRecord]:
    records: list[ObservableIdentityRecord] = []
    seen_families = {record.family_id for record in identity_matrix}
    for family in sorted(seen_families):
        identities = [record for record in identity_matrix if record.family_id == family]
        source_id = next((record.source_id for record in identities if record.identity_complete), None)
        identity_complete = any(record.identity_complete for record in identities)
        for observable_class, name in FAMILY_OBSERVABLES.get(family, [("UNKNOWN", "unknown")]):
            records.append(_observable_record(family, source_id, observable_class, name, identity_complete))
    return records


def _observable_record(
    family: str,
    source_id: str | None,
    observable_class: str,
    name: str,
    identity_complete: bool,
) -> ObservableIdentityRecord:
    if not identity_complete:
        return ObservableIdentityRecord(
            family_id=family,
            source_id=source_id,
            observable_class=observable_class,
            observable_name=name,
            expected_unit=_expected_unit(observable_class),
            numeric_value_expected=_numeric_expected(observable_class),
            observable_status="SOURCE_NOT_LOCATABLE",
            blockers=["SOURCE_IDENTITY_INCOMPLETE"],
        )
    return ObservableIdentityRecord(
        family_id=family,
        source_id=source_id,
        observable_class=observable_class,
        observable_name=name,
        source_locatable=True,
        expected_location_type="page_or_table",
        expected_unit=_expected_unit(observable_class),
        numeric_value_expected=_numeric_expected(observable_class),
        observable_status="SOURCE_LOCATABLE",
    )


def _expected_unit(observable_class: str) -> str | None:
    return {
        "VISIBILITY": "dimensionless",
        "CONTRAST_DECAY": "dimensionless",
        "DECOHERENCE_RATE": "s^-1",
        "PHASE_DECAY_RATE": "s^-1",
        "PHASE_SHIFT": "rad",
        "CURVATURE_PROXY": "dimensionless",
        "LOCALIZATION_WIDTH": "m",
        "BANDPASS_RESPONSE": "dimensionless",
        "BOUNDARY_RESPONSE": "dimensionless",
        "NOISE_SPECTRUM": "Hz^-1",
        "PARAMETER_BOUND": "dimensionless",
    }.get(observable_class)


def _numeric_expected(observable_class: str) -> bool:
    return observable_class != "UNKNOWN"
