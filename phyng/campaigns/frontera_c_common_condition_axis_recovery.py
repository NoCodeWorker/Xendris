"""Campaign wrapper for v5.9.2 common condition axis recovery."""

from __future__ import annotations

from pathlib import Path

from phyng.candidates.common_axis_recovery import (
    run_common_condition_axis_recovery,
    write_common_condition_axis_outputs,
)


def run(root: str | Path = ".") -> dict:
    payload = run_common_condition_axis_recovery(root)
    output_paths = write_common_condition_axis_outputs(root, payload)
    decision = payload["decision"]
    return {
        "status": decision["final_status"],
        "selected_axis": decision["selected_axis"],
        "selected_candidate_family": decision["selected_candidate_family"],
        "v6_0_permitted": decision["v6_0_permitted"],
        "predictive_gain_permitted": decision["predictive_gain_permitted"],
        "output_paths": output_paths,
    }


if __name__ == "__main__":
    print(run("."))
