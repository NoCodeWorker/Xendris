def classify_non_triviality(
    has_negative_bound: bool,
    has_predictive_model: bool,
    has_empirical_threshold: bool,
    has_gain: bool
) -> str:
    if has_gain and has_predictive_model and has_empirical_threshold:
        return "EMPIRICALLY_ACTIONABLE"
    elif has_predictive_model and has_gain:
        return "PREDICTIVE_NONTRIVIAL"
    elif has_negative_bound:
        return "NEGATIVE_NONTRIVIAL"
    elif has_predictive_model:
        return "STRUCTURAL_USEFUL"
    else:
        return "TRIVIAL_STRUCTURAL"
