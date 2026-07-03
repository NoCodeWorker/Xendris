from phyng.priority_exact_fill.priority_fill import is_validation_ready
from phyng.priority_exact_fill.schemas import PriorityExactFillRecord


def test_validation_ready_requires_exact_content():
    record = PriorityExactFillRecord(
        priority_source_id="SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE",
        source_id="SRC-PHI-V32-001",
        slot_id="SLOT_1_DECOHERENCE_BASELINE_MODELS",
        source_text_status="SOURCE_TEXT_AVAILABLE_LOCAL",
        location_type="SECTION",
        location_value="2",
        review_status="EXACT_FILL_VALIDATION_READY",
    )

    assert not is_validation_ready(record)

    record.exact_quote = "short exact local excerpt"

    assert is_validation_ready(record)


def test_unresolved_priority_record_requires_source_text():
    record = PriorityExactFillRecord(
        priority_source_id="SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE",
        source_id="SRC-PHI-V32-002",
        slot_id="SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT",
    )

    assert record.source_text_status == "SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD"
    assert record.review_status == "EXACT_FILL_REQUIRES_SOURCE_TEXT"
    assert not record.validation_ready
