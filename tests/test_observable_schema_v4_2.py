"""Tests for v4.2 observable schema."""

from __future__ import annotations

from phyng.observable_dataset.observable_schema import get_observable_schema_records


def test_observable_schema_contains_required_classes() -> None:
    records = get_observable_schema_records()
    classes = {r.observable_class for r in records}
    expected = {
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
    }
    assert expected.issubset(classes)
