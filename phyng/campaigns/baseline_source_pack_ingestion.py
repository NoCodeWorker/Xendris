"""
Phygn v1.0 — Campaign: Baseline Source Pack Ingestion

Entry point for BASELINE-SRC-PACK-001.
Calls run_limited_upgrade_execution and prints a console summary.
"""

from __future__ import annotations

import sys
from pathlib import Path

from phyng.baselines.limited_upgrade_execution import run_limited_upgrade_execution


def main(project_root: Path | None = None) -> None:
    root = project_root or Path(__file__).resolve().parent.parent.parent
    print(f"[BASELINE-SRC-PACK-001] project_root = {root}")

    result = run_limited_upgrade_execution(project_root=root)

    print()
    print("=" * 60)
    print("  BASELINE-SRC-PACK-001 — Ingestion Result")
    print("=" * 60)
    print(f"  Pack Status      : {result.source_pack_status}")
    print(f"  Audited (passed) : {result.audited_sources_count}")
    print(f"  FORMULA support  : {result.formula_support_count}")
    print(f"  OBSERVABLE sup.  : {result.observable_support_count}")
    print(f"  PARAMETER sup.   : {result.parameter_support_count}")
    print(f"  Baseline After   : {result.baseline_after}")
    print(f"  Upgrade Success  : {result.upgrade_success}")
    print(f"  Max Claim Level  : {result.max_claim_level}")
    print()
    print("  Allowed Claims:")
    for c in result.allowed_claims:
        print(f"    ✓ {c}")
    if not result.allowed_claims:
        print("    (none — sources required)")
    print()
    print("  Blocked Claims:")
    for c in result.blocked_claims:
        print(f"    ✗ {c}")
    print()
    print("  Reports:")
    for rp in result.report_paths:
        print(f"    → {rp}")
    print("=" * 60)


if __name__ == "__main__":
    root_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    main(root_arg)
