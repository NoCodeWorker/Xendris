"""Observable candidate construction for v5.7.2."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.observable_location.location_classifier import (
    ALLOWED_CLASSES,
    classify_snippet,
    find_figure_id,
    find_table_id,
    matches_observable,
    snippet_windows,
)
from phyng.observable_location.pdf_text_scan import extract_pages
from phyng.observable_location.schemas import TargetedObservableLocationCandidate


def build_observable_location_records(root: str | Path = ".") -> tuple[list[TargetedObservableLocationCandidate], list[TargetedObservableLocationCandidate], list[TargetedObservableLocationCandidate]]:
    repo_root = Path(root)
    source_manifest = _load_records(repo_root / "data/frontera_c/source_download/source_download_manifest_v5_7_2.json")
    targets = _load_records(repo_root / "data/frontera_c/source_acquisition/visibility_decoherence_observable_target_matrix_v5_7_1.json")
    targets_by_source: dict[str, list[dict]] = {}
    for target in targets:
        targets_by_source.setdefault(target["source_candidate_id"], []).append(target)

    candidates: list[TargetedObservableLocationCandidate] = []
    for source in source_manifest:
        if not source.get("file_verified"):
            continue
        local_path = repo_root / source["local_pdf_path"]
        pages = extract_pages(local_path)
        for target in targets_by_source.get(source["source_candidate_id"], []):
            observable_class = target["target_observable_class"]
            if observable_class not in ALLOWED_CLASSES:
                continue
            for page in pages:
                if not matches_observable(observable_class, page.text):
                    continue
                for snippet_index, snippet in enumerate(snippet_windows(page.text, observable_class), start=1):
                    classification, numeric, unit, blockers, next_action = classify_snippet(observable_class, snippet)
                    figure_id = find_figure_id(snippet)
                    table_id = find_table_id(snippet)
                    section_id = None if figure_id or table_id else "TEXT_SCAN"
                    candidates.append(
                        TargetedObservableLocationCandidate(
                            location_id=f"LOC-v5_7_2-{len(candidates) + 1:03d}",
                            source_candidate_id=source["source_candidate_id"],
                            source_id=source.get("source_id"),
                            local_pdf_path=source["local_pdf_path"],
                            local_pdf_hash=source["local_pdf_hash"],
                            page_number=page.page_number,
                            section_id=section_id,
                            figure_id=figure_id,
                            table_id=table_id,
                            equation_id=None,
                            observable_class=observable_class,
                            variable_name=target.get("target_variable"),
                            numeric_value_text=numeric,
                            unit_text=unit,
                            condition_text=target.get("expected_condition_axis"),
                            snippet=snippet,
                            classification=classification,
                            reviewer_decision="FORWARD_TO_V5_7_3_REVIEW" if classification == "OBSERVED_MEASUREMENT_CANDIDATE" else "REJECT_CONTEXT_ONLY",
                            extraction_blockers=blockers,
                            recommended_next_action=next_action,
                        )
                    )
                    if snippet_index >= 2:
                        break
    observed = [item for item in candidates if item.classification == "OBSERVED_MEASUREMENT_CANDIDATE"]
    rejected = [item for item in candidates if item.classification != "OBSERVED_MEASUREMENT_CANDIDATE"]
    return candidates, observed, rejected


def _load_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("records", []))
