"""Types for the Xendris Programming Reliability Benchmark."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class ProgrammingSample:
    """One programming reliability benchmark sample."""

    sample_id: str
    category: str
    language: str
    prompt: str
    starter_code: str | None
    test_code: str | None
    expected_behavior: str
    expected_decision: str
    expected_reason: str | None = None
    forbidden_changes: tuple[str, ...] = ()
    metadata: Mapping[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        payload = asdict(self)
        payload["forbidden_changes"] = list(self.forbidden_changes)
        payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class ProgrammingRunResult:
    """Result for one system on one programming sample."""

    sample_id: str
    system_name: str
    language: str
    answer: str
    extracted_code: str | None
    tests_passed: bool
    contract_preserved: bool
    runtime_error: str | None
    security_risk: bool
    performance_regression: bool
    decision: str
    reason: str | None
    score: float
    latency_ms: float
    estimated_cost_usd: float
    fingerprint: str
    calibration_audit: Mapping[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        payload = asdict(self)
        if self.calibration_audit is None:
            payload.pop("calibration_audit", None)
        return payload


@dataclass(frozen=True)
class ProgrammingBenchmarkSummary:
    """Aggregated programming benchmark summary."""

    total_samples: int
    average_score: float
    tests_passed_count: int
    contract_preserved_count: int
    runtime_error_count: int
    security_risk_count: int
    exclusion_rate: float
    production_overclaim_rate: float
    cost_per_correct_solution: float | None
    score_by_category: dict[str, float]
    calibration_metrics: Mapping[str, int] | None = None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        payload = asdict(self)
        if self.calibration_metrics is None:
            payload.pop("calibration_metrics", None)
        return payload
