"""v5.9.3 targeted expansion for the heating-power condition axis."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from phyng.core.report_contract import append_canonical_status_section, build_report_contract


POWER_TERMS = re.compile(r"\b(heating power|laser heating|heated|heating|thermal emission|laser power|power\s*of|[0-9]+(?:\.[0-9]+)?\s*W)\b", re.I)
OBSERVABLE_TERMS = re.compile(r"\b(visibility|contrast|interferogram|interference|fringe)\b", re.I)
STRICT_HEATING_TERMS = re.compile(r"\b(heating power|laser heating|thermal emission|increasing laser heating powers)\b", re.I)
WRONG_CONTEXT_TERMS = re.compile(
    r"\b(ioniz|detection|posterior|prior|model|simulation|constraint|constraints|future\s*experim|future\s+experiment|negligible|not\s+play)\b",
    re.I,
)


def run_heating_power_axis_expansion(root: str | Path = ".") -> dict[str, Any]:
    repo_root = Path(root)
    dataset = _load_json(repo_root / "data/frontera_c/master_goal/dataset_v5_7_4_master.json")
    source_manifest = _load_source_manifest(repo_root)
    existing_axis_records = _existing_heating_axis_records(dataset.get("records", []))
    local_scan_records = _scan_local_pdfs(repo_root, source_manifest, existing_axis_records)
    acquisition_queue = _build_acquisition_queue(existing_axis_records, local_scan_records)
    decision = _build_decision(existing_axis_records, local_scan_records, acquisition_queue)
    return {
        "axis_name": "heating_power_W",
        "record_count_before": len(existing_axis_records),
        "independent_source_count_before": len({item["source_id"] for item in existing_axis_records}),
        "existing_axis_records": existing_axis_records,
        "local_scan_records": local_scan_records,
        "acquisition_queue": acquisition_queue,
        "decision": decision,
        "forbidden_actions_avoided": [
            "laser detection power reclassified as heating_power_W",
            "theory/model posterior reclassified as observed visibility",
            "single-source axis promoted to PredictiveGain",
            "local text hint accepted as y_true without strict QC",
        ],
    }


def write_heating_power_axis_outputs(root: str | Path, payload: dict[str, Any]) -> dict[str, str]:
    repo_root = Path(root)
    data_dir = repo_root / "data/frontera_c/candidates"
    report_dir = repo_root / "reports/frontera_c/candidates"
    campaign_dir = repo_root / "reports/campaigns"
    docs_dir = repo_root / "docs"
    data_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "expansion_json": data_dir / "heating_power_axis_expansion_v5_9_3.json",
        "local_scan_json": data_dir / "heating_power_axis_local_scan_v5_9_3.json",
        "acquisition_queue_json": data_dir / "heating_power_axis_acquisition_queue_v5_9_3.json",
        "next_gate_json": data_dir / "heating_power_axis_next_gate_v5_9_3.json",
        "expansion_report": report_dir / "heating_power_axis_expansion_v5_9_3.md",
        "campaign_report": campaign_dir / "FRONTERA-C-HEATING-POWER-AXIS-EXPANSION-v5_9_3.md",
        "final_doc": docs_dir / "381_PHYGN_V5_9_3_TARGETED_HEATING_POWER_AXIS_EXPANSION_RESULTS.md",
    }
    paths["expansion_json"].write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    paths["local_scan_json"].write_text(
        json.dumps({"records": payload["local_scan_records"]}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    paths["acquisition_queue_json"].write_text(
        json.dumps({"records": payload["acquisition_queue"]}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    paths["next_gate_json"].write_text(json.dumps(payload["decision"], indent=2, sort_keys=True), encoding="utf-8")
    paths["expansion_report"].write_text(_canonical(_render_expansion_report(payload), payload), encoding="utf-8")
    paths["campaign_report"].write_text(_canonical(_render_campaign_report(payload), payload), encoding="utf-8")
    paths["final_doc"].write_text(_canonical(_render_final_doc(payload), payload), encoding="utf-8")
    return {key: path.relative_to(repo_root).as_posix() for key, path in paths.items()}


def _existing_heating_axis_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for record in records:
        conditions = record.get("conditions") or {}
        if "heating_power_W" not in conditions:
            continue
        output.append(
            {
                "y_true_id": record.get("y_true_id"),
                "source_id": record.get("source_id"),
                "local_pdf_hash": record.get("local_pdf_hash"),
                "local_pdf_path": record.get("local_pdf_path"),
                "page_number": record.get("page_number"),
                "location_label": record.get("location_label"),
                "heating_power_W": conditions.get("heating_power_W"),
                "observable_class": record.get("observable_class"),
                "variable_name": record.get("variable_name"),
                "value_numeric": record.get("value_numeric"),
                "unit": record.get("unit"),
                "qc_status": record.get("qc_status"),
                "record_status": "ACCEPTED_SEED_HEATING_POWER_YTRUE",
            }
        )
    return output


def _scan_local_pdfs(
    repo_root: Path,
    source_manifest: dict[str, dict[str, Any]],
    existing_axis_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    pages = _extract_pdf_pages(repo_root / "data/real_sources/pdfs")
    existing_hashes = {item.get("local_pdf_hash") for item in existing_axis_records}
    records = []
    for pdf_path, page_number, text in pages:
        normalized = " ".join(text.split())
        if not (POWER_TERMS.search(normalized) and OBSERVABLE_TERMS.search(normalized)):
            continue
        sha256 = _sha256(pdf_path)
        source = source_manifest.get(pdf_path.as_posix()) or source_manifest.get(str(pdf_path).replace("\\", "/")) or {}
        status, reason = _classify_hit(normalized, sha256 in existing_hashes)
        records.append(
            {
                "scan_id": f"HPAXIS-v5_9_3-SCAN-{len(records)+1:03d}",
                "source_id": source.get("source_id") or source.get("source_candidate_id") or pdf_path.stem,
                "source_title": source.get("title") or pdf_path.stem,
                "local_pdf_path": pdf_path.as_posix(),
                "local_pdf_hash": sha256,
                "page_number": page_number,
                "scan_status": status,
                "rejection_or_review_reason": reason,
                "contains_power_term": True,
                "contains_observable_term": True,
                "strict_heating_context": bool(STRICT_HEATING_TERMS.search(normalized)),
                "snippet": _snippet(normalized),
                "usable_as_new_ytrue": False,
            }
        )
    return records


def _classify_hit(text: str, is_existing_seed_source: bool) -> tuple[str, str]:
    if is_existing_seed_source and STRICT_HEATING_TERMS.search(text):
        return "EXISTING_SEED_SOURCE_ALREADY_ACCEPTED", "Heating-power y_true already exists from this source."
    if "laser power" in text.lower() or "powerof" in text.lower() or "power of" in text.lower():
        return "REJECTED_WRONG_AXIS_OR_CONTEXT", "Laser/detection power is not automatically heating_power_W."
    if WRONG_CONTEXT_TERMS.search(text):
        return "REJECTED_MODEL_OR_CONTEXT_ONLY", "Context is model, detector, future-work, or non-observed-axis material."
    if STRICT_HEATING_TERMS.search(text):
        return "REQUIRES_STRICT_YTRUE_REVIEW", "Strict heating context found, but no automated v5.9.3 y_true acceptance is allowed."
    return "CONTEXT_ONLY_REQUIRES_HUMAN_REVIEW", "Power and observable terms co-occur but axis mapping is not strict."


def _build_acquisition_queue(
    existing_axis_records: list[dict[str, Any]],
    local_scan_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    existing_sources = sorted({item["source_id"] for item in existing_axis_records})
    review_candidates = [item for item in local_scan_records if item["scan_status"] == "REQUIRES_STRICT_YTRUE_REVIEW"]
    queue = [
        {
            "task_id": "HPAXIS-v5_9_3-ACQUIRE-001-INDEPENDENT-HEATING-POWER-SOURCE",
            "axis_name": "heating_power_W",
            "priority": "CRITICAL",
            "required_source_independence": f"Must not be any of: {', '.join(existing_sources)}",
            "required_observable": "visibility_fraction or interference_contrast observed as a function of heating_power_W",
            "required_provenance": "complete source identity plus local hash or exact external provenance",
            "required_location": "page/table/figure/section containing power values and observed visibility/contrast values",
            "status": "TARGETED_SOURCE_ACQUISITION_REQUIRED",
            "reason": "Current heating_power_W axis has adequate record count but only one independent source.",
        }
    ]
    if review_candidates:
        queue.append(
            {
                "task_id": "HPAXIS-v5_9_3-REVIEW-002-LOCAL-STRICT-CANDIDATES",
                "axis_name": "heating_power_W",
                "priority": "HIGH",
                "candidate_scan_ids": [item["scan_id"] for item in review_candidates],
                "status": "STRICT_MANUAL_REVIEW_REQUIRED",
                "reason": "Local text scan found strict heating context outside automatically accepted seed records.",
            }
        )
    return queue


def _build_decision(
    existing_axis_records: list[dict[str, Any]],
    local_scan_records: list[dict[str, Any]],
    acquisition_queue: list[dict[str, Any]],
) -> dict[str, Any]:
    accepted_sources = {item["source_id"] for item in existing_axis_records}
    accepted_count = len(existing_axis_records)
    independent_source_count = len(accepted_sources)
    strict_review_candidates = [item for item in local_scan_records if item["scan_status"] == "REQUIRES_STRICT_YTRUE_REVIEW"]
    threshold_reached = accepted_count >= 6 and independent_source_count >= 2
    if threshold_reached:
        status = "HEATING_POWER_AXIS_EXPANSION_THRESHOLD_REACHED"
        allowed_next_phase = "v5.9.4 - SOURCE_AGNOSTIC_DECOHERENCE_RESPONSE candidate rule formulation"
        blocker = None
    elif strict_review_candidates:
        status = "HEATING_POWER_AXIS_EXPANSION_REQUIRES_STRICT_REVIEW"
        allowed_next_phase = None
        blocker = "Local scan found possible heating-power candidates, but strict y_true review is required before axis expansion."
    else:
        status = "HEATING_POWER_AXIS_EXPANSION_REQUIRES_TARGETED_SOURCE_ACQUISITION"
        allowed_next_phase = None
        blocker = "No independent accepted y_true records on heating_power_W were added from local sources."
    return {
        "final_status": status,
        "axis_name": "heating_power_W",
        "accepted_heating_power_ytrue_count": accepted_count,
        "accepted_heating_power_source_count": independent_source_count,
        "new_accepted_ytrue_count": 0,
        "local_scan_record_count": len(local_scan_records),
        "strict_review_candidate_count": len(strict_review_candidates),
        "acquisition_task_count": len(acquisition_queue),
        "threshold_reached": threshold_reached,
        "selected_candidate_family": None,
        "v6_0_permitted": False,
        "predictive_gain_permitted": False,
        "allowed_next_phase": allowed_next_phase,
        "blocker": blocker,
        "next_required_action": (
            "Acquire or manually extract an independent source with observed visibility/contrast versus heating_power_W."
        ),
    }


def _load_source_manifest(repo_root: Path) -> dict[str, dict[str, Any]]:
    manifests = [
        repo_root / "data/frontera_c/source_download/source_download_manifest_v5_7_2.json",
    ]
    by_path: dict[str, dict[str, Any]] = {}
    for manifest_path in manifests:
        data = _load_json(manifest_path)
        for record in data.get("records", []):
            local_path = record.get("local_pdf_path")
            if local_path:
                by_path[Path(local_path).as_posix()] = record
                by_path[(repo_root / local_path).as_posix()] = record
    return by_path


def _extract_pdf_pages(pdf_dir: Path) -> list[tuple[Path, int, str]]:
    try:
        import fitz  # type: ignore
    except Exception:
        return []
    pages: list[tuple[Path, int, str]] = []
    for path in sorted(pdf_dir.glob("*.pdf")):
        try:
            with fitz.open(path) as doc:
                for index, page in enumerate(doc, start=1):
                    pages.append((path, index, page.get_text("text") or ""))
        except Exception:
            continue
    return pages


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _snippet(text: str) -> str:
    power = POWER_TERMS.search(text)
    observable = OBSERVABLE_TERMS.search(text)
    positions = [match.start() for match in [power, observable] if match]
    start = max(min(positions) - 180, 0) if positions else 0
    return text[start : start + 720]


def _render_expansion_report(payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    lines = [
        "# Heating-Power Axis Expansion v5.9.3",
        "",
        f"Final status: `{decision['final_status']}`",
        f"Accepted heating-power y_true: `{decision['accepted_heating_power_ytrue_count']}`",
        f"Accepted heating-power source count: `{decision['accepted_heating_power_source_count']}`",
        f"New accepted y_true: `{decision['new_accepted_ytrue_count']}`",
        f"Local scan records: `{decision['local_scan_record_count']}`",
        f"Strict review candidates: `{decision['strict_review_candidate_count']}`",
        "",
        "| Scan status | Count |",
        "|---|---:|",
    ]
    counts: dict[str, int] = {}
    for record in payload["local_scan_records"]:
        counts[record["scan_status"]] = counts.get(record["scan_status"], 0) + 1
    for status, count in sorted(counts.items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "No PredictiveGain was computed. No candidate was selected."])
    return "\n".join(lines) + "\n"


def _render_campaign_report(payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    return "\n".join(
        [
            "# Campaign Report - FRONTERA-C-HEATING-POWER-AXIS-EXPANSION-v5_9_3",
            "",
            f"- status: `{decision['final_status']}`",
            f"- axis_name: `{decision['axis_name']}`",
            f"- accepted_heating_power_ytrue_count: `{decision['accepted_heating_power_ytrue_count']}`",
            f"- accepted_heating_power_source_count: `{decision['accepted_heating_power_source_count']}`",
            f"- new_accepted_ytrue_count: `{decision['new_accepted_ytrue_count']}`",
            f"- v6_0_permitted: `{decision['v6_0_permitted']}`",
            f"- predictive_gain_permitted: `{decision['predictive_gain_permitted']}`",
        ]
    ) + "\n"


def _render_final_doc(payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    lines = [
        "# Phygn v5.9.3 - Targeted Heating-Power Axis Expansion Results",
        "",
        "Date: 2026-07-02",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{decision['final_status']}`",
        f"Axis: `{decision['axis_name']}`",
        f"Accepted heating-power y_true count: `{decision['accepted_heating_power_ytrue_count']}`",
        f"Accepted heating-power independent source count: `{decision['accepted_heating_power_source_count']}`",
        f"New accepted y_true count: `{decision['new_accepted_ytrue_count']}`",
        f"v6.0 permitted: `{decision['v6_0_permitted']}`",
        f"PredictiveGain permitted: `{decision['predictive_gain_permitted']}`",
        "",
        "## Interpretation",
        "",
        decision["blocker"] or "Heating-power axis threshold was reached.",
        "",
        "## Next Required Action",
        "",
        decision["next_required_action"],
        "",
        "## Blocked Claims",
        "",
        "- Frontera C is validated.",
        "- PredictiveGain exists.",
        "- Heating-power axis is multi-source ready.",
        "- Laser detection power equals heating_power_W.",
        "- Local text scan equals accepted y_true.",
        "",
        "Final discipline:",
        "",
        "```txt",
        "Same-axis expansion requires independent observed y_true.",
        "Power text is not heating-power y_true.",
        "```",
    ]
    return "\n".join(lines) + "\n"


def _canonical(markdown: str, payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    contract = build_report_contract(
        title="Targeted Heating-Power Axis Expansion v5.9.3",
        campaign_id="FRONTERA-C-HEATING-POWER-AXIS-EXPANSION-v5_9_3",
        domain_status=decision["final_status"],
        domain="heating_power_axis_expansion",
        next_actions=[decision["next_required_action"]],
        discipline_note="Axis expansion is dataset preparation, not scoring.",
    )
    return append_canonical_status_section(markdown, contract)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
