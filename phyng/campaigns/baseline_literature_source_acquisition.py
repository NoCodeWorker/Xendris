"""
Phygn v1.1 — Campaign: Baseline Literature Source Acquisition

Entry point for the v1.1 source acquisition preparation pipeline.
Runs: manifest validation → extract validation → acquisition tasks → readiness report.

Does NOT claim sources have been ingested.
"""

from __future__ import annotations

import sys
from pathlib import Path

from phyng.evidence.extract_validation import (
    validate_extract_folder,
    write_extract_support_tags_report,
)
from phyng.evidence.source_acquisition_tasks import generate_source_acquisition_tasks, get_missing_categories
from phyng.evidence.source_manifest_validation import (
    validate_source_manifest,
    write_manifest_validation_report,
)
from phyng.evidence.source_pack_readiness_v1_1 import (
    create_baseline_source_folders,
    generate_baseline_source_pack_readiness_v1_1,
)


def main(project_root: Path | None = None) -> None:
    root = project_root or Path(__file__).resolve().parent.parent.parent
    print(f"[BASELINE-SRC-PACK-001 v1.1] project_root = {root}")

    # Step 1 — Scaffold folders
    folders = create_baseline_source_folders(root)
    print(f"\n[1/4] Folders ready: {len(folders)} directories")

    # Step 2 — Manifest validation
    manifest_path = root / "sources" / "baseline" / "source_manifest.json"
    manifest_result = validate_source_manifest(manifest_path, root)
    write_manifest_validation_report(manifest_result, root)
    print(f"[2/4] Manifest validation: {manifest_result.summary}")

    # Step 3 — Extract validation
    extracts_dir = root / "sources" / "baseline" / "extracts"
    extract_results = validate_extract_folder(extracts_dir)
    extract_report = write_extract_support_tags_report(extract_results, root)
    valid_extracts = sum(1 for r in extract_results if r.valid)
    print(f"[3/4] Extracts: {valid_extracts}/{len(extract_results)} valid — report: {extract_report}")

    # Step 4 — Acquisition tasks
    tasks = generate_source_acquisition_tasks(root, covered_categories=[])
    missing = get_missing_categories(tasks)
    print(f"[4/4] Acquisition tasks: {len(tasks)} total, {len(missing)} open")

    # Step 5 — Readiness report
    readiness = generate_baseline_source_pack_readiness_v1_1(root)

    print()
    print("=" * 60)
    print("  BASELINE-SRC-PACK-001 v1.1 — Readiness Result")
    print("=" * 60)
    print(f"  Folders exist          : {readiness.folders_exist}")
    print(f"  Manifest exists        : {readiness.manifest_exists}")
    print(f"  Manifest valid         : {readiness.manifest_valid}")
    print(f"  Extracts count         : {readiness.extracts_count}")
    print(f"  Validated extracts     : {readiness.validated_extracts_count}")
    print(f"  Readiness Status       : {readiness.readiness_status}")
    print(f"  Ready for ingestion    : {readiness.ready_for_ingestion_attempt}")
    print()
    print(f"  Allowed next action:")
    print(f"    → {readiness.allowed_next_action}")
    print()
    print("  Reports:")
    for rp in readiness.report_paths:
        print(f"    → {rp}")
    print()
    print("  Missing source categories:")
    for cat in missing:
        print(f"    ⚠ {cat}")
    print()
    print("  Blocked claims (ALL statuses):")
    print("    ✗ Phygn predicts gravitational decoherence.")
    print("    ✗ Frontera C is validated.")
    print("    ✗ The boundary-aware candidate is validated.")
    print("    ✗ SyntheticGain is physical PredictiveGain.")
    print("=" * 60)


if __name__ == "__main__":
    root_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    main(root_arg)
