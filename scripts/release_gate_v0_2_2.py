#!/usr/bin/env python3
"""Run the local Xendris v0.2.2 clean release gate."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class GateStep:
    """One release-gate command result."""

    name: str
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    warning_only: bool = False

    @property
    def passed(self) -> bool:
        return self.returncode == 0


def main() -> int:
    steps = run_release_gate()
    historical_count = load_historical_rejected_count()
    status = decide_status(steps)
    print(render_report(steps, status, historical_count))
    return 0 if status == "PASS" else 1


def run_release_gate() -> list[GateStep]:
    """Run v0.2.2 release checks without hiding failures."""
    python = sys.executable
    commands = [
        (
            "historical_quarantine_tests",
            (python, "-m", "pytest", "tests/benchmarking/test_historical_artifact_quarantine.py", "-q"),
        ),
        (
            "citation_checker_tests",
            (python, "-m", "pytest", "tests/benchmarking/test_benchmark_evidence_citation_checker.py", "-q"),
        ),
        (
            "benchmark_suite_excellence_audit",
            (python, "scripts/audit_benchmark_suite_excellence.py", "--fail-on-blockers"),
        ),
        (
            "benchmark_evidence_registry",
            (python, "scripts/build_benchmark_evidence_registry.py", "--require-admitted"),
        ),
        (
            "benchmark_evidence_citation_checker",
            (python, "scripts/check_benchmark_evidence_citations.py"),
        ),
        ("git_diff_check", ("git", "diff", "--check")),
        ("working_tree_clean", ("git", "status", "--short")),
    ]
    steps: list[GateStep] = []
    for name, command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        returncode = result.returncode
        if name == "working_tree_clean" and result.stdout.strip():
            returncode = 1
        warning_only = name == "git_diff_check" and _is_known_warning_only(
            result.stdout + result.stderr
        )
        steps.append(
            GateStep(
                name=name,
                command=command,
                returncode=returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                warning_only=warning_only,
            )
        )
    return steps


def decide_status(steps: list[GateStep]) -> str:
    """Return PASS, WARNINGS_PRESENT, or BLOCKED."""
    blockers = [step for step in steps if not step.passed and not step.warning_only]
    if blockers:
        return "BLOCKED"
    warnings = [step for step in steps if step.warning_only]
    return "WARNINGS_PRESENT" if warnings else "PASS"


def load_historical_rejected_count() -> int:
    """Return rejected artifact count from the current evidence registry."""
    registry = ROOT / "runs" / "benchmark_evidence_registry.json"
    if not registry.exists():
        return 0
    payload = json.loads(registry.read_text(encoding="utf-8"))
    return int(payload.get("rejected_count", 0))


def render_report(steps: list[GateStep], status: str, historical_count: int) -> str:
    """Render release-gate output."""
    lines = [
        "XENDRIS_RELEASE_GATE_V0_2_2",
        f"status={status}",
        f"historical_rejected_artifacts={historical_count}",
        "",
    ]
    for step in steps:
        result = "PASS" if step.passed else "WARNING" if step.warning_only else "BLOCKED"
        lines.append(f"[{result}] {step.name}")
        lines.append(f"command={' '.join(step.command)}")
        if step.stdout.strip():
            lines.append("stdout:")
            lines.append(step.stdout.strip())
        if step.stderr.strip():
            lines.append("stderr:")
            lines.append(step.stderr.strip())
        lines.append("")
    return "\n".join(lines).strip()


def _is_known_warning_only(output: str) -> bool:
    """Return true when diff-check output has only CRLF warnings."""
    stripped = [
        line
        for line in output.splitlines()
        if line.strip() and not line.startswith("warning: in the working copy of")
    ]
    return not stripped


if __name__ == "__main__":
    raise SystemExit(main())
