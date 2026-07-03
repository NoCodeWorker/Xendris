"""Quality control rules for v4.2 observable dataset."""

from __future__ import annotations

from phyng.observable_dataset.schemas import QualityControlRules


def get_quality_control_rules() -> QualityControlRules:
    """Build the official quality control rules for v4.2 y_true planning."""
    return QualityControlRules(
        rules=[
            "unit normalization required",
            "source hash traceability required",
            "page/table/figure reference required",
            "numeric uncertainty required when available",
            "do not infer data from prose unless explicitly quantitative",
            "figure digitization must be marked as approximate",
            "supplementary files must be hashed",
            "author-provided data must be provenance-tagged",
        ],
        notes=[
            "All extracted y_true data must strictly adhere to these rules.",
            "Any validation dataset failing these rules must be rejected.",
        ],
    )
