"""Input loaders for v5.7.3 targeted y_true extraction."""

from __future__ import annotations

import json
from pathlib import Path


def load_inputs(root: str | Path = ".") -> dict:
    repo_root = Path(root)
    return {
        "observed": _records(repo_root / "data/frontera_c/observable_location/targeted_observed_measurement_candidates_v5_7_2.json"),
        "source_manifest": _records(repo_root / "data/frontera_c/source_download/source_download_manifest_v5_7_2.json"),
        "existing_ytrue": _records(repo_root / "data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json"),
        "next_gate_v572": _json(repo_root / "data/frontera_c/observable_location/v5_7_2_next_gate_decision.json"),
    }


def _records(path: Path) -> list[dict]:
    payload = _json(path)
    return list(payload.get("records", []))


def _json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))
