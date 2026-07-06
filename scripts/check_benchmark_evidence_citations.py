#!/usr/bin/env python3
"""Check benchmark docs for unsafe citations to rejected evidence artifacts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[1]


ALLOWED_CONTEXT_MARKERS = (
    "rejected",
    "rejection",
    "blocked",
    "blocker",
    "historical",
    "not admitted",
    "not evidence",
    "must not be used",
    "superseded",
    "rejected artifact",
    "rejected artifacts",
    "artefacto rechazado",
    "artefactos rechazados",
    "rechazado",
    "bloqueado",
    "historico",
    "histórico",
)


@dataclass(frozen=True)
class RejectedArtifact:
    """Rejected benchmark artifact from the evidence registry."""

    summary_path: str
    report_path: str | None
    reason: str

    @property
    def patterns(self) -> tuple[str, ...]:
        """Return path patterns that count as references to this artifact."""
        values = [self.summary_path]
        if self.report_path:
            values.append(self.report_path)
        normalized: list[str] = []
        for value in values:
            value = value.strip()
            if not value:
                continue
            normalized.append(_normalize_path_text(value))
            normalized.append(_normalize_path_text(value.replace("/", "\\")))
        return tuple(dict.fromkeys(normalized))


@dataclass(frozen=True)
class CitationViolation:
    """Unsafe citation to a rejected benchmark artifact."""

    document_path: str
    line_number: int
    artifact_path: str
    reason: str
    line_text: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-compatible representation."""
        return {
            "document_path": self.document_path,
            "line_number": self.line_number,
            "artifact_path": self.artifact_path,
            "reason": self.reason,
            "line_text": self.line_text,
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fail when docs cite rejected benchmark artifacts as evidence."
    )
    parser.add_argument("--registry", default="runs/benchmark_evidence_registry.json")
    parser.add_argument("--docs-dir", default="docs")
    parser.add_argument("--output-json", default="")
    args = parser.parse_args(argv)

    registry_path = Path(args.registry)
    docs_dir = Path(args.docs_dir)
    rejected = load_rejected_artifacts(registry_path)
    violations = check_rejected_artifact_citations(rejected, docs_dir)

    payload = {
        "registry": str(registry_path),
        "docs_dir": str(docs_dir),
        "rejected_artifact_count": len(rejected),
        "violation_count": len(violations),
        "violations": [violation.to_dict() for violation in violations],
    }

    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        "BENCHMARK_EVIDENCE_CITATIONS "
        f"rejected={len(rejected)} violations={len(violations)}"
    )
    for violation in violations:
        print(
            f"{violation.document_path}:{violation.line_number}: "
            f"unsafe reference to {violation.artifact_path} ({violation.reason})"
        )
    return 1 if violations else 0


def load_rejected_artifacts(registry_path: str | Path) -> list[RejectedArtifact]:
    """Load rejected artifact records from an evidence registry JSON file."""
    payload = json.loads(Path(registry_path).read_text(encoding="utf-8"))
    rejected: list[RejectedArtifact] = []
    for record in payload.get("rejected", []):
        if not isinstance(record, Mapping):
            continue
        summary_path = str(record.get("summary_path", "")).strip()
        if not summary_path:
            continue
        report_path = record.get("report_path")
        rejected.append(
            RejectedArtifact(
                summary_path=summary_path,
                report_path=str(report_path).strip() if report_path else None,
                reason=str(record.get("reason", "rejected")),
            )
        )
    return rejected


def check_rejected_artifact_citations(
    rejected_artifacts: Iterable[RejectedArtifact],
    docs_dir: str | Path,
) -> list[CitationViolation]:
    """Return unsafe citations to rejected benchmark artifacts in docs."""
    artifacts = tuple(rejected_artifacts)
    root = Path(docs_dir)
    if not root.exists():
        return []

    violations: list[CitationViolation] = []
    for document in _iter_markdown_documents(root):
        lines = document.read_text(encoding="utf-8").splitlines()
        normalized_lines = [_normalize_path_text(line) for line in lines]
        for index, normalized_line in enumerate(normalized_lines):
            for artifact in artifacts:
                matched_pattern = _matched_artifact_pattern(normalized_line, artifact)
                if not matched_pattern:
                    continue
                if _is_allowed_rejected_context(lines, index):
                    continue
                violations.append(
                    CitationViolation(
                        document_path=str(document),
                        line_number=index + 1,
                        artifact_path=matched_pattern,
                        reason=artifact.reason,
                        line_text=lines[index].strip(),
                    )
                )
    return violations


def _iter_markdown_documents(root: Path) -> Iterable[Path]:
    yield from sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and (path.suffix == ".md" or path.name.endswith(".md.template"))
    )


def _matched_artifact_pattern(line: str, artifact: RejectedArtifact) -> str | None:
    for pattern in artifact.patterns:
        if pattern and pattern in line:
            return pattern
    return None


def _is_allowed_rejected_context(lines: list[str], index: int) -> bool:
    current_heading = _nearest_heading(lines, index)
    window_start = max(0, index - 4)
    window_end = min(len(lines), index + 5)
    context = "\n".join([current_heading, *lines[window_start:window_end]]).lower()
    return any(marker in context for marker in ALLOWED_CONTEXT_MARKERS)


def _nearest_heading(lines: list[str], index: int) -> str:
    for offset in range(index, -1, -1):
        line = lines[offset].strip()
        if line.startswith("#"):
            return line
    return ""


def _normalize_path_text(value: str) -> str:
    return value.replace("\\", "/").lower()


if __name__ == "__main__":
    raise SystemExit(main())
