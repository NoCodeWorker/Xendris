"""ModelAdapter interface definition."""

from __future__ import annotations

from typing import Protocol
from xendris.core.runtime.request import RuntimeRequest
from xendris.core.runtime.response import RuntimeCandidate


class ModelAdapter(Protocol):
    """Protocol for model candidate generation without external network calls."""

    def generate(self, request: RuntimeRequest) -> RuntimeCandidate:
        """Generate a response candidate for the given runtime request."""
        ...
