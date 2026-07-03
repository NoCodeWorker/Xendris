"""Observable target matrix construction."""

from __future__ import annotations

from phyng.source_acquisition.schemas import ObservableTargetRecord, SourceAcquisitionQueueItem


def build_observable_target_matrix(queue: list[SourceAcquisitionQueueItem]) -> list[ObservableTargetRecord]:
    records = []
    for item in queue:
        for observable in item.target_observable_classes:
            records.append(
                ObservableTargetRecord(
                    source_candidate_id=item.acquisition_id,
                    target_observable_class=observable,
                    target_variable="visibility_fraction" if "VISIBILITY" in observable else "interference_contrast",
                    expected_condition_axis=item.expected_conditions[0] if item.expected_conditions else "unknown_condition",
                    expected_location_type="FIGURE",
                    expected_numeric_form="fraction_or_percent_visibility_or_contrast",
                    why_ytrue_possible=item.reason_for_relevance,
                    risk_of_not_ytrue="May require visual figure extraction; source identity alone is not evidence.",
                    priority=item.priority,
                )
            )
    return records
