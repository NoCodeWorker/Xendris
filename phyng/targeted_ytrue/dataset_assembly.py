"""Dataset assembly for v5.7.3 targeted y_true extraction."""

from __future__ import annotations

from collections import Counter

from phyng.targeted_ytrue.schemas import AcceptedTargetedYTrue


def assemble_dataset(existing: list[dict], new: list[AcceptedTargetedYTrue]) -> dict:
    normalized_existing = [_normalize_existing(record) for record in existing]
    new_records = [record.model_dump() for record in new]
    records = normalized_existing + new_records
    return {
        "dataset_id": "VISIBILITY-DECOHERENCE-EXPANDED-YTRUE-DATASET-v5_7_3",
        "existing_accepted_ytrue_count": len(normalized_existing),
        "new_accepted_ytrue_count": len(new_records),
        "accepted_ytrue_count": len(records),
        "source_count": len({record["source_id"] for record in records}),
        "records": records,
        "observable_class_distribution": dict(Counter(record.get("observable_class") for record in records)),
        "condition_distribution": dict(Counter(_condition_keys(record) for record in records)),
        "qc_distribution": dict(Counter(record.get("qc_status") for record in records)),
        "predictive_gain_computed": False,
        "physical_claim_created": False,
        "frontera_c_validated": False,
    }


def _normalize_existing(record: dict) -> dict:
    value = record.get("value", record.get("value_numeric"))
    conditions = record.get("conditions")
    if conditions is None and record.get("experimental_condition_name"):
        conditions = {
            record["experimental_condition_name"]: record.get("experimental_condition_value"),
            "unit": record.get("experimental_condition_unit"),
        }
    return {
        "y_true_id": record.get("y_true_id"),
        "dataset_version": "v5.3",
        "source_id": record.get("source_id"),
        "source_title": record.get("source_title"),
        "source_year": record.get("source_year"),
        "local_pdf_path": record.get("local_pdf_path"),
        "local_pdf_hash": record.get("local_pdf_hash"),
        "page_number": record.get("page_number"),
        "location_label": record.get("figure_id") or record.get("location_label"),
        "observable_class": record.get("observable_class"),
        "variable_name": record.get("variable_name"),
        "value_numeric": value,
        "original_value_text": record.get("original_value_text"),
        "unit": record.get("unit"),
        "normalized_unit": record.get("unit"),
        "conditions": conditions or {},
        "qc_status": record.get("qc_status"),
        "claim_impact": "DATASET_EXPANSION_ONLY",
    }


def _condition_keys(record: dict) -> str:
    conditions = record.get("conditions") or {}
    return ",".join(sorted(str(key) for key in conditions.keys())) or "none"
