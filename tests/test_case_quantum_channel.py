"""
Tests for quantum channel (depolarizing) case study.
"""

import pytest

from phyng.case_studies.quantum_channel import (
    depolarizing_distribution,
    quantum_channel_trace_case,
)
from phyng.errors import InvalidProbabilityError


def test_depolarizing_distribution_p_zero():
    dist = depolarizing_distribution(0.0)
    assert dist[0] == 1.0
    assert dist[1] == 0.0


def test_depolarizing_distribution_p_one():
    dist = depolarizing_distribution(1.0)
    assert dist[0] == 0.5
    assert dist[1] == 0.5


def test_depolarizing_distribution_rejects_invalid_p():
    with pytest.raises(InvalidProbabilityError):
        depolarizing_distribution(1.5)
    with pytest.raises(InvalidProbabilityError):
        depolarizing_distribution(-0.1)


def test_depolarizing_tau_zero_when_p_zero():
    """p=0 → identity channel → τ=0 → NULL_TRACE."""
    result = quantum_channel_trace_case(p=0.0)
    assert result["tau"] == 0.0
    assert result["trace_type"] == "NULL_TRACE"
    assert result["claim_status"] == "NOT_DETECTABLE"


def test_depolarizing_tau_positive_when_p_positive():
    """p>0 → depolarization → τ>0 → DETECTABLE_TRACE."""
    result = quantum_channel_trace_case(p=0.1)
    assert result["tau"] > 0
    assert result["trace_type"] == "DETECTABLE_TRACE"
    assert result["claim_status"] == "ALLOWED"


def test_depolarizing_case_id():
    result = quantum_channel_trace_case(p=0.5)
    assert result["case_id"] == "QC-DEPOLARIZING-001"


def test_depolarizing_small_p_not_detectable():
    """Very small p with large epsilon → NOT_DETECTABLE."""
    result = quantum_channel_trace_case(p=1e-8, epsilon_exp=1.0)
    assert result["trace_type"] == "NOT_DETECTABLE"
    assert result["claim_status"] == "NOT_DETECTABLE"
