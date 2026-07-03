"""Generate y_true acquisition plan items for v4.2."""

from __future__ import annotations

from phyng.observable_dataset.schemas import NormalizedObservableTarget, YTrueAcquisitionItem


def build_acquisition_plan(targets: list[NormalizedObservableTarget]) -> list[YTrueAcquisitionItem]:
    """Generate acquisition plan items for each normalized target."""
    plan: list[YTrueAcquisitionItem] = []

    index = 1
    for t in targets:
        c = t.observable_class

        # Prioritize based on class
        if c in ("VISIBILITY", "CONTRAST_DECAY"):
            priority = "CRITICAL"
        elif c in ("DECOHERENCE_RATE", "COHERENCE_LOSS"):
            priority = "HIGH"
        elif c in ("MASS_REGIME", "TIME_REGIME", "SEPARATION_REGIME", "TEMPERATURE_PRESSURE_REGIME"):
            priority = "MEDIUM"
        else:
            priority = "LOW"

        # Determine method and requirements
        method = "NOT_ACQUIRABLE_FROM_CURRENT_SOURCES"
        manual = False
        experimental = False
        blockers = []

        if t.y_true_status == "Y_TRUE_ACQUIRABLE_MANUAL_EXTRACTION":
            method = "MANUAL_TABLE_EXTRACTION"
            manual = True
            req_measurement = f"Extract raw numeric {t.observable_name} values from source tables."
        elif t.y_true_status == "Y_TRUE_ACQUIRABLE_PUBLIC_DATA":
            method = "PUBLIC_DATASET_LOOKUP"
            req_measurement = f"Lookup public database references for {t.observable_name} bounds."
        elif t.y_true_status == "Y_TRUE_REQUIRES_EXPERIMENT":
            method = "NEW_EXPERIMENT_REQUIRED"
            experimental = True
            blockers = ["No active experimental setup for this exact observable."]
            req_measurement = f"Perform new interferometry experiments to measure {t.observable_name}."
        else:
            method = "NOT_ACQUIRABLE_FROM_CURRENT_SOURCES"
            blockers = ["This field is a constraint or limitation, not an observable outcome."]
            req_measurement = f"Reference constraint context for {t.observable_name}."

        plan.append(
            YTrueAcquisitionItem(
                acquisition_id=f"ACQ-v4_2-{index:03d}",
                target_id=t.target_id,
                observable_class=c,
                y_true_status=t.y_true_status,
                required_measurement=req_measurement,
                candidate_data_sources=[t.source_id],
                acquisition_method=method,
                manual_extraction_required=manual,
                experimental_required=experimental,
                expected_unit=t.unit,
                quality_requirements=[
                    "Source hash traceability required.",
                    "Unit normalization to SI / standard form required.",
                    "Uncertainty bounds must be recorded.",
                ],
                blockers=blockers,
                priority=priority,
            )
        )
        index += 1

    return plan

