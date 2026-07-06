"""
xendris.core.algebra — [EXPERIMENTAL] Claim Object Algebra.

WARNING: This module is EXPERIMENTAL. The types below are minimal stubs
to satisfy imports from other experimental packages (runtime, orchestrator).
The full implementation lives in the `experimental-trust-layers` branch.
"""

from __future__ import annotations

from typing import Any


class ClaimObject:
    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)


__all__ = ["ClaimObject"]
