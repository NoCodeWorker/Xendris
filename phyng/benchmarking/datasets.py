"""Dataset loading and normalization helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_COLUMNS = {
    "source_id",
    "observable_class",
    "variable_name",
    "value",
    "unit",
    "experimental_condition_name",
    "experimental_condition_value",
}


def load_ytrue_dataset(path: str | Path):
    records = json.loads(Path(path).read_text(encoding="utf-8")).get("records", [])
    try:
        import pandas as pd

        return pd.DataFrame(records)
    except ModuleNotFoundError:
        return records


def validate_ytrue_dataframe(df: Any) -> dict:
    columns = set(df.columns) if hasattr(df, "columns") else set(df[0].keys() if df else [])
    missing = sorted(REQUIRED_COLUMNS - columns)
    return {"valid": not missing, "missing_columns": missing, "row_count": len(df)}


def normalize_units(df: Any):
    if hasattr(df, "copy"):
        out = df.copy()
        if "unit" in out:
            out["unit"] = out["unit"].replace({"dimensionless percent": "dimensionless_fraction"})
        return out
    out = [dict(row) for row in df]
    for row in out:
        if row.get("unit") == "dimensionless percent":
            row["unit"] = "dimensionless_fraction"
    return out


def normalize_observable_class(name: str) -> str:
    return name.strip().upper().replace(" ", "_")
