from phyng.model_comparison.detectability import (
    classify_detectability,
    delta_series,
    max_abs_delta,
)
from phyng.model_comparison.metrics import compute_error, compute_predictive_gain
from phyng.model_comparison.models import (
    boundary_aware_visibility,
    boundary_coupling_value,
    default_boundary_coupling_spec,
    exponential_visibility,
)
from phyng.model_comparison.schemas import ModelComparisonResult, ModelComparisonSpec


DEFAULT_BLOCKED_CLAIMS = [
    "Phygn predicts gravitational decoherence.",
    "Boundary C causes decoherence.",
    "The invariant explains decoherence.",
    "This validates Frontera C.",
]

DEFAULT_REQUIRED_SOURCES = [
    "standard decoherence visibility decay",
    "environmental decoherence in matter-wave interferometry",
    "experimental visibility thresholds",
]


def run_model_comparison(spec: ModelComparisonSpec) -> ModelComparisonResult:
    gamma_base = spec.parameters.get("gamma_base")
    alpha = spec.parameters.get("alpha")
    B = spec.parameters.get("B")
    QB = spec.parameters.get("QB")
    coupling_function = spec.parameters.get("coupling_function", 0.0)

    if gamma_base is None:
        raise ValueError("parameters.gamma_base is required")
    if alpha is None:
        raise ValueError("parameters.alpha is required")
    if B is None:
        raise ValueError("parameters.B is required")
    if QB is None:
        raise ValueError("parameters.QB is required")

    if isinstance(coupling_function, str):
        function_name = coupling_function
    else:
        function_name = "B"

    coupling = spec.boundary_coupling or default_boundary_coupling_spec(function_name)
    coupling_value = boundary_coupling_value(function_name, B=B, QB=QB)
    delta_gamma_c = alpha * coupling_value

    y_base = exponential_visibility(spec.t, gamma_base)
    y_candidate = boundary_aware_visibility(spec.t, gamma_base, delta_gamma_c)
    deltas = delta_series(y_base, y_candidate)
    max_delta = max_abs_delta(y_base, y_candidate)
    detectability = classify_detectability(max_delta, spec.epsilon_exp)

    error_base = None
    error_candidate = None
    gain_c = None
    predictive_status = "MODEL_DELTA_ONLY"
    evidence_level = 3

    if spec.y_true is not None:
        error_base = compute_error(spec.error_metric, spec.y_true, y_base)
        error_candidate = compute_error(spec.error_metric, spec.y_true, y_candidate)
        gain_c = compute_predictive_gain(error_base, error_candidate)
        evidence_level = 4
        if gain_c > 0:
            predictive_status = "POSITIVE_TOY_GAIN"
        elif gain_c == 0:
            predictive_status = "ZERO_GAIN"
        else:
            predictive_status = "NEGATIVE_GAIN"

    allowed_claims = [
        "The candidate produces a computed toy delta under explicit assumptions.",
    ]
    if detectability == "UNDETECTABLE_DIFFERENCE":
        allowed_claims.append(
            "The candidate toy delta is below the selected detectability threshold."
        )
    elif detectability == "DETECTABLE_TOY_DIFFERENCE":
        allowed_claims.append(
            "The candidate toy delta is above the selected threshold, but no physical prediction is claimed."
        )

    if predictive_status == "POSITIVE_TOY_GAIN":
        allowed_claims.append(
            "The candidate improves the toy benchmark under the selected metric, but no physical prediction is claimed."
        )

    required_next_steps = [
        "Ingest source-backed decoherence baseline references.",
        "Define benchmark data or y_true before claiming Predictive Gain.",
        "Link model assumptions to RAG sources.",
    ]

    return ModelComparisonResult(
        comparison_id=spec.comparison_id,
        campaign_id=spec.campaign_id,
        system_id=spec.system_id,
        observable=spec.observable,
        y_true=spec.y_true,
        y_base=y_base,
        y_candidate=y_candidate,
        error_base=error_base,
        error_candidate=error_candidate,
        gain_c=gain_c,
        delta_series=deltas,
        max_abs_delta=max_delta,
        detectability_status=detectability,
        predictive_status=predictive_status,
        evidence_level=evidence_level,
        maximum_allowed_claim_level=evidence_level,
        allowed_claims=allowed_claims,
        blocked_claims=DEFAULT_BLOCKED_CLAIMS.copy(),
        required_sources=DEFAULT_REQUIRED_SOURCES.copy(),
        required_tests=[
            "tests/test_model_comparison_engine.py",
            "tests/test_campaign_002_decoherence.py",
        ],
        required_next_steps=required_next_steps,
    )
