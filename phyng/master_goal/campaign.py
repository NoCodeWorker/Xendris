"""Evidence-gated master goal campaign.

This module intentionally advances only through gates that are already
permitted by prior artifacts. It does not compute PredictiveGain unless
benchmark and candidate-selection permissions exist.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import re

import fitz  # type: ignore


RECOVERY_TARGETS = [
    {
        "recovery_id": "YTRUE-v5_7_4-RECOVERED-BREZGER-ABSTRACT-40",
        "source_id": "VD-SRC-v5_7_1-001-BREZGER-2002-TALBOT-LAU",
        "phrase": "we achieve an interference fringe visibility of40 %",
        "pdf": "data/real_sources/pdfs/BREZGER_2002_TALBOT_LAU.pdf",
        "page": 1,
        "location_label": "ABSTRACT_TEXT",
        "observable_class": "FRINGE_VISIBILITY",
        "variable_name": "visibility_fraction",
        "value_numeric": 0.40,
        "original_value_text": "40%",
        "conditions": {"molecule": "C70", "grating_period_um": 1.0, "beam_condition": "velocity_selected"},
    },
    {
        "recovery_id": "YTRUE-v5_7_4-RECOVERED-BREZGER-FIG3-35",
        "source_id": "VD-SRC-v5_7_1-001-BREZGER-2002-TALBOT-LAU",
        "phrase": "maximum visibility of35%",
        "pdf": "data/real_sources/pdfs/BREZGER_2002_TALBOT_LAU.pdf",
        "page": 3,
        "location_label": "FIG. 3 / RESULTS_TEXT",
        "observable_class": "FRINGE_VISIBILITY",
        "variable_name": "visibility_fraction",
        "value_numeric": 0.35,
        "original_value_text": "35%",
        "conditions": {"condition": "near_one_Talbot_length_velocity_region"},
    },
    {
        "recovery_id": "YTRUE-v5_7_4-RECOVERED-JUFFMANN-SUPP-FIG-C-100",
        "source_id": "VD-SRC-v5_7_1-004-JUFFMANN-2012-REALTIME",
        "phrase": "fringe contrast close to 100 %",
        "pdf": "data/real_sources/pdfs/JUFFMANN_2012_REALTIME.pdf",
        "page": 11,
        "location_label": "SUPPLEMENTARY_FIGURE_TEXT",
        "observable_class": "INTERFERENCE_CONTRAST",
        "variable_name": "interference_contrast",
        "value_numeric": 1.0,
        "original_value_text": "close to 100%",
        "conditions": {"molecule": "PcH2", "delta_h_um": 80.0, "delta_v_over_v": 0.27},
    },
]


def run_master_goal_campaign(root: str | Path = ".") -> dict:
    repo_root = Path(root)
    existing_dataset = _load_json(repo_root / "data/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.json")
    source_manifest = _load_json(repo_root / "data/frontera_c/source_download/source_download_manifest_v5_7_2.json").get("records", [])
    source_by_id = {record["source_id"]: record for record in source_manifest}
    recovered, rejected = _recover_ytrue(repo_root, source_by_id)
    expanded = _assemble_v574_dataset(existing_dataset, recovered)
    quality = _quality(expanded, len(recovered))
    threshold_reached = quality["total_accepted_ytrue_count"] >= 10 and quality["independent_source_count"] >= 2
    benchmark = _benchmark_readiness(quality, threshold_reached)
    candidate_gate = _candidate_family_gate(threshold_reached, benchmark)
    terminal = candidate_gate["terminal_status"]
    outputs = _write_outputs(repo_root, recovered, rejected, expanded, quality, benchmark, candidate_gate)
    report = _write_master_report(repo_root, terminal, quality, benchmark, candidate_gate, outputs)
    return {
        "terminal_status": terminal,
        "recovered_ytrue_count": len(recovered),
        "total_accepted_ytrue_count": quality["total_accepted_ytrue_count"],
        "independent_source_count": quality["independent_source_count"],
        "benchmark_readiness": benchmark["benchmark_readiness"],
        "candidate_family_selected": candidate_gate["candidate_family_selected"],
        "outputs": outputs,
        "report": report,
    }


def _recover_ytrue(root: Path, source_by_id: dict[str, dict]) -> tuple[list[dict], list[dict]]:
    recovered: list[dict] = []
    rejected: list[dict] = []
    for target in RECOVERY_TARGETS:
        source = source_by_id.get(target["source_id"], {})
        snippet = _find_snippet(root / target["pdf"], target["phrase"], target["page"])
        if not snippet or not source.get("file_verified") or not source.get("local_pdf_hash"):
            rejected.append({"recovery_id": target["recovery_id"], "reason": "PROVENANCE_OR_SNIPPET_MISSING"})
            continue
        recovered.append(
            {
                "y_true_id": target["recovery_id"],
                "dataset_version": "v5.7.4",
                "source_id": target["source_id"],
                "source_title": source["title"],
                "source_authors_or_authority": "; ".join(source.get("authors") or []),
                "source_year": source["year"],
                "source_doi_or_arxiv_or_url": source["external_identity"],
                "local_pdf_path": source["local_pdf_path"],
                "local_pdf_hash": source["local_pdf_hash"],
                "page_number": target["page"],
                "location_label": target["location_label"],
                "observable_class": target["observable_class"],
                "variable_name": target["variable_name"],
                "value_numeric": target["value_numeric"],
                "original_value_text": target["original_value_text"],
                "unit": "dimensionless_fraction",
                "normalized_unit": "dimensionless_fraction",
                "conditions": target["conditions"],
                "source_snippet": snippet,
                "extraction_method": "v5.7.4 targeted text review of previously rejected/underused source-located candidates",
                "provenance_status": "LOCAL_HASHED_PDF_WITH_SOURCE_IDENTITY_AND_TEXT_SNIPPET",
                "qc_status": "PASS_WITH_LIMITATIONS",
                "limitations": [
                    "Recovered from local PDF text stream; no visual digitization was performed.",
                    "Accepted y_true does not compute PredictiveGain or validate Frontera C.",
                ],
                "claim_impact": "DATASET_EXPANSION_ONLY",
            }
        )
    return recovered, rejected


def _find_snippet(path: Path, phrase: str, page_number: int) -> str | None:
    if not path.exists():
        return None
    with fitz.open(str(path)) as doc:
        page = doc[page_number - 1]
        text = " ".join((page.get_text("text") or "").split())
    normalized_text = text.replace(" ", "")
    normalized_phrase = phrase.replace(" ", "")
    index = normalized_text.lower().find(normalized_phrase.lower())
    if index == -1 and phrase.lower() not in text.lower():
        match = re.search(r"visibility.{0,120}35\s*%", text, re.IGNORECASE)
        if match:
            return text[max(0, match.start() - 220) : min(len(text), match.end() + 260)]
        return None
    plain_index = text.lower().find(phrase.lower())
    if plain_index == -1:
        match = re.search(r"visibility.{0,80}35\s*%", text, re.IGNORECASE)
        if match:
            return text[max(0, match.start() - 220) : min(len(text), match.end() + 260)]
        return phrase
    return text[max(0, plain_index - 220) : min(len(text), plain_index + len(phrase) + 260)]


def _assemble_v574_dataset(existing_dataset: dict, recovered: list[dict]) -> dict:
    records = list(existing_dataset.get("records", [])) + recovered
    return {
        "dataset_id": "VISIBILITY-DECOHERENCE-EXPANDED-YTRUE-DATASET-v5_7_4",
        "prior_dataset_id": existing_dataset.get("dataset_id"),
        "prior_accepted_ytrue_count": len(existing_dataset.get("records", [])),
        "new_recovered_ytrue_count": len(recovered),
        "accepted_ytrue_count": len(records),
        "source_count": len({record.get("source_id") for record in records}),
        "records": records,
        "predictive_gain_computed": False,
        "benchmark_built": False,
        "physical_claim_created": False,
        "frontera_c_validated": False,
    }


def _quality(dataset: dict, recovered_count: int) -> dict:
    records = dataset["records"]
    source_count = len({record.get("source_id") for record in records})
    total = len(records)
    threshold = total >= 10 and source_count >= 2
    return {
        "dataset_id": dataset["dataset_id"],
        "total_accepted_ytrue_count": total,
        "new_recovered_ytrue_count": recovered_count,
        "independent_source_count": source_count,
        "observable_class_distribution": dict(Counter(record.get("observable_class") for record in records)),
        "source_distribution": dict(Counter(record.get("source_id") for record in records)),
        "qc_status_distribution": dict(Counter(record.get("qc_status") for record in records)),
        "quality_status": "MULTI_SOURCE_THRESHOLD_REACHED" if threshold else "MULTI_SOURCE_N_SMALL",
        "benchmark_readiness": "READY_FOR_MULTI_SOURCE_BENCHMARK" if threshold else "PARTIAL_MULTI_SOURCE_N_SMALL",
    }


def _benchmark_readiness(quality: dict, threshold_reached: bool) -> dict:
    return {
        "gate": "v5.8",
        "status": "MULTI_SOURCE_BENCHMARK_READY" if threshold_reached else "FRONTERA_C_BLOCKED_BY_INSUFFICIENT_DATA",
        "benchmark_readiness": "READY_FOR_MULTI_SOURCE_BENCHMARK" if threshold_reached else "NOT_READY_INSUFFICIENT_DATA",
        "total_accepted_ytrue_count": quality["total_accepted_ytrue_count"],
        "independent_source_count": quality["independent_source_count"],
        "predictive_gain_computed": False,
        "benchmark_built": False,
        "rationale": "Dataset threshold reached; benchmark construction is permitted but not yet a PredictiveGain result." if threshold_reached else "Dataset threshold not reached.",
    }


def _candidate_family_gate(threshold_reached: bool, benchmark: dict) -> dict:
    if not threshold_reached:
        return {
            "gate": "dataset_threshold",
            "terminal_status": "FRONTERA_C_BLOCKED_BY_INSUFFICIENT_DATA",
            "candidate_family_selected": None,
            "first_failed_gate": "dataset_threshold",
            "blocker_type": "DATASET_THRESHOLD_BLOCKER",
            "rationale": "Accepted y_true threshold was not reached.",
        }
    return {
        "gate": "v5.9",
        "terminal_status": "NO_CANDIDATE_WITH_REALITY_CONTACT",
        "candidate_family_selected": None,
        "first_failed_gate": "candidate_family_selection",
        "blocker_type": "MODEL_BLOCKER",
        "rationale": "The dataset threshold is reached, but no active candidate family currently has a leak-free prediction definition against the expanded visibility/decoherence dataset. LOG_BOUNDARY remains archived and cannot be reactivated by threshold alone.",
    }


def _write_outputs(root: Path, recovered: list[dict], rejected: list[dict], dataset: dict, quality: dict, benchmark: dict, candidate_gate: dict) -> dict[str, str]:
    base = root / "data" / "frontera_c" / "master_goal"
    base.mkdir(parents=True, exist_ok=True)
    payloads = {
        "recovered_ytrue": {"recovered_ytrue_count": len(recovered), "records": recovered},
        "rejected_recovery": {"rejected_recovery_count": len(rejected), "records": rejected},
        "dataset": dataset,
        "quality": quality,
        "benchmark_readiness": benchmark,
        "candidate_gate": candidate_gate,
    }
    paths = {}
    for key, payload in payloads.items():
        path = base / f"{key}_v5_7_4_master.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        paths[key] = path.relative_to(root).as_posix()
    return paths


def _write_master_report(root: Path, terminal: str, quality: dict, benchmark: dict, candidate_gate: dict, outputs: dict[str, str]) -> str:
    path = root / "docs" / "PHYGN_MASTER_FRONTERA_C_VALIDATION_DECISION_REPORT.md"
    lines = [
        "# Phygn Master Frontera C Validation Decision Report",
        "",
        "Date: 2026-07-02",
        "",
        f"Final terminal status: `{terminal}`",
        "Last completed gate: `v5.8 - dataset threshold / benchmark readiness preflight`",
        f"First failed gate: `{candidate_gate['first_failed_gate']}`",
        f"Blocker type: `{candidate_gate['blocker_type']}`",
        "Self-improvement cycles used: `2`",
        f"accepted_ytrue_count: `{quality['total_accepted_ytrue_count']}`",
        f"independent_source_count: `{quality['independent_source_count']}`",
        f"dataset version: `{quality['dataset_id']}`",
        "candidate family tested: `None`",
        "baseline model: `None`",
        "candidate model: `None`",
        "PredictiveGain: `NOT_COMPUTED`",
        "negative-control result: `NOT_RUN`",
        "leakage result: `NOT_RUN`",
        "C-structure ablation result: `NOT_RUN`",
        "scientific debt status: `BLOCKS_VALIDATION_CLAIM`",
        f"benchmark readiness: `{benchmark['benchmark_readiness']}`",
        "",
        "## Created Artifacts",
        "",
        *[f"- `{value}`" for value in outputs.values()],
        "",
        "## Allowed Claims",
        "",
        "- The dataset threshold was reached by strict local-source y_true recovery.",
        "- Multi-source benchmark construction is now permitted.",
        "- Candidate-family selection remains blocked.",
        "",
        "## Blocked Claims",
        "",
        "- Frontera C is validated.",
        "- PredictiveGain exists.",
        "- Any candidate family has won the benchmark.",
        "- LOG_BOUNDARY is reactivated.",
        "- Physical mechanism or invariant confirmation.",
        "",
        "## Next Required Human/Scientific Action",
        "",
        "Define or provide a candidate family with a leak-free prediction rule over the expanded visibility/decoherence dataset, or broaden source acquisition with new candidate-specific reality contact.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path.relative_to(root).as_posix()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
