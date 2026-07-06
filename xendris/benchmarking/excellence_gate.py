"""Benchmark Excellence Gate v0.1.

The gate is a conservative structural review for benchmark artifacts. It does
not improve outputs, change scores, call providers, modify datasets, validate
universal superiority, or inflate benchmarks.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class BenchmarkExcellenceDecision(str, Enum):
    """Allowed Benchmark Excellence Gate decisions."""

    READY_FOR_INTERPRETATION = "READY_FOR_INTERPRETATION"
    WARNINGS_PRESENT = "WARNINGS_PRESENT"
    BLOCKED_FOR_INTERPRETATION = "BLOCKED_FOR_INTERPRETATION"


class BenchmarkExcellenceIssueSeverity(str, Enum):
    """Issue severity for Benchmark Excellence Gate findings."""

    BLOCKER = "BLOCKER"
    WARNING = "WARNING"
    NOTE = "NOTE"


@dataclass(frozen=True)
class BenchmarkExcellenceIssue:
    """One issue or note found by the Benchmark Excellence Gate."""

    code: str
    severity: BenchmarkExcellenceIssueSeverity
    message: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-compatible representation."""
        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
        }


@dataclass(frozen=True)
class BenchmarkExcellenceAssessment:
    """Result of a benchmark excellence assessment."""

    decision: BenchmarkExcellenceDecision
    issues: tuple[BenchmarkExcellenceIssue, ...]

    @property
    def blockers(self) -> tuple[BenchmarkExcellenceIssue, ...]:
        """Return blocker issues."""
        return tuple(issue for issue in self.issues if issue.severity == BenchmarkExcellenceIssueSeverity.BLOCKER)

    @property
    def warnings(self) -> tuple[BenchmarkExcellenceIssue, ...]:
        """Return warning issues."""
        return tuple(issue for issue in self.issues if issue.severity == BenchmarkExcellenceIssueSeverity.WARNING)

    @property
    def notes(self) -> tuple[BenchmarkExcellenceIssue, ...]:
        """Return notes."""
        return tuple(issue for issue in self.issues if issue.severity == BenchmarkExcellenceIssueSeverity.NOTE)

    @property
    def has_blockers(self) -> bool:
        """Return True when interpretation must be blocked."""
        return bool(self.blockers)

    @property
    def has_warnings(self) -> bool:
        """Return True when non-blocking warnings are present."""
        return bool(self.warnings)

    @property
    def is_ready(self) -> bool:
        """Return True when no blocker prevents careful interpretation."""
        return not self.has_blockers

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        return {
            "decision": self.decision.value,
            "issues": [issue.to_dict() for issue in self.issues],
            "blockers": [issue.to_dict() for issue in self.blockers],
            "warnings": [issue.to_dict() for issue in self.warnings],
            "notes": [issue.to_dict() for issue in self.notes],
            "has_blockers": self.has_blockers,
            "has_warnings": self.has_warnings,
            "is_ready": self.is_ready,
        }


def assess_benchmark_excellence(
    summary: Mapping[str, Any],
    report_text: str | None = None,
) -> BenchmarkExcellenceAssessment:
    """Assess whether benchmark artifacts are structurally interpretable."""
    issues: list[BenchmarkExcellenceIssue] = []
    metadata = _mapping(summary.get("metadata"))
    normalized_report = _normalize(report_text or "")
    execution_mode = _normalize(str(metadata.get("execution_mode", "")))
    is_dry_run = execution_mode in {"dry_run", "dry-run", "dryrun"}
    is_real_provider = execution_mode in {"real_provider", "real-provider", "real", "api", "provider"}

    _require(_has(metadata, "dataset_hash"), issues, "missing_dataset_hash", "Dataset hash is required.")
    _require(_has(metadata, "execution_mode"), issues, "missing_execution_mode", "Execution mode is required.")
    _require(
        _has(metadata, "dataset_name") or _has(metadata, "dataset_version"),
        issues,
        "missing_dataset_version_or_name",
        "Dataset name or dataset version is required.",
    )
    _require(
        _has(metadata, "model") or _has(metadata, "base_model") or _has_system_names(summary),
        issues,
        "missing_model_name_or_system_names",
        "Model name or comparable system names are required.",
    )

    total = _total_sample_count(summary)
    _require(total is not None, issues, "missing_total_sample_count", "Total sample count is required.")
    if total is not None and total <= 0:
        _add_blocker(issues, "invalid_total_sample_count", "Total sample count must be greater than zero.")

    _require(
        _has_comparable_score_pair(summary),
        issues,
        "missing_comparable_score_pair",
        "Two comparable score fields or system summaries are required.",
    )
    _require(_has(summary, "average_delta"), issues, "missing_average_delta", "Average delta is required.")

    if not _contains_no_universal_superiority_warning(normalized_report):
        _add_blocker(
            issues,
            "missing_no_universal_superiority_warning",
            "Report must include a clear no-universal-superiority warning.",
        )

    if not _contains_limitations_section(normalized_report):
        _add_blocker(
            issues,
            "missing_limitations_section",
            "Report must include a limitations section.",
        )

    if is_dry_run:
        _add_note(issues, "dry_run_result", "Execution mode is dry-run; provider performance is not measured.")
        if _dry_run_claims_real_provider_performance(normalized_report):
            _add_blocker(
                issues,
                "dry_run_report_claims_real_provider_performance",
                "Dry-run report suggests real provider performance.",
            )

    if is_real_provider and not _has(metadata, "provider"):
        _add_blocker(
            issues,
            "real_provider_run_missing_provider_name",
            "Real provider run must disclose provider name.",
        )

    _warn_if_missing(metadata, "temperature", issues, "missing_temperature", "Temperature is not disclosed.")
    _warn_if_missing(metadata, "max_tokens", issues, "missing_max_tokens", "Max token limit is not disclosed.")
    _warn_if_missing(metadata, "xendris_version", issues, "missing_xendris_version", "Xendris version is not disclosed.")
    _warn_if_missing(metadata, "python_version", issues, "missing_python_version", "Python version is not disclosed.")
    _warn_if_missing(metadata, "dataset_hash_algorithm", issues, "missing_dataset_hash_algorithm", "Dataset hash algorithm is not disclosed.")
    _warn_if_missing(metadata, "run_date", issues, "missing_run_date", "Run date is not disclosed.")
    _warn_if_missing(metadata, "provider", issues, "missing_provider_disclosure", "Provider is not disclosed.")
    _warn_if_missing(
        metadata,
        "external_data_disclosure",
        issues,
        "missing_external_data_disclosure",
        "External data disclosure policy is not documented.",
    )
    _warn_if_missing(
        metadata,
        "pricing_assumptions",
        issues,
        "missing_pricing_assumptions",
        "Pricing assumptions are not documented.",
    )

    has_latency = _has_latency_metrics(summary)
    has_cost = _has_cost_metrics(summary)
    if not has_latency:
        severity = BenchmarkExcellenceIssueSeverity.BLOCKER if _report_claims_latency(normalized_report) else BenchmarkExcellenceIssueSeverity.WARNING
        _add_issue(issues, "missing_latency_metrics", severity, "Latency metrics are missing.")
    if not has_cost:
        severity = BenchmarkExcellenceIssueSeverity.BLOCKER if _report_claims_cost(normalized_report) else BenchmarkExcellenceIssueSeverity.WARNING
        _add_issue(issues, "missing_cost_metrics", severity, "Cost metrics are missing.")

    _add_context_notes(summary, normalized_report, issues)

    if any(issue.severity == BenchmarkExcellenceIssueSeverity.BLOCKER for issue in issues):
        decision = BenchmarkExcellenceDecision.BLOCKED_FOR_INTERPRETATION
    elif any(issue.severity == BenchmarkExcellenceIssueSeverity.WARNING for issue in issues):
        decision = BenchmarkExcellenceDecision.WARNINGS_PRESENT
    else:
        decision = BenchmarkExcellenceDecision.READY_FOR_INTERPRETATION

    return BenchmarkExcellenceAssessment(decision=decision, issues=tuple(issues))


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _has(mapping: Mapping[str, Any], key: str) -> bool:
    return key in mapping and mapping[key] not in {None, ""}


def _normalize(text: str) -> str:
    return text.lower().replace("_", "-")


def _total_sample_count(summary: Mapping[str, Any]) -> int | None:
    value = summary.get("total_samples", summary.get("total_sample_count"))
    return value if isinstance(value, int) else None


def _has_system_names(summary: Mapping[str, Any]) -> bool:
    systems = _mapping(summary.get("systems"))
    return len(systems) >= 2


def _has_comparable_score_pair(summary: Mapping[str, Any]) -> bool:
    score_pairs = (
        ("average_score_deepseek", "average_score_xendris"),
        ("average_deepseek_score", "average_xendris_score"),
    )
    if any(all(_has(summary, key) for key in pair) for pair in score_pairs):
        return True
    systems = _mapping(summary.get("systems"))
    scored_systems = [
        system for system in systems.values()
        if isinstance(system, Mapping) and _has(system, "average_score")
    ]
    return len(scored_systems) >= 2


def _has_latency_metrics(summary: Mapping[str, Any]) -> bool:
    if any(_has(summary, key) for key in ("average_latency_deepseek_ms", "average_latency_xendris_ms", "latency_overhead_ms")):
        return True
    systems = _mapping(summary.get("systems"))
    return any(isinstance(system, Mapping) and _has(system, "latency_average_ms") for system in systems.values())


def _has_cost_metrics(summary: Mapping[str, Any]) -> bool:
    if any(_has(summary, key) for key in ("total_cost_deepseek_usd", "total_cost_xendris_usd", "cost_per_valid_answer_deepseek", "cost_per_valid_answer_xendris")):
        return True
    systems = _mapping(summary.get("systems"))
    return any(
        isinstance(system, Mapping)
        and any(_has(system, key) for key in ("estimated_cost_usd", "cost_per_correct_solution", "cost_per_valid_answer"))
        for system in systems.values()
    )


def _contains_no_universal_superiority_warning(report: str) -> bool:
    return (
        "no universal superiority" in report
        or "no-superioridad universal" in report
        or "no superioridad universal" in report
        or "does not imply universal" in report
        or "no demuestra superioridad universal" in report
    )


def _contains_limitations_section(report: str) -> bool:
    return "## limitations" in report or "## limitaciones" in report or "\nlimitations" in report or "\nlimitaciones" in report


def _dry_run_claims_real_provider_performance(report: str) -> bool:
    suspicious = (
        "real provider run",
        "real-provider run",
        "corrida real",
        "proveedor real",
        "api real",
        "real deepseek score",
    )
    return any(phrase in report for phrase in suspicious)


def _report_claims_cost(report: str) -> bool:
    return any(phrase in report for phrase in (" cost", "\ncost", "cost ", "coste", "costo", "pricing", "precio"))


def _report_claims_latency(report: str) -> bool:
    return any(phrase in report for phrase in ("latency", "latencia", "ms ", "milliseconds"))


def _add_context_notes(summary: Mapping[str, Any], report: str, issues: list[BenchmarkExcellenceIssue]) -> None:
    metadata = _mapping(summary.get("metadata"))
    dataset_name = _normalize(str(metadata.get("dataset_name", "")))
    if "benchmark-local" in report or "benchmark local" in report or "under this dataset" in report:
        _add_note(issues, "benchmark_local_only", "Report limits interpretation to the benchmark context.")
    if "closed dataset" in report or "dataset cerrado" in report or "closed" in dataset_name:
        _add_note(issues, "closed_dataset", "Artifact describes a closed dataset.")
    if "synthetic" in report or "sintético" in report or "synthetic" in dataset_name:
        _add_note(issues, "synthetic_dataset", "Artifact describes a synthetic dataset.")
    if summary.get("gap_closed_ratio") is None and "frontier gap" in report:
        _add_note(issues, "frontier_gap_not_applicable", "Frontier gap appears not applicable.")


def _require(condition: bool, issues: list[BenchmarkExcellenceIssue], code: str, message: str) -> None:
    if not condition:
        _add_blocker(issues, code, message)


def _warn_if_missing(
    metadata: Mapping[str, Any],
    key: str,
    issues: list[BenchmarkExcellenceIssue],
    code: str,
    message: str,
) -> None:
    if not _has(metadata, key):
        _add_issue(issues, code, BenchmarkExcellenceIssueSeverity.WARNING, message)


def _add_blocker(issues: list[BenchmarkExcellenceIssue], code: str, message: str) -> None:
    _add_issue(issues, code, BenchmarkExcellenceIssueSeverity.BLOCKER, message)


def _add_note(issues: list[BenchmarkExcellenceIssue], code: str, message: str) -> None:
    _add_issue(issues, code, BenchmarkExcellenceIssueSeverity.NOTE, message)


def _add_issue(
    issues: list[BenchmarkExcellenceIssue],
    code: str,
    severity: BenchmarkExcellenceIssueSeverity,
    message: str,
) -> None:
    issues.append(BenchmarkExcellenceIssue(code=code, severity=severity, message=message))
