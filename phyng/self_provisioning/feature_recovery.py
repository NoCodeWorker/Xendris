"""Conservative feature recovery attempt for blocked candidate selection."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MASS_PATTERNS = [
    re.compile(r"\b(\d+(?:[.,]\d+)?)\s*(?:amu|AMU|u|Da|kDa)\b"),
    re.compile(r"\b(?:mass|masses|molecular weight)[^\n\r]{0,80}?(\d+(?:[.,]\d+)?)\s*(?:amu|AMU|u|Da|kDa)\b"),
]
SCALE_PATTERNS = [
    re.compile(r"\b(?:grating period|period|separation|Talbot length|path separation|distance)[^\n\r]{0,120}?(\d+(?:[.,]\d+)?)\s*(nm|um|µm|mm|cm|m)\b", re.IGNORECASE),
    re.compile(r"\b(\d+(?:[.,]\d+)?)\s*(nm|um|µm|mm|cm|m)\s+(?:period|separation|distance|grating)\b", re.IGNORECASE),
]
MECHANISM_PATTERNS = [
    re.compile(r"\bthermal(?:ly)?\b|\bheating\b|\bdecoherence\b|\bvelocity\b|\bmolecule\b|\bgrating\b", re.IGNORECASE),
]


@dataclass(frozen=True)
class FeatureRecoverySummary:
    total_records: int
    mass_feature_hints: int
    operational_scale_hints: int
    mechanism_hints: int
    mass_feature_complete: bool
    operational_scale_complete: bool
    shared_numeric_condition_axis_available: bool
    observable_mechanism_class_complete: bool
    c_coordinate_candidate_permitted: bool
    source_agnostic_candidate_permitted: bool
    terminal_status: str


def run_feature_recovery_attempt(root: str | Path = ".") -> dict[str, Any]:
    """Search local hashed source text for non-target features without promoting them."""

    repo_root = Path(root)
    dataset = _load_json(repo_root / "data/frontera_c/master_goal/dataset_v5_7_4_master.json")
    records = dataset.get("records", [])
    recovery_records = [_recover_record_features(repo_root, record) for record in records]
    summary = _summarize(records, recovery_records)
    payload = {
        "status": summary.terminal_status,
        "summary": summary.__dict__,
        "records": recovery_records,
        "blocked_candidate_families": {
            "C_COORDINATE_RESPONSE": [
                "mass_kg not complete for all accepted y_true records",
                "operational_scale_L_m is not justified by a non-ad-hoc rule for all accepted y_true records",
                "lambda_C_m and r_g_m cannot be derived without complete mass_kg",
            ],
            "B_SUPPRESSED": [
                "mass_kg not complete for all accepted y_true records",
                "operational_scale_L_m is not justified by a non-ad-hoc rule for all accepted y_true records",
            ],
            "QB_STRUCTURAL": [
                "operational_scale_L_m remains ad-hoc without a declared scale-selection rule",
            ],
            "SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE": [
                "no shared numeric condition axis spans all accepted y_true records",
                "observable_mechanism_class is not complete with source-local provenance for every record",
            ],
        },
        "forbidden_promotions_avoided": [
            "text hint promotion to selected feature",
            "source identity to evidence",
            "local PDF hash to physical support",
            "feature recovery to PredictiveGain permission",
        ],
    }
    out_dir = repo_root / "data/frontera_c/self_provisioning"
    report_dir = repo_root / "reports/frontera_c/self_provisioning"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "feature_recovery_attempt_v5_9_1.json"
    report_path = report_dir / "feature_recovery_attempt_v5_9_1.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    report_path.write_text(_render_report(payload), encoding="utf-8")
    payload["artifact_paths"] = {
        "json": json_path.relative_to(repo_root).as_posix(),
        "report": report_path.relative_to(repo_root).as_posix(),
    }
    return payload


def _recover_record_features(root: Path, record: dict[str, Any]) -> dict[str, Any]:
    local_pdf_path = record.get("local_pdf_path")
    text = _extract_source_text(root / local_pdf_path) if local_pdf_path else ""
    condition_keys = sorted(k for k in record.get("conditions", {}).keys() if k != "unit")
    mass_hint = _first_match(text, MASS_PATTERNS)
    scale_hint = _first_match(text, SCALE_PATTERNS)
    mechanism_hint = _first_match(text, MECHANISM_PATTERNS)
    return {
        "y_true_id": record.get("y_true_id"),
        "source_id": record.get("source_id"),
        "local_pdf_path": local_pdf_path,
        "local_pdf_hash": record.get("local_pdf_hash"),
        "condition_keys": condition_keys,
        "mass_feature": _feature_state("mass_kg", mass_hint, "AMBIGUOUS_TEXT_HINT" if mass_hint else "MISSING"),
        "operational_scale_feature": _feature_state(
            "operational_scale_L_m",
            scale_hint,
            "TEXT_HINT_REQUIRES_NON_AD_HOC_SCALE_RULE" if scale_hint else "MISSING",
        ),
        "observable_mechanism_feature": _feature_state(
            "observable_mechanism_class",
            mechanism_hint,
            "TEXT_HINT_REQUIRES_CLASSIFICATION_REVIEW" if mechanism_hint else "MISSING",
        ),
        "usable_for_candidate_selection": False,
        "selection_blocker": (
            "Recovered source-text hints are incomplete or require a predeclared theory rule; "
            "they cannot be promoted into leak-free candidate features."
        ),
    }


def _feature_state(feature_name: str, hint: dict[str, Any] | None, status: str) -> dict[str, Any]:
    return {
        "feature_name": feature_name,
        "status": status,
        "value_text": hint.get("value_text") if hint else None,
        "page_number": hint.get("page_number") if hint else None,
        "snippet": hint.get("snippet") if hint else None,
        "usable_for_candidate": False,
    }


def _summarize(records: list[dict[str, Any]], recovery_records: list[dict[str, Any]]) -> FeatureRecoverySummary:
    condition_sets = [tuple(item.get("condition_keys", [])) for item in recovery_records]
    shared_axis = bool(condition_sets) and len(set(condition_sets)) == 1 and bool(condition_sets[0])
    mass_hints = sum(1 for item in recovery_records if item["mass_feature"]["value_text"])
    scale_hints = sum(1 for item in recovery_records if item["operational_scale_feature"]["value_text"])
    mechanism_hints = sum(1 for item in recovery_records if item["observable_mechanism_feature"]["value_text"])
    total = len(records)
    return FeatureRecoverySummary(
        total_records=total,
        mass_feature_hints=mass_hints,
        operational_scale_hints=scale_hints,
        mechanism_hints=mechanism_hints,
        mass_feature_complete=False,
        operational_scale_complete=False,
        shared_numeric_condition_axis_available=shared_axis,
        observable_mechanism_class_complete=False,
        c_coordinate_candidate_permitted=False,
        source_agnostic_candidate_permitted=False,
        terminal_status="FEATURE_RECOVERY_ATTEMPTED_SELECTION_STILL_BLOCKED",
    )


def _extract_source_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        import fitz  # type: ignore

        with fitz.open(path) as doc:
            return "\f".join(page.get_text("text") for page in doc)
    except Exception:
        return ""


def _first_match(text: str, patterns: list[re.Pattern[str]]) -> dict[str, Any] | None:
    if not text:
        return None
    pages = text.split("\f") if "\f" in text else [text]
    for page_index, page_text in enumerate(pages, start=1):
        normalized = " ".join(page_text.split())
        for pattern in patterns:
            match = pattern.search(normalized)
            if match:
                start = max(match.start() - 80, 0)
                end = min(match.end() + 80, len(normalized))
                return {
                    "value_text": match.group(0),
                    "page_number": page_index,
                    "snippet": normalized[start:end],
                }
    return None


def _render_report(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Feature Recovery Attempt v5.9.1",
        "",
        f"Status: `{payload['status']}`",
        f"Total y_true records reviewed: `{summary['total_records']}`",
        f"Mass text hints: `{summary['mass_feature_hints']}`",
        f"Operational scale text hints: `{summary['operational_scale_hints']}`",
        f"Mechanism text hints: `{summary['mechanism_hints']}`",
        f"C-coordinate candidate permitted: `{summary['c_coordinate_candidate_permitted']}`",
        f"Source-agnostic candidate permitted: `{summary['source_agnostic_candidate_permitted']}`",
        "",
        "## Decision",
        "",
        "Feature recovery did not remove the v5.9 blocker. Text hints remain incomplete, ambiguous, or dependent on a non-ad-hoc theory rule.",
        "",
        "No PredictiveGain was computed. No candidate was selected. No physical claim was upgraded.",
    ]
    return "\n".join(lines) + "\n"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
