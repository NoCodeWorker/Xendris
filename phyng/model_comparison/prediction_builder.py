"""Build prediction records for v4.1 model comparison."""

from __future__ import annotations

from phyng.model_comparison.schemas import ModelPredictionRecord, ModelRegistryRecord


def build_prediction_records(
    models: list[ModelRegistryRecord],
    benchmark_rows: list[dict],
) -> list[ModelPredictionRecord]:
    """Generate prediction records for all model/row pairs."""
    predictions: list[ModelPredictionRecord] = []

    index = 1
    for model in models:
        for row in benchmark_rows:
            benchmark_id = row.get("benchmark_id", "")
            source_id = row.get("source_id", "")
            obs_type = row.get("observable_type", "")
            allowed_comp = row.get("allowed_model_comparison", True)

            # Build prediction behavior and basis descriptions based on model family
            if model.model_family == "BASELINE":
                basis = "Standard decoherence formulation (thermal / collisional / gas scattering)"
                behavior = "Calculated decoherence baseline decay"
            elif model.model_family == "NEGATIVE_CONTROL":
                basis = "Decoherence model with candidate active coupling term set to zero"
                behavior = "Zero active signal visibility curves"
            else:
                basis = f"Simulated prediction using constraints from {row.get('observable_type', '')}"
                behavior = "Bounded candidate visibility curve predictions"

            predictions.append(
                ModelPredictionRecord(
                    prediction_id=f"PRED-v4_1-{index:04d}",
                    model_id=model.model_id,
                    benchmark_id=benchmark_id,
                    source_id=source_id,
                    observable_type=obs_type,
                    predicted_behavior=behavior,
                    prediction_basis=basis,
                    uses_real_y_true=False,  # Hardcoded false since no real-world y_true
                    y_true_available=False,  # Hardcoded false
                    comparison_allowed=allowed_comp,
                    limitations=[
                        "Simulated prediction only; no real y_true observed data.",
                        f"Subject to model limitations of {model.model_id}.",
                    ],
                )
            )
            index += 1

    return predictions
