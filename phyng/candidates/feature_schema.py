"""Feature schema builder for v5.9 candidate screening."""

from __future__ import annotations

from phyng.candidates.dataset_introspection import introspect_dataset
from phyng.candidates.schemas import CandidateFamilyRecord, CandidateFeatureSchema


FORBIDDEN = [
    "visibility_fraction",
    "interference_contrast",
    "value_numeric",
    "value",
    "original_value_text",
    "qc_status",
    "source_id",
    "page_number",
    "figure_id",
    "location_label",
    "local_pdf_hash",
]


def build_feature_schema(dataset: dict, families: list[CandidateFamilyRecord]) -> CandidateFeatureSchema:
    meta = introspect_dataset(dataset)
    allowed = sorted(set(meta["condition_keys"] + ["observable_class", "variable_name"]))
    missing = {
        family.candidate_family_id: [
            feature for feature in family.required_features if feature not in allowed and feature not in _virtual_features(meta)
        ]
        for family in families
    }
    return CandidateFeatureSchema(
        dataset_id=meta["dataset_id"],
        target_variable="value_numeric",
        forbidden_feature_columns=FORBIDDEN,
        allowed_feature_columns=allowed,
        missing_required_features_by_candidate=missing,
        derived_feature_rules=[
            {
                "feature": "non_target_condition_features",
                "rule": "May use condition fields only; must exclude value_numeric, original_value_text, source_id and local identifiers.",
            }
        ],
        leakage_notes=["Heterogeneous condition keys mean no shared numeric condition axis currently spans all records."],
    )


def _virtual_features(meta: dict) -> set[str]:
    virtual = {"non_target_condition_features"}
    if meta["common_condition_keys"]:
        virtual.add("shared_numeric_condition_axis")
    return virtual
