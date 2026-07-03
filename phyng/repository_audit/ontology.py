"""Core ontology and state consistency audit."""

from __future__ import annotations

from pathlib import Path

from phyng.repository_audit.schemas import StateFamilyRecord
from phyng.repository_audit.structure import parse_python, py_files, status_literals


STATE_FAMILIES = [
    "EpistemicMode",
    "RiskLevel",
    "FrictionLevel",
    "LadderLevel",
    "TruthBoundaryStatus",
    "PermissionLevel",
    "ClaimStatus",
    "ActionStatus",
    "EvidenceLevel",
    "SourceSupportStatus",
    "BenchmarkStatus",
    "DetectabilityStatus",
    "CandidateSurvivalStatus",
    "FailureConditionStatus",
    "PredictionStatus",
    "CalibrationStatus",
    "BusinessValidationStatus",
    "WTPLevel",
    "ChannelValidationLevel",
    "UnitEconomicsStatus",
    "BusinessRiskStatus",
]

ALIASES = {
    "WTPLevel": ["WTPLevel", "WillingnessToPayLevel"],
    "PermissionLevel": ["PermissionLevel", "BusinessPermissionLevel"],
    "ChannelValidationLevel": ["ChannelValidationLevel"],
}


def audit_core_ontology(root: Path) -> list[StateFamilyRecord]:
    root = Path(root)
    py_paths = py_files(root)
    report_paths = sorted((root / "reports").rglob("*.md"))
    test_paths = sorted((root / "tests").glob("test_*.py"))
    records: list[StateFamilyRecord] = []

    file_texts = {
        str(path.relative_to(root)).replace("\\", "/"): path.read_text(encoding="utf-8", errors="ignore")
        for path in py_paths
    }
    report_texts = {
        str(path.relative_to(root)).replace("\\", "/"): path.read_text(encoding="utf-8", errors="ignore")
        for path in report_paths
    }
    test_texts = {
        str(path.relative_to(root)).replace("\\", "/"): path.read_text(encoding="utf-8", errors="ignore")
        for path in test_paths
    }

    string_only = _likely_string_only_statuses(root)

    for family in STATE_FAMILIES:
        names = ALIASES.get(family, [family])
        definitions: list[str] = []
        consumers: list[str] = []
        producers: list[str] = []
        tests: list[str] = []
        reports: list[str] = []
        representation = "missing"

        for rel, text in file_texts.items():
            for name in names:
                if f"{name} =" in text or f"class {name}" in text:
                    definitions.append(rel)
                    representation = "enum_or_literal"
                if name in text:
                    consumers.append(rel)
                if any(token in rel for token in ("schemas.py", "gatekeeper.py", "report.py")) and name in text:
                    producers.append(rel)
        for rel, text in test_texts.items():
            if any(name in text for name in names):
                tests.append(rel)
        for rel, text in report_texts.items():
            if any(name in text for name in names):
                reports.append(rel)

        warnings: list[str] = []
        unique_definitions = sorted(set(definitions))
        if not unique_definitions:
            warnings.append("State family not explicitly defined; may be string-only or absent.")
        if len(unique_definitions) > 1:
            warnings.append("Multiple definitions detected; canonicalization map recommended.")
        if not tests and unique_definitions:
            warnings.append("Definition found without direct test references.")

        records.append(
            StateFamilyRecord(
                state_family=family,
                definitions=unique_definitions,
                consumers=sorted(set(consumers)),
                producers=sorted(set(producers)),
                serialized_in_reports=sorted(set(reports)),
                tests=sorted(set(tests)),
                is_canonical=len(unique_definitions) == 1,
                representation=representation,
                likely_string_only_statuses=string_only.get(family, []),
                warnings=warnings,
            )
        )

    return records


def _likely_string_only_statuses(root: Path) -> dict[str, list[str]]:
    buckets: dict[str, set[str]] = {family: set() for family in STATE_FAMILIES}
    for path in py_files(root):
        tree = parse_python(path)
        if tree is None:
            continue
        for token in status_literals(tree):
            family = _family_for_token(token)
            if family:
                buckets[family].add(token)
    return {family: sorted(values) for family, values in buckets.items() if values}


def _family_for_token(token: str) -> str | None:
    if token.startswith("RISK_"):
        return "RiskLevel"
    if token.startswith("FRICTION_"):
        return "FrictionLevel"
    if token.startswith("WTP_"):
        return "WTPLevel"
    if token.startswith("CHANNEL_"):
        return "ChannelValidationLevel"
    if token.startswith("UNIT_ECONOMICS_"):
        return "UnitEconomicsStatus"
    if token.startswith("BUSINESS_"):
        return "BusinessValidationStatus"
    if token.startswith("CLAIM_"):
        return "ClaimStatus"
    if token.startswith(("ACTION_", "EXECUTION_")):
        return "ActionStatus"
    if "DETECTABLE" in token:
        return "DetectabilityStatus"
    if token.startswith(("FAIL_", "PASS_")):
        return "FailureConditionStatus"
    return None
