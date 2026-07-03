"""Evaluate measurement readiness for v4.2."""

from __future__ import annotations

from phyng.observable_dataset.schemas import MeasurementReadinessRecord, NormalizedObservableTarget


def evaluate_readiness(targets: list[NormalizedObservableTarget]) -> list[MeasurementReadinessRecord]:
    """Evaluate readiness per observable class and construct the readiness matrix."""
    matrix: list[MeasurementReadinessRecord] = []

    classes = [
        "VISIBILITY",
        "COHERENCE_LOSS",
        "DECOHERENCE_RATE",
        "CONTRAST_DECAY",
        "MASS_REGIME",
        "TIME_REGIME",
        "SEPARATION_REGIME",
        "TEMPERATURE_PRESSURE_REGIME",
        "PARAMETER_BOUND",
        "LIMITATION_FLAG",
        "EXPERIMENTAL_CONTEXT",
    ]

    for c in classes:
        ts = [t for t in targets if t.observable_class == c]
        t_count = len(ts)

        avail = sum(1 for t in ts if t.y_true_status == "Y_TRUE_AVAILABLE")
        pub = sum(1 for t in ts if t.y_true_status == "Y_TRUE_ACQUIRABLE_PUBLIC_DATA")
        manual = sum(1 for t in ts if t.y_true_status == "Y_TRUE_ACQUIRABLE_MANUAL_EXTRACTION")
        exp = sum(1 for t in ts if t.y_true_status == "Y_TRUE_REQUIRES_EXPERIMENT")
        blocked = sum(1 for t in ts if t.y_true_status in ("Y_TRUE_NOT_OBSERVABLE_FROM_CURRENT_SOURCE", "Y_TRUE_BLOCKED_BY_AMBIGUITY"))

        # Determine readiness status and next actions
        if t_count == 0:
            status = "BLOCKED"
            next_action = "No targets classified in this class."
        elif blocked == t_count:
            status = "BLOCKED"
            next_action = "Observable class serves only as constraints or limits."
        elif exp > 0:
            status = "EXPERIMENT_REQUIRED"
            next_action = "Design experimental measurements to capture values."
        elif manual > 0:
            status = "MANUAL_EXTRACTION_REQUIRED"
            next_action = "Perform manual data extraction from source papers."
        elif pub > 0:
            status = "PUBLIC_DATA_SEARCH_REQUIRED"
            next_action = "Search public repositories for datasets."
        else:
            status = "READY_FOR_YTRUE_EXTRACTION"
            next_action = "Acquire observed truth values."

        matrix.append(
            MeasurementReadinessRecord(
                observable_class=c,
                target_count=t_count,
                y_true_available_count=avail,
                public_data_acquirable_count=pub,
                manual_extraction_count=manual,
                experiment_required_count=exp,
                blocked_count=blocked,
                readiness_status=status,
                next_action=next_action,
            )
        )

    return matrix
