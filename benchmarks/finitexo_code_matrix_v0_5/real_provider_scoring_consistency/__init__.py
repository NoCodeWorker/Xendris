"""v0.5.6 real-provider scoring consistency gate."""

from .scoring_gate import (
    ScoringConsistencyConfig,
    evaluate_scoring_consistency,
    write_scoring_consistency_artifacts,
)

__all__ = [
    "ScoringConsistencyConfig",
    "evaluate_scoring_consistency",
    "write_scoring_consistency_artifacts",
]
