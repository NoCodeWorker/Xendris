"""Public dataset search logic for Track C."""

from __future__ import annotations

from pathlib import Path
from phyng.external_evidence.schemas import PublicDatasetSearchResult


def run_public_dataset_search(inputs: dict, root: str | Path = ".") -> list[PublicDatasetSearchResult]:
    root_path = Path(root)
    queue = inputs.get("public_dataset_lookup_queue_v4_3", {}).get("public_dataset_lookup_queue", [])
    ext_dir = root_path / "data/external_datasets"

    results: list[PublicDatasetSearchResult] = []
    dir_exists = ext_dir.is_dir()
    files = list(ext_dir.glob("*")) if dir_exists else []

    # Map queue by source_id
    by_source: dict[str, list[str]] = {}
    for item in queue:
        s_id = item.get("source_id", "")
        t_id = item.get("target_id", "")
        by_source.setdefault(s_id, []).append(t_id)

    # Fallback to hashes if queue empty
    if not by_source:
        hashes = inputs.get("source_hashes_v3_6", {}).get("hashes", [])
        for h in hashes:
            by_source[h["source_id"]] = []

    for idx, (source_id, target_ids) in enumerate(by_source.items(), start=1):
        evidence_status = "PUBLIC_DATASET_NOT_FOUND"
        blockers = ["PUBLIC_DATASET_NOT_FOUND"]
        dataset_path = None
        dataset_hash = None

        if len(files) > 0:
            pass

        results.append(
            PublicDatasetSearchResult(
                search_id=f"PUB-SEARCH-v4_5-{idx:03d}",
                source_id=source_id,
                target_ids=target_ids,
                repository_name=None,
                repository_reference=None,
                local_dataset_path=dataset_path,
                dataset_hash=dataset_hash,
                expected_observables=["TEMPERATURE_PRESSURE_REGIME", "MASS_REGIME", "TIME_REGIME", "SEPARATION_REGIME"],
                found_numeric_values=False,
                candidate_records=[],
                evidence_status=evidence_status,
                blockers=blockers,
            )
        )
    return results
