"""
Tests for mesoscopic interferometer case study.
"""

from phyng.case_studies.mesoscopic_interferometer import mesoscopic_interferometer_case


def test_mesoscopic_case_runs():
    result = mesoscopic_interferometer_case()
    assert result["case_id"] == "MESO-INT-001"


def test_mesoscopic_negative_bound():
    """B is negligible → NEGATIVE_BOUND_TRACE."""
    result = mesoscopic_interferometer_case()
    assert result["trace_type"] == "NEGATIVE_BOUND_TRACE"


def test_mesoscopic_scale_accepted():
    result = mesoscopic_interferometer_case()
    assert result["scale_review_status"] == "ACCEPTED"


def test_mesoscopic_Q_order_of_magnitude():
    """Q ≈ 3.5e-19."""
    result = mesoscopic_interferometer_case()
    assert 1e-20 < result["Q"] < 1e-17


def test_mesoscopic_B_order_of_magnitude():
    """B ≈ 7.4e-38."""
    result = mesoscopic_interferometer_case()
    assert 1e-39 < result["B"] < 1e-36


def test_mesoscopic_QB_order_of_magnitude():
    """QB ≈ 2.6e-56."""
    result = mesoscopic_interferometer_case()
    assert 1e-57 < result["QB"] < 1e-54


def test_mesoscopic_qb_valid():
    result = mesoscopic_interferometer_case()
    assert result["qb_valid"] is True


def test_mesoscopic_forbidden_interpretation():
    result = mesoscopic_interferometer_case()
    assert "predicts" in result["forbidden_interpretation"].lower()
