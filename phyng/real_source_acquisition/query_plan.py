"""Slot-based real source query plan for PHI_GRADIENT."""

from __future__ import annotations

from phyng.real_source_acquisition.schemas import RealSourceQueryPlan, SlotQuery


def build_phi_gradient_real_source_query_plan() -> RealSourceQueryPlan:
    slot_queries = [
        _query("Q-SLOT-1", "SLOT_1_DECOHERENCE_BASELINE_MODELS", "visibility decay decoherence rate interferometry Gamma_env", ["visibility_decay_observable", "Gamma_env_rate", "baseline_model"], 1),
        _query("Q-SLOT-8", "SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT", "fringe visibility decoherence exponential decay contrast loss", ["visibility_decay_observable", "contrast_loss_equation"], 2),
        _query("Q-SLOT-5", "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS", "mesoscopic interferometry visibility decoherence benchmark mass separation time", ["mass_range", "length_or_separation_range", "time_range", "visibility_measure"], 3),
        _query("Q-SLOT-2", "SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS", "gravitational decoherence model mass dependent decoherence rate", ["mass_dependent_rate", "length_scale_dependence", "parameter_constraints"], 4),
        _query("Q-SLOT-4", "SLOT_4_GRADIENT_TRANSITION_OPERATORS", "gradient term effective decoherence model transition region operator", ["gradient_operator", "transition_region", "rate_contribution"], 5),
        _query("Q-SLOT-3", "SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS", "log scale coordinates decoherence model dimensionless variables", ["dimensionless_log_variables", "scale_transformation"], 6),
        _query("Q-SLOT-6", "SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS", "dimensionless coupling decoherence rate constraint interferometry", ["alpha_like_constraint", "coupling_bound", "rate_ratio_constraint"], 7),
    ]
    negative_queries = [
        _query("Q-SLOT-7", "SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES", "environmental decoherence dominates gravitational decoherence interferometry", ["contradiction", "exclusion", "dominant_background"], 8),
    ]
    benchmark_queries = [query for query in slot_queries if query.slot_id == "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS"]
    return RealSourceQueryPlan(
        campaign_id="PHI-GRADIENT-REAL-SOURCE-ACQUISITION-v3_0",
        target_candidate="LOG_BOUNDARY / PHI_GRADIENT",
        slot_queries=slot_queries,
        negative_queries=negative_queries,
        benchmark_queries=benchmark_queries,
        acquisition_limits={"max_candidates_per_query": 5, "max_total_candidates": 40},
        inclusion_rules=["equation", "observable", "parameter range", "benchmark data", "experimental bound", "rate model", "explicit negative constraint"],
        exclusion_rules=["broad conceptual discussion", "generic gradient language", "generic scale language", "no observable", "no equation", "no parameter range", "no benchmark"],
    )


def _query(query_id: str, slot_id: str, query_text: str, expected_components: list[str], priority: int) -> SlotQuery:
    return SlotQuery(
        query_id=query_id,
        slot_id=slot_id,
        query_text=query_text,
        expected_components=expected_components,
        priority=priority,
        source_types=["paper", "benchmark", "dataset", "review_with_equations"],
    )
