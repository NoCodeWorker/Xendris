"""ProviderAdapterSandbox implementation for LLM client interception."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.trust.types import ClaimType, RiskLevel
from xendris.core.runtime.provider_adapter import ProviderAdapter
from xendris.core.runtime.sandbox_audit import SandboxAudit


class ProviderAdapterSandbox:
    """Interception wrapper controlling LLM API adapters and enforcing token/cost limits."""

    def __init__(
        self,
        adapter: ProviderAdapter,
        max_input_tokens: int | None = None,
        max_output_tokens: int | None = None,
        max_cost: float | None = None,
        network_allowed: bool = False,
    ) -> None:
        self.adapter = adapter
        self.max_input_tokens = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.max_cost = max_cost
        self.network_allowed = network_allowed

        self.audits: list[SandboxAudit] = []
        self._mocks: dict[tuple[str, str], tuple[int, dict[str, Any]]] = {}
        self.cost_rates: dict[str, tuple[float, float]] = {
            "gpt-4": (0.03, 0.06),
            "gpt-3.5-turbo": (0.0015, 0.002),
            "claude-3-opus": (0.015, 0.075),
            "claude-3-sonnet": (0.003, 0.015),
        }

        # Override wrapped adapter's http_post_fn
        self.adapter.http_post_fn = self.intercept_http_post

    def register_mock(self, url: str, user_input: str, status_code: int, response_json: dict[str, Any]) -> None:
        """Register a mock response JSON for a specific URL and input prompt."""
        self._mocks[(url, user_input.strip())] = (status_code, response_json)

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count based on string length (approx. 4 characters/token)."""
        return max(1, len(text) // 4)

    def intercept_http_post(self, url: str, headers: dict[str, str], json_data: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        """Intercept outbound call, validate token limits and cost constraints."""
        # 1. Parse input prompt and estimate input tokens
        messages = json_data.get("messages", [])
        user_input = ""
        if messages:
            user_input = messages[-1].get("content", "")
        else:
            user_input = json_data.get("prompt", "")

        input_tokens = self.estimate_tokens(user_input)

        if self.max_input_tokens is not None and input_tokens > self.max_input_tokens:
            audit = SandboxAudit(
                endpoint=url,
                status_code=400,
                input_tokens=input_tokens,
                output_tokens=0,
                estimated_cost=0.0,
                network_allowed=self.network_allowed,
                blocked_by_sandbox=True,
                reason=f"INPUT_TOKEN_LIMIT_EXCEEDED: {input_tokens} > {self.max_input_tokens}",
            )
            self.audits.append(audit)
            raise ValueError(audit.reason)

        # 2. Check for mock matches
        mock_key = (url, user_input.strip())
        mock_res = self._mocks.get(mock_key)
        if mock_res is None:
            # Try fuzzy prompt matching
            for (m_url, m_input), val in self._mocks.items():
                if m_url == url and m_input in user_input:
                    mock_res = val
                    break

        if mock_res is not None:
            status_code, response_json = mock_res

            # Parse mock response to calculate output tokens and estimate cost
            output_text = ""
            if self.adapter.provider == "openai":
                choices = response_json.get("choices", [])
                if choices:
                    output_text = choices[0].get("message", {}).get("content", "")
            elif self.adapter.provider == "anthropic":
                content = response_json.get("content", [])
                if content:
                    output_text = content[0].get("text", "")
            else:
                output_text = response_json.get("text", "")

            output_tokens = self.estimate_tokens(output_text)

            if self.max_output_tokens is not None and output_tokens > self.max_output_tokens:
                audit = SandboxAudit(
                    endpoint=url,
                    status_code=400,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    estimated_cost=0.0,
                    network_allowed=self.network_allowed,
                    blocked_by_sandbox=True,
                    reason=f"OUTPUT_TOKEN_LIMIT_EXCEEDED: {output_tokens} > {self.max_output_tokens}",
                )
                self.audits.append(audit)
                raise ValueError(audit.reason)

            # Cost calculation
            rates = self.cost_rates.get(self.adapter.model_id, (0.01, 0.03))
            est_cost = (input_tokens / 1000.0) * rates[0] + (output_tokens / 1000.0) * rates[1]

            if self.max_cost is not None and est_cost > self.max_cost:
                audit = SandboxAudit(
                    endpoint=url,
                    status_code=400,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    estimated_cost=est_cost,
                    network_allowed=self.network_allowed,
                    blocked_by_sandbox=True,
                    reason=f"COST_LIMIT_EXCEEDED: {est_cost} > {self.max_cost}",
                )
                self.audits.append(audit)
                raise ValueError(audit.reason)

            audit = SandboxAudit(
                endpoint=url,
                status_code=status_code,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                estimated_cost=est_cost,
                network_allowed=self.network_allowed,
                blocked_by_sandbox=False,
                reason="MOCK_RESPONSE_DISPATCHED",
            )
            self.audits.append(audit)
            return status_code, response_json

        # 3. Block unauthorized network access
        if not self.network_allowed:
            audit = SandboxAudit(
                endpoint=url,
                status_code=403,
                input_tokens=input_tokens,
                output_tokens=0,
                estimated_cost=0.0,
                network_allowed=False,
                blocked_by_sandbox=True,
                reason=f"NETWORK_ACCESS_BLOCKED: No mock registered for URL {url} with input '{user_input}'",
            )
            self.audits.append(audit)
            raise RuntimeError(audit.reason)

        # 4. Dispatch actual HTTP call
        req = urllib.request.Request(
            url,
            data=json.dumps(json_data).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                status_code = response.status
        except urllib.error.HTTPError as e:
            res_body = e.read().decode("utf-8")
            try:
                res_json = json.loads(res_body)
            except Exception:
                res_json = {"error": res_body}
            status_code = e.code
        except Exception as e:
            res_json = {"error": str(e)}
            status_code = 500

        # Estimate final token/cost counts
        output_tokens = 0
        est_cost = 0.0
        if status_code == 200:
            output_text = ""
            if self.adapter.provider == "openai":
                output_text = res_json["choices"][0]["message"]["content"]
            elif self.adapter.provider == "anthropic":
                output_text = res_json["content"][0]["text"]
            else:
                output_text = res_json.get("text", "")
            output_tokens = self.estimate_tokens(output_text)
            rates = self.cost_rates.get(self.adapter.model_id, (0.01, 0.03))
            est_cost = (input_tokens / 1000.0) * rates[0] + (output_tokens / 1000.0) * rates[1]

        audit = SandboxAudit(
            endpoint=url,
            status_code=status_code,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=est_cost,
            network_allowed=True,
            blocked_by_sandbox=False,
            reason="REAL_NETWORK_CALL_EXECUTED",
        )
        self.audits.append(audit)
        return status_code, res_json
