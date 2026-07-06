"""Interpretation gate for experimental programming calibration ablations."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class CalibrationAblationGateIssue:
    """One structural issue found in a calibration ablation artifact."""

    code: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class CalibrationAblationGateAssessment:
    """Gate decision for experimental calibration ablation evidence."""

    status: str
    issues: tuple[CalibrationAblationGateIssue, ...]

    @property
    def has_blockers(self) -> bool:
        return any(issue.severity == "BLOCKER" for issue in self.issues)

    def to_dict(self) -> dict[str, object]:
        blockers = [issue.to_dict() for issue in self.issues if issue.severity == "BLOCKER"]
        warnings = [issue.to_dict() for issue in self.issues if issue.severity == "WARNING"]
        notes = [issue.to_dict() for issue in self.issues if issue.severity == "NOTE"]
        return {
            "status": self.status,
            "issues": [issue.to_dict() for issue in self.issues],
            "blockers": blockers,
            "warnings": warnings,
            "notes": notes,
            "has_blockers": self.has_blockers,
        }


def assess_programming_calibration_ablation(
    summary: Mapping[str, Any],
    report_text: str | None = None,
) -> CalibrationAblationGateAssessment:
    """Assess whether calibration ablation output is ready as experimental analysis."""
    issues: list[CalibrationAblationGateIssue] = []
    metadata = _mapping(summary.get("metadata"))
    report = _normalize(report_text or "")

    _require(metadata.get("dataset_name"), issues, "missing_dataset_name", "Dataset name is required.")
    _require(metadata.get("dataset_version"), issues, "missing_dataset_version", "Dataset version is required.")
    _require(metadata.get("dataset_hash"), issues, "missing_dataset_hash", "Dataset hash is required.")
    _require(
        str(metadata.get("execution_mode", "")).lower() in {"dry-run", "dry_run"},
        issues,
        "missing_dry_run_mode",
        "Calibration ablation must disclose dry-run execution mode.",
    )
    _require(
        str(metadata.get("provider_mode", "")).lower() in {"mock", "dry-run", "dry_run"},
        issues,
        "missing_mock_provider_mode",
        "Calibration ablation must disclose mock provider mode.",
    )
    _require(
        metadata.get("experimental_calibration_variant_disclosed") is True,
        issues,
        "missing_calibration_disclosure",
        "Summary must disclose the experimental calibration variant.",
    )
    _require(
        metadata.get("historical_artifacts_overwritten") is False,
        issues,
        "historical_artifact_overwrite_not_disclosed",
        "Summary must disclose that historical artifacts were not overwritten.",
    )

    variants = summary.get("variants", [])
    variant_names = set(variants) if isinstance(variants, list) else set()
    expected = {"deepseek_base", "xendris_uncalibrated", "xendris_calibrated"}
    _require(
        expected.issubset(variant_names),
        issues,
        "missing_required_variants",
        "Ablation must include base, uncalibrated, and calibrated variants.",
    )
    _require(
        isinstance(summary.get("category_breakdown"), Mapping),
        issues,
        "missing_category_breakdown",
        "Category breakdown is required.",
    )
    _require(
        _mapping(summary.get("systems")).get("xendris_calibrated", {}).get("calibration_metrics"),
        issues,
        "missing_calibration_metrics",
        "Calibrated variant must include calibration metrics.",
    )
    _require(
        _has_no_universal_superiority_warning(report),
        issues,
        "missing_no_universal_superiority_warning",
        "Report must include a no-universal-superiority warning.",
    )
    _require(
        "## limitations" in report or "## limitaciones" in report,
        issues,
        "missing_limitations",
        "Report must include limitations.",
    )
    if _claims_universal_superiority(report):
        _add_blocker(
            issues,
            "universal_superiority_claim",
            "Report contains unsupported universal superiority wording.",
        )
    if _claims_real_provider_performance(report):
        _add_blocker(
            issues,
            "real_provider_performance_claim",
            "Dry-run ablation must not claim real-provider performance.",
        )

    status = "BLOCKED_FOR_INTERPRETATION" if any(i.severity == "BLOCKER" for i in issues) else "ADMITTED_EXPERIMENTAL_ANALYSIS"
    return CalibrationAblationGateAssessment(status=status, issues=tuple(issues))


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _normalize(text: str) -> str:
    return text.lower().replace("_", "-")


def _require(
    condition: object,
    issues: list[CalibrationAblationGateIssue],
    code: str,
    message: str,
) -> None:
    if not condition:
        _add_blocker(issues, code, message)


def _add_blocker(issues: list[CalibrationAblationGateIssue], code: str, message: str) -> None:
    issues.append(CalibrationAblationGateIssue(code=code, severity="BLOCKER", message=message))


def _has_no_universal_superiority_warning(report: str) -> bool:
    return (
        "no universal superiority" in report
        or "no-superioridad universal" in report
        or "no superioridad universal" in report
        or "does not imply universal" in report
        or "no demuestra superioridad universal" in report
    )


def _claims_universal_superiority(report: str) -> bool:
    suspicious = (
        "proves universal superiority",
        "demonstrates universal superiority",
        "shows universal superiority",
        "globally better at programming",
        "mejora programación globalmente",
        "superioridad universal demostrada",
    )
    return any(phrase in report for phrase in suspicious)


def _claims_real_provider_performance(report: str) -> bool:
    suspicious = (
        "real provider performance",
        "real-provider performance",
        "corrida real",
        "proveedor real",
        "real deepseek performance",
    )
    return any(phrase in report for phrase in suspicious)


__all__ = [
    "CalibrationAblationGateAssessment",
    "CalibrationAblationGateIssue",
    "assess_programming_calibration_ablation",
]
