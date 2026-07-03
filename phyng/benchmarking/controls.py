"""Negative-control helpers."""

from __future__ import annotations

import random


def shuffled_target(values: list[float], seed: int = 5700) -> list[float]:
    out = list(values)
    random.Random(seed).shuffle(out)
    return out


def parameter_fairness(candidate_parameter_count: int, control_parameter_count: int) -> dict:
    return {
        "candidate_parameter_count": candidate_parameter_count,
        "control_parameter_count": control_parameter_count,
        "fair_or_stricter": control_parameter_count <= candidate_parameter_count,
    }
