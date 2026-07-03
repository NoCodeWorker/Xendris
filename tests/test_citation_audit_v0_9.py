from phyng.evidence.source_records_v0_9 import SourceRecordV09
from phyng.evidence.citation_audit_v0_9 import audit_citation_v0_9


def test_url_only_fails_no_local_content():
    record = SourceRecordV09(
        source_id="SRC-URL-ONLY",
        title="Decoherence Paper",
        authors=["Author"],
        year="2020",
        local_path=None,
        url="http://dec.pdf",
        ingestion_status="CANDIDATE_ONLY"
    )
    result = audit_citation_v0_9(record)
    assert result.passed is False
    assert result.audit_status == "FAILED_NO_LOCAL_CONTENT"


def test_metadata_only_does_not_unlock_baseline():
    # If ingestion_status is INGESTED_METADATA_ONLY, it passes but is PASSED_METADATA_ONLY
    # And formula/observable supports are forbidden
    record = SourceRecordV09(
        source_id="SRC-META-ONLY",
        title="Decoherence Paper",
        authors=["Author"],
        year="2020",
        local_path="tests/test_citation_audit_v0_9.py", # exists
        ingestion_status="INGESTED_METADATA_ONLY",
        metadata_status="COMPLETE"
    )
    result = audit_citation_v0_9(record)
    assert result.passed is True
    assert result.audit_status == "PASSED_METADATA_ONLY"
    assert "FORMULA_SUPPORT" in result.forbidden_support_types


def test_passed_limited_allows_direct_formula_support():
    record = SourceRecordV09(
        source_id="SRC-LIMITED-OK",
        title="Decoherence Paper",
        authors=["Author"],
        year="2020",
        local_path="tests/test_citation_audit_v0_9.py", # exists
        ingestion_status="INGESTED_WITH_EXTRACTS",
        metadata_status="COMPLETE"
    )
    result = audit_citation_v0_9(record)
    assert result.passed is True
    assert result.audit_status == "PASSED_LIMITED"
    assert "FORMULA_SUPPORT" in result.allowed_support_types


def test_low_trust_blocks_hard_claim():
    record = SourceRecordV09(
        source_id="SRC-LOW-TRUST",
        title="Decoherence Paper",
        authors=["Author"],
        year="2020",
        local_path="tests/test_citation_audit_v0_9.py", # exists
        ingestion_status="INGESTED_WITH_EXTRACTS",
        metadata_status="COMPLETE",
        trust_level="LOW"
    )
    result = audit_citation_v0_9(record)
    assert result.passed is False
    assert result.audit_status == "FAILED_LOW_TRUST"


def test_contradictory_source_blocks_claim():
    record = SourceRecordV09(
        source_id="SRC-CONTRA",
        title="Decoherence Paper",
        authors=["Author"],
        year="2020",
        local_path="tests/test_citation_audit_v0_9.py", # exists
        ingestion_status="INGESTED_WITH_EXTRACTS",
        metadata_status="COMPLETE",
        notes="This contradicts Markovian noise."
    )
    result = audit_citation_v0_9(record)
    assert result.passed is False
    assert result.audit_status == "FAILED_CONTRADICTORY"
