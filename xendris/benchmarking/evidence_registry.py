"""Benchmark evidence registry for Xendris.

The registry admits only benchmark artifacts that passed the Benchmark
Excellence Gate. It does not rescore, improve, or reinterpret model outputs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Literal, Mapping


BenchmarkEvidenceStatus = Literal["ADMITTED", "REJECTED"]


@dataclass(frozen=True)
class BenchmarkEvidenceRecord:
    """One benchmark artifact admission record."""

    summary_path: str
    status: BenchmarkEvidenceStatus
    decision: str
    report_path: str | None
    blocker_count: int
    warning_count: int
    reason: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        return asdict(self)


@dataclass(frozen=True)
class BenchmarkEvidenceRegistry:
    """Registry of benchmark artifacts admitted or rejected as evidence."""

    admitted: tuple[BenchmarkEvidenceRecord, ...]
    rejected: tuple[BenchmarkEvidenceRecord, ...]

    @property
    def admitted_count(self) -> int:
        """Return the number of admitted benchmark artifacts."""
        return len(self.admitted)

    @property
    def rejected_count(self) -> int:
        """Return the number of rejected benchmark artifacts."""
        return len(self.rejected)

    @property
    def total_count(self) -> int:
        """Return total benchmark artifacts reviewed."""
        return self.admitted_count + self.rejected_count

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        return {
            "admitted_count": self.admitted_count,
            "rejected_count": self.rejected_count,
            "total_count": self.total_count,
            "admitted": [record.to_dict() for record in self.admitted],
            "rejected": [record.to_dict() for record in self.rejected],
        }


def build_benchmark_evidence_registry(audit_payload: Mapping[str, Any]) -> BenchmarkEvidenceRegistry:
    """Build an evidence registry from a suite excellence audit payload."""
    admitted: list[BenchmarkEvidenceRecord] = []
    rejected: list[BenchmarkEvidenceRecord] = []
    for raw_record in audit_payload.get("records", []):
        if not isinstance(raw_record, Mapping):
            continue
        record = _record_from_audit(raw_record)
        if record.status == "ADMITTED":
            admitted.append(record)
        else:
            rejected.append(record)
    return BenchmarkEvidenceRegistry(admitted=tuple(admitted), rejected=tuple(rejected))


def write_benchmark_evidence_registry_json(
    registry: BenchmarkEvidenceRegistry,
    path: str | Path,
) -> None:
    """Write evidence registry JSON."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(registry.to_dict(), ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def render_benchmark_evidence_registry_markdown(registry: BenchmarkEvidenceRegistry) -> str:
    """Render evidence registry as Markdown."""
    admitted_rows = [
        f"| `{record.summary_path}` | `{record.report_path or 'none'}` |"
        for record in registry.admitted
    ]
    rejected_rows = [
        f"| `{record.summary_path}` | `{record.decision}` | {record.blocker_count} | {record.warning_count} | {record.reason} |"
        for record in registry.rejected
    ]
    return f"""# Benchmark Evidence Registry

## Summary

| Metric | Value |
|---|---:|
| Total artifacts reviewed | {registry.total_count} |
| Admitted | {registry.admitted_count} |
| Rejected | {registry.rejected_count} |

## Admitted Artifacts

Only artifacts admitted here may be used as benchmark evidence in comparisons,
roadmap decisions, or public-facing benchmark claims.

| Summary | Report |
|---|---|
{chr(10).join(admitted_rows) if admitted_rows else '| none | none |'}

## Rejected Artifacts

Rejected artifacts may remain historically useful, but must not be used as
strong evidence until remediated and re-audited.

| Summary | Decision | Blockers | Warnings | Reason |
|---|---|---:|---:|---|
{chr(10).join(rejected_rows) if rejected_rows else '| none | none | 0 | 0 | none |'}

## Interpretation

This registry controls evidence admission only. It does not validate universal
model superiority, production readiness, or scientific truth.
"""


def write_benchmark_evidence_registry_markdown(
    registry: BenchmarkEvidenceRegistry,
    path: str | Path,
) -> None:
    """Write evidence registry Markdown."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_benchmark_evidence_registry_markdown(registry), encoding="utf-8")


def _record_from_audit(record: Mapping[str, Any]) -> BenchmarkEvidenceRecord:
    decision = str(record.get("decision", "UNKNOWN"))
    has_blockers = bool(record.get("has_blockers", False))
    blocker_count = _int_value(record.get("blocker_count"))
    warning_count = _int_value(record.get("warning_count"))
    status: BenchmarkEvidenceStatus = (
        "ADMITTED" if decision == "READY_FOR_INTERPRETATION" and not has_blockers else "REJECTED"
    )
    reason = "Ready for careful interpretation." if status == "ADMITTED" else _rejection_reason(record)
    return BenchmarkEvidenceRecord(
        summary_path=str(record.get("summary_path", "")),
        status=status,
        decision=decision,
        report_path=record.get("report_path") if record.get("report_path") else None,
        blocker_count=blocker_count,
        warning_count=warning_count,
        reason=reason,
    )


def _rejection_reason(record: Mapping[str, Any]) -> str:
    issues = record.get("issues", [])
    if isinstance(issues, list):
        for issue in issues:
            if isinstance(issue, Mapping) and issue.get("severity") == "BLOCKER":
                return str(issue.get("code", "blocked"))
    return "not_ready_for_interpretation"


def _int_value(value: Any) -> int:
    return value if isinstance(value, int) else 0
