"""
Tests for phyng.candidates.term_families
"""

from phyng.candidates.term_families import get_candidate_term_families, CandidateFamily

def test_candidate_families_exist():
    families = get_candidate_term_families()
    assert len(families) == 4
    for key, fam in families.items():
        assert isinstance(fam, CandidateFamily)
        assert fam.candidate_family_id == key
        assert len(fam.formula) > 0

def test_b_suppressed_candidate_is_negative_control():
    families = get_candidate_term_families()
    b_fam = families["B_SUPPRESSED"]
    assert b_fam.default_admissibility == "ADMISSIBLE_NEGATIVE_CONTROL"
    assert b_fam.dimensionless_core == "B"

def test_qb_candidate_is_structural_control():
    families = get_candidate_term_families()
    qb_fam = families["QB_STRUCTURAL"]
    assert qb_fam.default_admissibility == "ADMISSIBLE_NEGATIVE_CONTROL"
    assert qb_fam.dimensionless_core == "Q * B"
