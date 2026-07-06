"""Type definitions for Xendris A/B Benchmarking."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal


@dataclass(frozen=True)
class BenchmarkSample:
    """A sample case to run in the A/B evaluation suite."""

    sample_id: str
    prompt: str
    category: str
    expected_decision: str | None = None
    expected_reason: str | None = None
    expected_answer: str | None = None
    metadata: dict[str, str] | None = None


@dataclass(frozen=True)
class SystemRunResult:
    """The result of executing a single sample against a system."""

    sample_id: str
    system_name: str
    base_model: str
    answer: str
    decision: str | None = None
    reason: str | None = None
    scoring_allowed: bool | None = None
    latency_ms: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost_usd: float | None = None
    error: str | None = None
    fingerprint: str = ""

    def to_dict(self) -> dict[str, object]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class ABComparisonResult:
    """The comparison of runs for a single sample between DeepSeek and Xendris."""

    sample_id: str
    category: str
    deepseek_result: SystemRunResult
    xendris_result: SystemRunResult
    deepseek_score: float
    xendris_score: float
    delta_score: float
    winner: Literal["deepseek", "xendris", "tie"]
    notes: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Convert to dictionary."""
        return {
            "sample_id": self.sample_id,
            "category": self.category,
            "deepseek_result": self.deepseek_result.to_dict(),
            "xendris_result": self.xendris_result.to_dict(),
            "deepseek_score": self.deepseek_score,
            "xendris_score": self.xendris_score,
            "delta_score": self.delta_score,
            "winner": self.winner,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class ABRunSummary:
    """Aggregated stats for the entire A/B run."""

    total_samples: int
    xendris_wins: int
    deepseek_wins: int
    ties: int
    average_deepseek_score: float
    average_xendris_score: float
    average_delta: float
    xendris_win_rate: float
    deepseek_win_rate: float
    tie_rate: float
    average_latency_deepseek_ms: float
    average_latency_xendris_ms: float
    latency_overhead_ms: float
    total_cost_deepseek_usd: float
    total_cost_xendris_usd: float
    cost_overhead_usd: float
    xendris_exclusion_rate: float
    xendris_human_review_rate: float
    cost_per_valid_answer_deepseek: float
    cost_per_valid_answer_xendris: float

    def to_dict(self) -> dict[str, object]:
        """Convert to dictionary."""
        return asdict(self)
