"""Campaign wrapper for the Frontera C master goal."""

from __future__ import annotations

from pathlib import Path

from phyng.master_goal.campaign import run_master_goal_campaign


def run(root: str | Path = "."):
    return run_master_goal_campaign(root)


if __name__ == "__main__":
    result = run_master_goal_campaign(root=".")
    print(result)
