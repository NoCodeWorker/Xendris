"""Campaign wrapper for v5.9 reality-contact candidate-family construction."""

from __future__ import annotations

from pathlib import Path

from phyng.candidates.campaign import run_frontera_c_reality_contact_candidate_family_campaign


def run(root: str | Path = "."):
    return run_frontera_c_reality_contact_candidate_family_campaign(root)


if __name__ == "__main__":
    result = run_frontera_c_reality_contact_candidate_family_campaign(root=".")
    print(result)
