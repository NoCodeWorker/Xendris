import math

from phyng.model_comparison.schemas import BoundaryCouplingSpec


def exponential_visibility(t: list[float], gamma: float) -> list[float]:
    if gamma < 0:
        raise ValueError("gamma must be >= 0")
    return [math.exp(-gamma * value) for value in t]


def boundary_aware_visibility(
    t: list[float],
    gamma_base: float,
    delta_gamma_c: float,
) -> list[float]:
    if gamma_base < 0:
        raise ValueError("gamma_base must be >= 0")
    if delta_gamma_c < 0:
        raise ValueError("delta_gamma_c must be >= 0 for the initial toy candidate")
    return exponential_visibility(t, gamma_base + delta_gamma_c)


def boundary_coupling_value(function_name: str, *, B: float, QB: float) -> float:
    if B <= 0:
        raise ValueError("B must be > 0")
    if QB < 0:
        raise ValueError("QB must be >= 0")

    if function_name == "B":
        return B
    if function_name == "QB":
        return QB
    if function_name == "INV_ABS_LOG10_B":
        return 1.0 / abs(math.log10(B))

    raise ValueError(f"Unsupported boundary coupling function: {function_name}")


def default_boundary_coupling_spec(function_name: str = "B") -> BoundaryCouplingSpec:
    formulas = {
        "B": "delta_gamma_c = alpha * B",
        "QB": "delta_gamma_c = alpha * QB",
        "INV_ABS_LOG10_B": "delta_gamma_c = alpha / abs(log10(B))",
    }
    return BoundaryCouplingSpec(
        coupling_id=f"TOY-COUPLING-{function_name}",
        formula=formulas.get(function_name, function_name),
        reason=(
            "Initial explicit toy coupling for model-comparison plumbing. "
            "It is not source-backed and cannot support a physical decoherence claim."
        ),
        status="TOY_REQUIRES_SOURCE_FOR_PHYSICAL_INTERPRETATION",
        forbidden_interpretations=[
            "Phygn predicts gravitational decoherence.",
            "Boundary C causes decoherence.",
            "The invariant explains decoherence.",
        ],
    )
