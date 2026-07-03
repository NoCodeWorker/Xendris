"""Dataset introspection for v5.9 candidate-family screening."""

from __future__ import annotations

import json
from pathlib import Path
from collections import Counter


def load_canonical_dataset(root: str | Path = ".") -> dict:
    repo_root = Path(root)
    master = repo_root / "data/frontera_c/master_goal/dataset_v5_7_4_master.json"
    fallback = repo_root / "data/frontera_c/targeted_ytrue/visibility_decoherence_expanded_ytrue_dataset_v5_7_3.json"
    path = master if master.exists() else fallback
    return json.loads(path.read_text(encoding="utf-8"))


def introspect_dataset(dataset: dict) -> dict:
    records = list(dataset.get("records", []))
    condition_keys = sorted({key for record in records for key in (record.get("conditions") or {}).keys()})
    numeric_condition_keys = sorted(
        {
            key
            for record in records
            for key, value in (record.get("conditions") or {}).items()
            if isinstance(value, (int, float))
        }
    )
    common_condition_keys = [
        key for key in condition_keys if all(key in (record.get("conditions") or {}) for record in records)
    ]
    source_count = len({record.get("source_id") for record in records})
    return {
        "dataset_id": dataset.get("dataset_id"),
        "record_count": len(records),
        "source_count": source_count,
        "target_variables": sorted({record.get("variable_name") for record in records}),
        "observable_classes": dict(Counter(record.get("observable_class") for record in records)),
        "condition_keys": condition_keys,
        "numeric_condition_keys": numeric_condition_keys,
        "common_condition_keys": common_condition_keys,
        "has_multi_source_threshold": len(records) >= 10 and source_count >= 2,
    }
