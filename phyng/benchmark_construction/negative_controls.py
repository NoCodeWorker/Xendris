"""Generate negative control plans for v4.0."""

from __future__ import annotations

from phyng.benchmark_construction.schemas import NegativeControl, NegativeControlPlan


def generate_negative_control_plan(records: list[dict]) -> NegativeControlPlan:
    """Generate a formal negative-control plan using survived slots and a mandatory NO_SLOT4 control."""
    controls: list[NegativeControl] = []

    # Check which slots have survived
    slots_found = {r.get("assigned_slot", "") for r in records}

    # 1. BASELINE_ONLY_CONTROL
    if "SLOT_1_DECOHERENCE_BASELINE" in slots_found:
        controls.append(
            NegativeControl(
                control_id="CTRL-v4_0-001",
                source_id="SRC-ALL-BASELINE",
                slot_id="SLOT_1_DECOHERENCE_BASELINE",
                control_type="BASELINE_ONLY_CONTROL",
                what_it_tests="Tests if the candidate model can be falsified on standard baseline decoherence rates.",
                failure_condition="Candidate predicts lower decoherence than baseline thermal decoherence.",
                expected_result_if_PHIGRADIENT_is_only_analogy="Candidate matches baseline thermal decoherence without extra signal.",
                expected_result_if_candidate_has_signal="Candidate shows additional visible decay above thermal baseline.",
            )
        )

    # 2. OBSERVABLE_ONLY_CONTROL
    if "SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE" in slots_found:
        controls.append(
            NegativeControl(
                control_id="CTRL-v4_0-002",
                source_id="SRC-ALL-OBSERVABLE",
                slot_id="SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE",
                control_type="OBSERVABLE_ONLY_CONTROL",
                what_it_tests="Tests if visibility decay matches standard decoherence models.",
                failure_condition="Candidate predicts higher visibility than baseline quantum mechanics allows.",
                expected_result_if_PHIGRADIENT_is_only_analogy="Visibility follows standard decoherence curves.",
                expected_result_if_candidate_has_signal="Visibility shows extra modulation or phase shift.",
            )
        )

    # 3. BENCHMARK_RANGE_CONTROL
    if "SLOT_3_BENCHMARK_RANGES" in slots_found:
        controls.append(
            NegativeControl(
                control_id="CTRL-v4_0-003",
                source_id="SRC-ALL-BENCHMARK",
                slot_id="SLOT_3_BENCHMARK_RANGES",
                control_type="BENCHMARK_RANGE_CONTROL",
                what_it_tests="Tests candidate behavior outside the benchmark mass/temperature ranges.",
                failure_condition="Candidate predicts gradient signals in macro-regimes already ruled out by standard decoherence.",
                expected_result_if_PHIGRADIENT_is_only_analogy="Zero signal in all regimes.",
                expected_result_if_candidate_has_signal="Signal scales with mass according to collapse models.",
            )
        )

    # 4. PARAMETER_CONSTRAINT_CONTROL
    if "SLOT_5_PARAMETER_CONSTRAINTS" in slots_found:
        controls.append(
            NegativeControl(
                control_id="CTRL-v4_0-004",
                source_id="SRC-ALL-PARAMETER",
                slot_id="SLOT_5_PARAMETER_CONSTRAINTS",
                control_type="PARAMETER_CONSTRAINT_CONTROL",
                what_it_tests="Tests if candidate parameters exceed collapse bounds.",
                failure_condition="Candidate collapse rate lambda exceeds CSL upper bound of 1e-8/s.",
                expected_result_if_PHIGRADIENT_is_only_analogy="Lambda is effectively zero or conforms to bounds.",
                expected_result_if_candidate_has_signal="Lambda is bounded within the permitted region.",
            )
        )

    # 5. LIMITATION_STRESS_CONTROL
    if "SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS" in slots_found:
        controls.append(
            NegativeControl(
                control_id="CTRL-v4_0-005",
                source_id="SRC-ALL-LIMITATION",
                slot_id="SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS",
                control_type="LIMITATION_STRESS_CONTROL",
                what_it_tests="Tests if background noise dominates the candidate model.",
                failure_condition="Model signal is smaller than environmental background noise floor.",
                expected_result_if_PHIGRADIENT_is_only_analogy="Candidate output is indistinguishable from noise.",
                expected_result_if_candidate_has_signal="Candidate signal is detectable above the limitation noise floor.",
            )
        )

    # 6. NO_SLOT4_CONTROL (Always included)
    controls.append(
        NegativeControl(
            control_id="CTRL-v4_0-006",
            source_id="SRC-ALL-SLOT4-DEBT",
            slot_id="SLOT_4_GRADIENT_TRANSITION_EFFECTIVE_DYNAMICS",
            control_type="NO_SLOT4_CONTROL",
            what_it_tests="Verifies candidate model behavior with the SLOT_4 gradient component zeroed out.",
            failure_condition="Model comparison relies on non-zero SLOT_4 coupling.",
            expected_result_if_PHIGRADIENT_is_only_analogy="Benchmark comparison succeeds without gradient component.",
            expected_result_if_candidate_has_signal="Benchmark comparison remains valid for non-gradient observables.",
        )
    )

    return NegativeControlPlan(
        controls=controls,
        notes=[
            "Negative-control plan verifies model behavior without laundering mechanism debt.",
            "Includes a mandatory NO_SLOT4 control to guarantee benchmark independence from gradient claims.",
        ],
    )
