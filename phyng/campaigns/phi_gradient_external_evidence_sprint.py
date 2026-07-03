"""Campaign wrapper for v4.5 external evidence sprint."""

from __future__ import annotations

import sys
from pathlib import Path

from phyng.external_evidence.campaign import run_phi_gradient_external_evidence_sprint_campaign


def main() -> None:
    res = run_phi_gradient_external_evidence_sprint_campaign(Path("."))
    print(res)
    if "BLOCKED" in res["status"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
