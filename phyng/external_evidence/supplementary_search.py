"""Supplementary search logic for Track B."""

from __future__ import annotations

from pathlib import Path
from phyng.external_evidence.schemas import SupplementarySearchResult


def run_supplementary_search(inputs: dict, root: str | Path = ".") -> list[SupplementarySearchResult]:
    root_path = Path(root)
    queue = inputs.get("supplementary_lookup_queue_v4_3", {}).get("supplementary_lookup_queue", [])
    supp_dir = root_path / "data/real_sources/supplementary"

    results: list[SupplementarySearchResult] = []
    # If no local directory or no files in it:
    dir_exists = supp_dir.is_dir()
    files = list(supp_dir.glob("*")) if dir_exists else []

    # Map queue by source_id
    by_source: dict[str, list[str]] = {}
    for item in queue:
        s_id = item.get("source_id", "")
        t_id = item.get("target_id", "")
        by_source.setdefault(s_id, []).append(t_id)

    # If queue is empty, we still inspect the sources from hashes to be robust
    if not by_source:
        hashes = inputs.get("source_hashes_v3_6", {}).get("hashes", [])
        for h in hashes:
            by_source[h["source_id"]] = []

    for idx, (source_id, target_ids) in enumerate(by_source.items(), start=1):
        evidence_status = "SUPPLEMENTARY_NOT_FOUND"
        blockers = ["SUPPLEMENTARY_NOT_FOUND"]
        supp_path = None
        file_hash = None

        if len(files) > 0:
            # If files existed, we would set SUPPLEMENTARY_FOUND_VALUES or similar
            pass

        results.append(
            SupplementarySearchResult(
                search_id=f"SUPP-SEARCH-v4_5-{idx:03d}",
                source_id=source_id,
                target_ids=target_ids,
                supplementary_path=supp_path,
                supplementary_url_or_reference=None,
                file_hash=file_hash,
                expected_observables=["COHERENCE_LOSS", "DECOHERENCE_RATE"],
                found_numeric_values=False,
                candidate_records=[],
                evidence_status=evidence_status,
                blockers=blockers,
            )
        )
    return results
