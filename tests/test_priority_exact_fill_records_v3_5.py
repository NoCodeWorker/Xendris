from phyng.campaigns.phi_gradient_exact_extract_review import run_phi_gradient_exact_extract_review_campaign
from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.priority_exact_fill.review_gate import run_phi_gradient_priority_exact_fill_gate
from phyng.priority_exact_fill.schemas import PriorityExactFillRecord


def test_no_quote_or_range_fabrication(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    run_phi_gradient_exact_extract_review_campaign(tmp_path)

    result = run_phi_gradient_priority_exact_fill_gate(tmp_path)

    assert result.status == "PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT"
    assert result.priority_records
    assert all(record.exact_quote is None for record in result.priority_records)
    assert all(record.parameter_range_text is None for record in result.priority_records)
    assert all(record.benchmark_range_text is None for record in result.priority_records)
    assert result.source_text_required_count == 5


def test_all_unavailable_status_requires_source_text(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    run_phi_gradient_exact_extract_review_campaign(tmp_path)

    result = run_phi_gradient_priority_exact_fill_gate(tmp_path)

    assert result.status == "PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT"
    assert result.validation_ready_count == 0
    assert result.unresolved_count == 5


def test_partial_status_when_some_sources_ready(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    run_phi_gradient_exact_extract_review_campaign(tmp_path)
    ready_record = PriorityExactFillRecord(
        priority_source_id="SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE",
        source_id="SRC-PHI-V32-001",
        slot_id="SLOT_1_DECOHERENCE_BASELINE_MODELS",
        source_text_status="SOURCE_TEXT_AVAILABLE_LOCAL",
        location_type="SECTION",
        location_value="2",
        exact_quote="short exact local excerpt",
        review_status="EXACT_FILL_VALIDATION_READY",
        validation_ready=True,
    )
    unresolved_record = PriorityExactFillRecord(
        priority_source_id="SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE",
        source_id="SRC-PHI-V32-002",
        slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
    )

    result = run_phi_gradient_priority_exact_fill_gate(tmp_path, priority_records=[ready_record, unresolved_record])

    assert result.status == "PHI_GRADIENT_PRIORITY_EXTRACTS_PARTIAL"
    assert result.validation_ready_count == 1
    assert result.unresolved_count == 1
