"""Generate 30-task controlled-run dataset from v0.4.3 frozen tasks.

Provenance:
- Base: benchmarks/finitexo_code_matrix_v0_4_3/ (10 frozen tasks)
- Method: Each of the 10 base tasks is replicated 3 times with variant_id added
  to task_id and track_id. No base task content is modified.
- Authorized claims: diagnostic controlled-run only, no superiority.
- Blocked claims: model superiority, provider ranking, external benchmark validation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = Path("benchmarks/finitexo_code_matrix_v0_4_3")
OUT = Path(__file__).resolve().parent
TASKS_OUT = OUT / "tasks"

VARIANT_LABELS = ["A", "B", "C"]
VERSION = "0.6.0"
DATASET_NAME = "Finitexo Code Matrix Controlled Run n=30"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    base_tasks = sorted((BASE / "tasks").glob("frozen_task_*.json"))
    base_hashes = _load_json(BASE / "frozen_dataset_hashes.json")

    print(f"Generating {len(base_tasks) * len(VARIANT_LABELS)} tasks from {len(base_tasks)} base tasks...")

    tasks: list[dict] = []
    for idx, base_path in enumerate(base_tasks, start=1):
        base = _load_json(base_path)
        for variant_idx, label in enumerate(VARIANT_LABELS, start=1):
            global_idx = (idx - 1) * len(VARIANT_LABELS) + variant_idx
            task_id = f"cr_n30_task_{global_idx:03d}"
            track_id = f"{base.get('task_id', 'base')}_{label}"
            content = {
                "task_id": task_id,
                "track_id": track_id,
                "task_version": VERSION,
                "base_task_id": base.get("task_id"),
                "base_task_version": base.get("task_version", ""),
                "base_content_hash": base.get("content_hash"),
                "variant_label": label,
                "source_origin": "CONTROLLED_RUN_N30_GENERATED",
                "prompt": base.get("prompt", ""),
                "expected_behavior": base.get("expected_behavior", ""),
                "allowed_files": base.get("allowed_files", []),
                "forbidden_files": base.get("forbidden_files", []),
                "validation_oracle": base.get("validation_oracle", ""),
                "visible_tests_description": base.get("visible_tests_description", ""),
                "hidden_tests_description": base.get("hidden_tests_description", ""),
                "network_required": base.get("network_required", False),
                "secrets_required": base.get("secrets_required", False),
            }
            cont = json.dumps(content, sort_keys=True)
            content_hash = hashlib.sha256(cont.encode("utf-8")).hexdigest()
            content["content_hash"] = content_hash
            tasks.append(content)

    # Write tasks
    for task in tasks:
        _write_json(TASKS_OUT / f"task_{task['task_id'].split('_')[-1]}.json", task)

    # Compute dataset hash and manifest hash
    manifest = {
        "dataset_name": DATASET_NAME,
        "dataset_version": VERSION,
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "v0.6.0",
        "dataset_status": "GENERATED",
        "dataset_type": "CONTROLLED_RUN_N30",
        "frozen_task_count": len(tasks),
        "base_dataset_path": str(BASE),
        "base_dataset_hash": base_hashes.get("dataset_hash", ""),
        "base_manifest_hash": base_hashes.get("manifest_hash", ""),
        "generation_method": "deterministic_replication_with_variant_ids",
        "variant_labels": VARIANT_LABELS,
        "authorized_claims": [
            "Diagnostic controlled-run n=30 generated deterministically from v0.4.3 frozen tasks.",
            "No model superiority claim authorized.",
            "No provider ranking claim authorized.",
            "No external benchmark validation claim authorized.",
        ],
        "blocked_claims": [
            "model superiority demonstrated",
            "provider ranking established",
            "external benchmark performance validated",
            "statistical significance established",
            "production-readiness proven",
        ],
        "external_superiority_claim_authorized": False,
        "model_comparison_allowed": False,
        "provider_execution_allowed": True,
        "statistical_claim_authorized": False,
    }
    cont_m = json.dumps(manifest, sort_keys=True)
    manifest_hash = hashlib.sha256(cont_m.encode("utf-8")).hexdigest()
    manifest["manifest_hash"] = manifest_hash

    # Compute dataset-level hash
    all_content = json.dumps([json.dumps(t, sort_keys=True) for t in tasks], sort_keys=True)
    dataset_hash = hashlib.sha256(all_content.encode("utf-8")).hexdigest()

    hashes = {
        "dataset_name": DATASET_NAME,
        "dataset_version": VERSION,
        "dataset_hash": dataset_hash,
        "manifest_hash": manifest_hash,
        "frozen_task_count": len(tasks),
        "base_dataset_hash": base_hashes.get("dataset_hash", ""),
        "base_manifest_hash": base_hashes.get("manifest_hash", ""),
    }

    _write_json(OUT / "dataset_hashes.json", hashes)
    _write_json(OUT / "dataset_manifest.json", manifest)

    # Provenance record
    provenance = {
        "generated_at": "2026-07-08T00:00:00Z",
        "generator": "benchmarks/finitexo_code_matrix_v0_6/datasets/controlled_run_n30/generate_dataset.py",
        "base_dataset": str(BASE),
        "base_dataset_hash": base_hashes.get("dataset_hash", ""),
        "method": "Each of the 10 v0.4.3 frozen tasks replicated 3 times (A, B, C variants)",
        "variant_labels": VARIANT_LABELS,
        "task_count": len(tasks),
        "dataset_hash": dataset_hash,
        "manifest_hash": manifest_hash,
        "reproducibility": "Run generate_dataset.py again with same base to reproduce identical hashes.",
        "authorized_claims": list(manifest["authorized_claims"]),
        "blocked_claims": list(manifest["blocked_claims"]),
    }
    _write_json(OUT / "provenance.json", provenance)

    print(f"  Tasks: {len(tasks)}")
    print(f"  Dataset hash: {dataset_hash}")
    print(f"  Manifest hash: {manifest_hash}")
    print(f"  Output: {OUT}")


if __name__ == "__main__":
    main()
