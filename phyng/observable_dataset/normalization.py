"""Normalize benchmark rows into standardized observable targets."""

from __future__ import annotations

from phyng.observable_dataset.schemas import NormalizedObservableTarget


def normalize_benchmark_rows(benchmark_rows: list[dict]) -> list[NormalizedObservableTarget]:
    """Normalize v4.0 benchmark rows into formal observable targets."""
    targets: list[NormalizedObservableTarget] = []

    index = 1
    for r in benchmark_rows:
        bid = r.get("benchmark_id", "")
        sid = r.get("source_id", "")
        eid = r.get("extract_id", "")
        obs_type = r.get("observable_type", "")
        text = r.get("observable_text", "")
        text_lower = text.lower()

        # Default mapping values
        obs_class = "EXPERIMENTAL_CONTEXT"
        var_name = "experimental_context"
        unit = "dimensionless"
        dtype = "string"
        context = "Context details from source literature"
        yt_status = "Y_TRUE_NOT_OBSERVABLE_FROM_CURRENT_SOURCE"

        if obs_type == "BASELINE":
            obs_class = "DECOHERENCE_RATE"
            var_name = "decoherence_rate"
            unit = "s^-1"
            dtype = "float"
            context = "Exponential baseline decay rate parameter"
            yt_status = "Y_TRUE_ACQUIRABLE_MANUAL_EXTRACTION"

        elif obs_type == "OBSERVABLE":
            if "visibility" in text_lower or "contrast" in text_lower:
                obs_class = "VISIBILITY"
                var_name = "visibility"
                unit = "dimensionless"
                dtype = "float"
                context = "Interference pattern fringe visibility contrast"
                yt_status = "Y_TRUE_ACQUIRABLE_MANUAL_EXTRACTION"
            elif "coherence" in text_lower:
                obs_class = "COHERENCE_LOSS"
                var_name = "coherence_loss"
                unit = "dimensionless"
                dtype = "float"
                context = "Decoherence/contrast reduction fraction"
                yt_status = "Y_TRUE_ACQUIRABLE_MANUAL_EXTRACTION"
            else:
                obs_class = "CONTRAST_DECAY"
                var_name = "contrast_decay_rate"
                unit = "s^-1"
                dtype = "float"
                context = "Fringe contrast decay constant"
                yt_status = "Y_TRUE_REQUIRES_EXPERIMENT"

        elif obs_type == "BENCHMARK_RANGE":
            if r.get("mass_range") is not None:
                obs_class = "MASS_REGIME"
                var_name = "mass"
                unit = "amu"
                dtype = "float"
                context = "Test particle mass boundaries"
            elif r.get("time_range") is not None:
                obs_class = "TIME_REGIME"
                var_name = "time"
                unit = "s"
                dtype = "float"
                context = "Coherence/interaction duration boundaries"
            elif r.get("length_or_separation_range") is not None:
                obs_class = "SEPARATION_REGIME"
                var_name = "separation"
                unit = "m"
                dtype = "float"
                context = "Spatial separation length/width bounds"
            else:
                obs_class = "TEMPERATURE_PRESSURE_REGIME"
                var_name = "temperature_pressure"
                unit = "K or mbar"
                dtype = "float"
                context = "Environmental pressure/temperature bounds"
            yt_status = "Y_TRUE_ACQUIRABLE_PUBLIC_DATA"

        elif obs_type == "PARAMETER_CONSTRAINT":
            obs_class = "PARAMETER_BOUND"
            var_name = "parameter_bound"
            unit = "dimensionless"
            dtype = "float"
            context = "CSL collapse parameter/bounds constraints"
            yt_status = "Y_TRUE_NOT_OBSERVABLE_FROM_CURRENT_SOURCE"

        elif obs_type == "NEGATIVE_LIMITATION":
            obs_class = "LIMITATION_FLAG"
            var_name = "limitation_flag"
            unit = "dimensionless"
            dtype = "string"
            context = "Environmental limitation background noise floor flag"
            yt_status = "Y_TRUE_NOT_OBSERVABLE_FROM_CURRENT_SOURCE"

        regime_fields = {
            "mass_range": r.get("mass_range"),
            "time_range": r.get("time_range"),
            "length_or_separation_range": r.get("length_or_separation_range"),
            "temperature_or_pressure": r.get("temperature_or_pressure"),
        }

        targets.append(
            NormalizedObservableTarget(
                target_id=f"TGT-v4_2-{index:03d}",
                benchmark_id=bid,
                source_id=sid,
                extract_id=eid,
                observable_class=obs_class,
                observable_name=obs_class.replace("_", " ").lower(),
                source_observable_text=text,
                normalized_variable_name=var_name,
                unit=unit,
                expected_dtype=dtype,
                measurement_context=context,
                regime_fields=regime_fields,
                candidate_model_fields=["predicted_visibility", "decay_rate"] if obs_class in ("VISIBILITY", "COHERENCE_LOSS", "DECOHERENCE_RATE", "CONTRAST_DECAY") else [],
                baseline_model_fields=["baseline_decay_rate"] if obs_class == "DECOHERENCE_RATE" else [],
                y_true_required=True,  # Hardcoded true per spec
                y_true_status=yt_status,
                slot4_debt_status="OPEN_BLOCKING_FOR_GRADIENT_CLAIMS",  # Hardcoded debt status
                predictive_gain_allowed=False,  # Hardcoded false since y_true is not Y_TRUE_AVAILABLE
                notes=[
                    f"Normalized from benchmark row {bid}.",
                    "No observed y_true is present; predictive gain is blocked.",
                ],
            )
        )
        index += 1

    return targets
