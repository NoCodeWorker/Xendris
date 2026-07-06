#!/usr/bin/env python3
"""Run the local Xendris v0.2.1 release hygiene gate."""

from __future__ import annotations

from dataclasses import dataclass
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
    known_warning: bool = False

    @property
    def passed(self) -> bool:
        return self.returncode == 0


def main() -> int:
    steps = run_release_gate()
    status = decide_status(steps)
    print(render_report(steps, status))
    return 0 if status == "PASS" else 1


def run_release_gate() -> list[GateStep]:
    """Run release hygiene checks without hiding failures."""
    python = sys.executable
    commands = [
        (
            "focused_citation_checker_tests",
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
    ]
    steps: list[GateStep] = []
    for name, command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        known_warning = name == "git_diff_check" and _is_known_phyng_api_whitespace_only(
            result.stdout + result.stderr
        )
        steps.append(
            GateStep(
                name=name,
                command=command,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                known_warning=known_warning,
            )
        )
    return steps


def decide_status(steps: list[GateStep]) -> str:
    """Return PASS, WARNINGS_PRESENT, or BLOCKED."""
    blockers = [step for step in steps if not step.passed and not step.known_warning]
    if blockers:
        return "BLOCKED"
    warnings = [step for step in steps if step.known_warning]
    return "WARNINGS_PRESENT" if warnings else "PASS"


def render_report(steps: list[GateStep], status: str) -> str:
    """Render a human-readable release-gate report."""
    lines = ["XENDRIS_RELEASE_GATE_V0_2_1", f"status={status}", ""]
    for step in steps:
        result = "PASS" if step.passed else "WARNING" if step.known_warning else "BLOCKED"
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


def _is_known_phyng_api_whitespace_only(output: str) -> bool:
    stripped = [
        line
        for line in output.splitlines()
        if line.strip()
        and not line.startswith("warning: in the working copy of")
        and not line.startswith("+")
    ]
    if not stripped:
        return False
    return all(line.startswith("phyng/api.py:") for line in stripped)


if __name__ == "__main__":
    raise SystemExit(main())
