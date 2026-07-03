"""Campaign wrapper for validate-if-possible self-provisioning loop."""

from __future__ import annotations

from pathlib import Path

from phyng.self_provisioning.campaign import run_validate_if_possible_loop_campaign


def run(root: str | Path = "."):
    return run_validate_if_possible_loop_campaign(root)


if __name__ == "__main__":
    result = run_validate_if_possible_loop_campaign(root=".")
    print(result)
