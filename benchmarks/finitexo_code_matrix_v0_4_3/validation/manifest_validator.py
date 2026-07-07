"""Manifest validation for v0.4.3 expanded freeze."""

from __future__ import annotations

from typing import Any, Mapping


def validate_manifest(manifest: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "v0.4.3",
        "dataset_version": "0.4.3",
        "dataset_status": "FROZEN",
        "dataset_type": "EXTERNAL_ADAPTED_CANDIDATE_FREEZE",
        "frozen_task_count": 10,
        "created_from_base_dataset": "v0.4",
        "created_from_expansion_pool": "v0.4.2",
        "base_v0_4_dataset_hash": "0ed903b013bff8650ce30030863d069a6cdd745d42964ba85082389d836cdb17",
        "base_v0_4_manifest_hash": "981406f6aa7a736cb64e698742075c4f05fbafcdf7e79e96a97c781224984298",
        "provider_execution_allowed": False,
        "model_comparison_allowed": False,
        "external_superiority_claim_authorized": False,
        "statistical_claim_authorized": False,
        "frozen_dataset_modified_without_version_bump_allowed": False,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            errors.append(f"manifest_invalid_{key}")
    return errors
