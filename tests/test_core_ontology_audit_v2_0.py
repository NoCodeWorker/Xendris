from pathlib import Path

from phyng.repository_audit.ontology import audit_core_ontology


def test_ontology_audit_detects_known_state_families():
    records = audit_core_ontology(Path("."))
    by_family = {record.state_family: record for record in records}

    assert "EpistemicMode" in by_family
    assert by_family["EpistemicMode"].definitions
    assert "BusinessValidationStatus" in by_family
    assert by_family["BusinessValidationStatus"].definitions
    assert by_family["WTPLevel"].definitions
