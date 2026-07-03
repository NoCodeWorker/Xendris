from phyng.campaigns.non_triviality import classify_non_triviality


def test_non_triviality_levels():
    # Trivial structural check
    status = classify_non_triviality(
        has_negative_bound=False,
        has_predictive_model=False,
        has_empirical_threshold=False,
        has_gain=False
    )
    assert status == "TRIVIAL_STRUCTURAL"
    
    # Negative nontrivial
    status = classify_non_triviality(
        has_negative_bound=True,
        has_predictive_model=False,
        has_empirical_threshold=True,
        has_gain=False
    )
    assert status == "NEGATIVE_NONTRIVIAL"
    
    # Predictive nontrivial
    status = classify_non_triviality(
        has_negative_bound=False,
        has_predictive_model=True,
        has_empirical_threshold=False,
        has_gain=True
    )
    assert status == "PREDICTIVE_NONTRIVIAL"

    
    # Empirically actionable
    status = classify_non_triviality(
        has_negative_bound=False,
        has_predictive_model=True,
        has_empirical_threshold=True,
        has_gain=True
    )
    # If we also have has_empirical_threshold and has_gain it is predictive or actionable
    # Let's verify standard status matches
    status = classify_non_triviality(
        has_negative_bound=False,
        has_predictive_model=True,
        has_empirical_threshold=True,
        has_gain=True
    )
    assert status == "EMPIRICALLY_ACTIONABLE"
