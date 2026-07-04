"""ProviderAdapter implementation for real LLM API providers."""

from __future__ import annotations

import hashlib
from typing import Any, Callable
from xendris.core.runtime.adapter import ModelAdapter
from xendris.core.runtime.request import RuntimeRequest
from xendris.core.runtime.response import RuntimeCandidate


class ProviderAdapter(ModelAdapter):
    """Adapter connecting to external LLM provider APIs with interceptable network dispatch."""

    def __init__(
        self,
        model_id: str,
        provider: str,
        api_key: str | None = None,
        base_url: str | None = None,
        http_post_fn: Callable[[str, dict[str, str], dict[str, Any]], tuple[int, dict[str, Any]]] | None = None,
    ) -> None:
        self.model_id = model_id
        self.provider = provider.lower()
        self.api_key = api_key
        self.base_url = base_url
        self.http_post_fn = http_post_fn or self.default_http_post

    def default_http_post(self, url: str, headers: dict[str, str], json_data: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        """Fallback direct execution blocker."""
        raise RuntimeError("Direct network access blocked by default. Use ProviderAdapterSandbox.")

    def generate(self, request: RuntimeRequest) -> RuntimeCandidate:
        """Construct payloads and invoke the dispatch delegate."""
        # 1. Determine endpoint URL and construct payloads
        if self.provider == "openai":
            url = self.base_url or "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key or 'mock-key'}",
                "Content-Type": "application/json",
            }
            json_data = {
                "model": self.model_id,
                "messages": [{"role": "user", "content": request.user_input}],
            }
        elif self.provider == "anthropic":
            url = self.base_url or "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": self.api_key or "mock-key",
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            }
            json_data = {
                "model": self.model_id,
                "messages": [{"role": "user", "content": request.user_input}],
                "max_tokens": 1024,
            }
        else:
            url = self.base_url or f"https://api.{self.provider}.com/v1/completions"
            headers = {"Content-Type": "application/json"}
            json_data = {"prompt": request.user_input}

        # 2. Invoke dispatch
        status_code, response_json = self.http_post_fn(url, headers, json_data)

        if status_code != 200:
            raise RuntimeError(f"Provider API returned error status {status_code}: {response_json}")

        # 3. Parse content based on schema
        if self.provider == "openai":
            content = response_json["choices"][0]["message"]["content"]
        elif self.provider == "anthropic":
            content = response_json["content"][0]["text"]
        else:
            content = response_json.get("text", "")

        raw_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        return RuntimeCandidate(
            candidate_id=f"CAND-{request.request_id}",
            model_id=self.model_id,
            provider=self.provider,
            content=content,
            raw_output_hash=raw_hash,
            metadata={"source": "provider_adapter", "endpoint": url},
        )
