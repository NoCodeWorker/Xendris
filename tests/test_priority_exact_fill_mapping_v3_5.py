from phyng.priority_exact_fill.equation_observable_map import build_priority_equation_observable_map
from phyng.priority_exact_fill.parameter_range_map import build_priority_parameter_range_map
from phyng.priority_exact_fill.schemas import PriorityExactFillRecord


def test_priority_exact_fill_mapping_uses_only_ready_records():
    ready = PriorityExactFillRecord(
        priority_source_id="SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE",
        source_id="SRC-PHI-V32-001",
        slot_id="SLOT_1_DECOHERENCE_BASELINE_MODELS",
        source_text_status="SOURCE_TEXT_AVAILABLE_LOCAL",
        location_type="SECTION",
        location_value="2",
        equation_text="local equation text",
        observable_text="local observable text",
        parameter_range_text="local parameter range",
        benchmark_range_text="local benchmark range",
        review_status="EXACT_FILL_VALIDATION_READY",
        validation_ready=True,
    )
    unresolved = PriorityExactFillRecord(
        priority_source_id="SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE",
        source_id="SRC-PHI-V32-002",
        slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
        equation_text="must not map",
    )

    equation_map = build_priority_equation_observable_map([ready, unresolved])
    parameter_map = build_priority_parameter_range_map([ready, unresolved])

    assert len(equation_map.entries) == 1
    assert equation_map.entries[0].source_id == "SRC-PHI-V32-001"
    assert len(parameter_map.entries) == 1
    assert parameter_map.entries[0].source_id == "SRC-PHI-V32-001"
