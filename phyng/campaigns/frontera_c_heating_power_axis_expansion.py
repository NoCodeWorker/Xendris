"""Campaign wrapper for v5.9.3 targeted heating-power axis expansion."""

from __future__ import annotations

from pathlib import Path

from phyng.candidates.heating_power_axis_expansion import (
    run_heating_power_axis_expansion,
    write_heating_power_axis_outputs,
)


def run(root: str | Path = ".") -> dict:
    payload = run_heating_power_axis_expansion(root)
    output_paths = write_heating_power_axis_outputs(root, payload)
    decision = payload["decision"]
    return {
        "status": decision["final_status"],
        "axis_name": decision["axis_name"],
        "accepted_heating_power_ytrue_count": decision["accepted_heating_power_ytrue_count"],
        "accepted_heating_power_source_count": decision["accepted_heating_power_source_count"],
        "new_accepted_ytrue_count": decision["new_accepted_ytrue_count"],
        "v6_0_permitted": decision["v6_0_permitted"],
        "predictive_gain_permitted": decision["predictive_gain_permitted"],
        "output_paths": output_paths,
    }


if __name__ == "__main__":
    print(run("."))
