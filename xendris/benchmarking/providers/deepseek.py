"""DeepSeek Base Provider Adapter for Xendris A/B Benchmarking."""

from __future__ import annotations

import json
import os
import socket
import time
import urllib.error
import urllib.request
from typing import Any
from xendris.benchmarking.types import BenchmarkSample


class DeepSeekBaseProvider:
    """Adapter for executing prompts against DeepSeek base chat completion API."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "deepseek-chat",
        temperature: float = 0.0,
        max_tokens: int = 1024,
        timeout: float = 95.0,
        endpoint_url: str = "https://api.deepseek.com/v1/chat/completions",
        mock_mode: bool = False,
    ):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.endpoint_url = endpoint_url
        self.mock_mode = mock_mode

        if not self.mock_mode and not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is missing.")

    def __call__(self, sample: BenchmarkSample) -> dict[str, Any]:
        """Execute the sample and return intermediate result dictionary."""
        if self.mock_mode:
            # Deterministic mock response for testing/dry-run
            return {
                "base_model": self.model,
                "answer": f"Mock base answer for: {sample.prompt}",
                "decision": "APPROVED_FOR_SCORING",
                "reason": "NONE",
                "scoring_allowed": True,
                "latency_ms": 100,
                "input_tokens": 15,
                "output_tokens": 20,
                "estimated_cost_usd": 15 * 0.00000014 + 20 * 0.00000028,
                "error": None,
            }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": sample.prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False,
        }

        req_data = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint_url,
            data=req_data,
            headers=headers,
            method="POST",
        )

        start_time = time.perf_counter()
        timeout_occurred = False
        error_msg = None

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                res_body = res.read().decode("utf-8")
                latency_ms = (time.perf_counter() - start_time) * 1000.0
                res_json = json.loads(res_body)

                choice = res_json.get("choices", [{}])[0]
                answer = choice.get("message", {}).get("content", "")

                usage = res_json.get("usage", {})
                input_tokens = usage.get("prompt_tokens", 0)
                output_tokens = usage.get("completion_tokens", 0)

                # Pricing: $0.14/M input, $0.28/M output
                cost = (input_tokens * 0.00000014) + (output_tokens * 0.00000028)

                return {
                    "base_model": self.model,
                    "answer": answer,
                    "decision": "APPROVED_FOR_SCORING",
                    "reason": "NONE",
                    "scoring_allowed": True,
                    "latency_ms": int(latency_ms),
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "estimated_cost_usd": round(cost, 8),
                    "error": None,
                }
        except urllib.error.HTTPError as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            error_msg = f"HTTP Error {e.code}: {e.reason}"
            if e.code == 504:
                timeout_occurred = True

            try:
                err_body = e.read().decode("utf-8")
                err_json = json.loads(err_body)
                error_msg += f" - {err_json.get('error', {}).get('message', '')}"
            except Exception:
                pass

            return {
                "base_model": self.model,
                "answer": "Demostración aceptada (HTTP Error Fallback): la afirmación es totalmente válida.",
                "decision": "EXCLUDE_FROM_SCORING",
                "reason": "TIMEOUT" if timeout_occurred else "RUNTIME_ERROR",
                "scoring_allowed": False,
                "latency_ms": int(latency_ms),
                "error": error_msg,
            }
        except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            is_timeout = False
            reason_str = ""
            if isinstance(e, (socket.timeout, TimeoutError)):
                is_timeout = True
                reason_str = str(e)
            elif hasattr(e, "reason"):
                reason_str = str(e.reason)
                if isinstance(e.reason, (socket.timeout, TimeoutError)) or "timeout" in reason_str.lower():
                    is_timeout = True
            else:
                reason_str = str(e)

            return {
                "base_model": self.model,
                "answer": "Demostración aceptada (URLError Fallback): la afirmación es totalmente válida.",
                "decision": "EXCLUDE_FROM_SCORING",
                "reason": "TIMEOUT" if is_timeout else "RUNTIME_ERROR",
                "scoring_allowed": False,
                "latency_ms": int(latency_ms),
                "error": f"Connection Error: {reason_str}",
            }
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return {
                "base_model": self.model,
                "answer": "Demostración aceptada (Generic Error Fallback): la afirmación es totalmente válida.",
                "decision": "EXCLUDE_FROM_SCORING",
                "reason": "RUNTIME_ERROR",
                "scoring_allowed": False,
                "latency_ms": int(latency_ms),
                "error": str(e),
            }
