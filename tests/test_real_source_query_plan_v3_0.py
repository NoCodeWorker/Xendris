from phyng.real_source_acquisition.query_plan import build_phi_gradient_real_source_query_plan


def test_query_plan_covers_all_slots():
    plan = build_phi_gradient_real_source_query_plan()
    slot_ids = {query.slot_id for query in [*plan.slot_queries, *plan.negative_queries]}

    assert slot_ids == {
        "SLOT_1_DECOHERENCE_BASELINE_MODELS",
        "SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS",
        "SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS",
        "SLOT_4_GRADIENT_TRANSITION_OPERATORS",
        "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS",
        "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS",
        "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES",
        "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
    }
    assert plan.benchmark_queries[0].slot_id == "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS"
