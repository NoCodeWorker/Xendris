"""
xendris.core.local — [EXPERIMENTAL] Local Context and Local Claim Algebra.

WARNING: This module is EXPERIMENTAL. The types below are minimal stubs
to satisfy imports from other experimental packages (runtime, router).
The full implementation lives in the `experimental-trust-layers` branch.
"""

from __future__ import annotations

from enum import Enum


class LocalContext(str, Enum):
    GENERAL = "GENERAL"
    CODE = "CODE"
    SCIENCE = "SCIENCE"
    MEDICINE = "MEDICINE"
    LAW = "LAW"
    FINANCE = "FINANCE"
    CREATIVE = "CREATIVE"
    CUSTOMER = "CUSTOMER"
    BENCHMARK = "BENCHMARK"
    PRODUCTION = "PRODUCTION"
    DOCUMENTATION = "DOCUMENTATION"
    LATENCY = "LATENCY"


__all__ = ["LocalContext"]
