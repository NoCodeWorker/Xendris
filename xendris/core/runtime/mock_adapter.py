"""MockModelAdapter for deterministic test execution."""

from __future__ import annotations

import hashlib
from typing import Any
from xendris.core.runtime.adapter import ModelAdapter
from xendris.core.runtime.request import RuntimeRequest
from xendris.core.runtime.response import RuntimeCandidate


class MockModelAdapter(ModelAdapter):
    """Deterministic, scripted model adapter that simulates model outputs in memory."""

    def __init__(self) -> None:
        self._outputs: dict[tuple[str, str], str] = {}
        self._intent_outputs: dict[tuple[str, str], str] = {}
        self._default_output: str = "Default deterministic response content."

    def register_output(self, model_id: str, request_id: str, content: str) -> None:
        """Register a scripted output for a specific model ID and request ID."""
        self._outputs[(model_id, request_id)] = content

    def register_intent_output(self, model_id: str, user_intent: str, content: str) -> None:
        """Register a scripted output for a specific model ID and user intent string."""
        self._intent_outputs[(model_id, user_intent)] = content

    def set_default_output(self, content: str) -> None:
        """Set a fallback default output string."""
        self._default_output = content

    def generate(self, request: RuntimeRequest) -> RuntimeCandidate:
        """Deterministically generate a candidate response without invoking remote APIs."""
        model_id = request.metadata.get("forced_model_id", "strong-coder")
        provider = request.metadata.get("forced_provider", "test-prov")

        # 1. Try to match registered request ID
        content = self._outputs.get((model_id, request.request_id))

        # 2. Try to match intent
        if content is None:
            content = self._intent_outputs.get((model_id, request.user_intent))

        # 3. Fallback to default
        if content is None:
            content = self._default_output

        # Compute output hash
        raw_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        return RuntimeCandidate(
            candidate_id=f"CAND-{request.request_id}",
            model_id=model_id,
            provider=provider,
            content=content,
            raw_output_hash=raw_hash,
            metadata={"source": "mock_adapter"},
        )
