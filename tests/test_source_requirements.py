from phyng.evidence import default_source_requirements


def test_source_requirement_created_for_missing_compton_source():
    requirements = default_source_requirements()
    requirement = next(req for req in requirements if req.requirement_id == "REQ-SRC-001")

    assert requirement.topic == "Reduced Compton wavelength"
    assert requirement.status == "REQUIRED"
    assert "CLAIM-QB-001" in requirement.linked_claim_ids
    assert requirement.required_trust_level == "HIGH"
