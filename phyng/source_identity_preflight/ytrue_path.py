"""y_true path plausibility matrix for v4.9."""

from __future__ import annotations

from phyng.source_identity_preflight.schemas import ObservableIdentityRecord, SourceAvailabilityMatrixRecord, YTruePathPlausibilityRecord


def build_ytrue_path_plausibility_matrix(
    observables: list[ObservableIdentityRecord],
    availability: list[SourceAvailabilityMatrixRecord],
) -> list[YTruePathPlausibilityRecord]:
    availability_by_family = {record.family_id: record for record in availability}
    records: list[YTruePathPlausibilityRecord] = []
    for observable in observables:
        source = availability_by_family.get(observable.family_id)
        records.append(plausibility_for_observable(observable, source))
    return records


def plausibility_for_observable(
    observable: ObservableIdentityRecord,
    availability: SourceAvailabilityMatrixRecord | None,
) -> YTruePathPlausibilityRecord:
    blockers: list[str] = []
    if not observable.source_locatable:
        blockers.append("SOURCE_NOT_LOCATABLE")
    if not observable.numeric_value_expected:
        blockers.append("NO_NUMERIC_VALUE_EXPECTATION")
    if availability is None or not availability.identity_complete:
        blockers.append("SOURCE_IDENTITY_INCOMPLETE")
    if blockers:
        level = "NONE"
    elif availability and availability.local_pdf_available:
        level = "HIGH"
    else:
        level = "MEDIUM"
    return YTruePathPlausibilityRecord(
        family_id=observable.family_id,
        source_id=observable.source_id,
        observable_class=observable.observable_class,
        possible_ytrue_source=availability.availability_status if availability else "UNKNOWN",
        plausibility_level=level,
        requires_manual_review=level in {"HIGH", "MEDIUM"},
        requires_download=bool(availability and availability.availability_status == "IDENTITY_ONLY_REQUIRES_DOWNLOAD"),
        requires_new_experiment=level == "NONE",
        blockers=blockers,
    )
