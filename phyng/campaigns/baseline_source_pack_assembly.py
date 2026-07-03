"""
Phygn v1.2 — Campaign: Baseline Source Pack Assembly

Entry point for BASELINE-SRC-PACK-001 v1.2 template assembly.
Runs the assembly function and prints a summary.
"""

from __future__ import annotations

import sys
from pathlib import Path

from phyng.evidence.source_pack_assembly import assemble_baseline_source_pack_templates


def main(project_root: Path | None = None) -> None:
    root = project_root or Path(__file__).resolve().parent.parent.parent
    print(f"[BASELINE-SRC-PACK-001 v1.2] project_root = {root}")

    result = assemble_baseline_source_pack_templates(root)

    print()
    print("=" * 60)
    print("  BASELINE-SRC-PACK-001 v1.2 — Assembly Result")
    print("=" * 60)
    print(f"  Assembly Status        : {result.assembly_status}")
    print(f"  Ready for Ingestion    : {result.ready_for_ingestion_attempt}")
    print(f"  Manifest Struct. Valid : {result.manifest_structurally_valid}")
    print(f"  Extracts Struct. Valid : {result.extracts_structurally_valid}")
    print()
    print("  Created Files:")
    for f in result.created_files:
        print(f"    → {Path(f).relative_to(root)}")
    print()
    print("  Reports:")
    for rp in result.report_paths:
        print(f"    → {Path(rp).relative_to(root)}")
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
