from __future__ import annotations

import json
from unittest.mock import patch

import pytest

import io
from urllib.error import HTTPError

from xendris.benchmarking.agentic_programming.agents.openai_provider import (
    call_openai,
    _is_gpt5_model,
    _redact_secrets,
    _extract_content_from_responses,
    _extract_content_from_chat,
    _extract_usage,
    _get_cost_quality,
)


class _FakeHTTPError(HTTPError):
    def __init__(self, code: int = 400, msg: str = "Bad Request", body: bytes = b""):
        fp = io.BytesIO(body) if body else None
        super().__init__("http://example.com", code, msg, {}, fp)


class TestGpt5ModelDetection:
    def test_gpt5_prefix_detected(self):
        assert _is_gpt5_model("gpt-5.5") is True

    def test_gpt5_model_array_detected(self):
        assert _is_gpt5_model("gpt-5-preview") is True

    def test_gpt4_model_not_detected(self):
        assert _is_gpt5_model("gpt-4.1-mini") is False

    def test_gpt4_model_not_detected_2(self):
        assert _is_gpt5_model("gpt-4.1-nano") is False

    def test_model_with_org_prefix(self):
        assert _is_gpt5_model("org/gpt-5.5") is True
        assert _is_gpt5_model("org/gpt-4.1-mini") is False


class TestRedactSecrets:
    def test_redacts_sk_key(self):
        result = _redact_secrets("sk-abc123def456ghi789jkl")
        assert "sk-abc123" not in result
        assert "REDACTED" in result

    def test_redacts_bearer_token(self):
        result = _redact_secrets("Authorization: Bearer sk-xxx123")
        assert "Bearer sk-xxx" not in result
        assert "REDACTED" in result

    def test_redacts_authorization_header(self):
        result = _redact_secrets("Authorization: Bearer tokensecret123")
        assert "tokensecret" not in result
        assert "REDACTED" in result

    def test_no_secrets_unchanged(self):
        text = "Hello, this is a normal message"
        assert _redact_secrets(text) == text

    def test_redacted_body_no_leak(self):
        body = '{"error": {"message": "Invalid API key: sk-abc123xyz789"}}'
        redacted = _redact_secrets(body)
        assert "sk-abc123" not in redacted
        assert "REDACTED" in redacted
        assert "error" in redacted


class TestExtractContentResponses:
    def test_extracts_output_text_from_message(self):
        body = {
            "output": [
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {"type": "output_text", "text": "def solve(): return 42"}
                    ],
                }
            ]
        }
        assert _extract_content_from_responses(body) == "def solve(): return 42"

    def test_returns_none_when_no_message(self):
        assert _extract_content_from_responses({"output": []}) is None

    def test_skips_reasoning_items(self):
        body = {
            "output": [
                {"type": "reasoning", "reasoning": "thinking..."},
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [
                        {"type": "output_text", "text": "final answer"}
                    ],
                },
            ]
        }
        assert _extract_content_from_responses(body) == "final answer"


class TestExtractContentChat:
    def test_extracts_from_choices(self):
        body = {
            "choices": [
                {"message": {"content": "hello world"}}
            ]
        }
        assert _extract_content_from_chat(body) == "hello world"

    def test_returns_none_on_empty_choices(self):
        assert _extract_content_from_chat({"choices": []}) is None


class TestExtractUsage:
    def test_chat_completions_usage(self):
        body = {"usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150}}
        u = _extract_usage(body, use_responses_api=False)
        assert u["input_tokens"] == 100
        assert u["output_tokens"] == 50
        assert u["total_tokens"] == 150

    def test_responses_api_usage(self):
        body = {"usage": {"input_tokens": 200, "output_tokens": 80, "total_tokens": 280}}
        u = _extract_usage(body, use_responses_api=True)
        assert u["input_tokens"] == 200
        assert u["output_tokens"] == 80
        assert u["total_tokens"] == 280

    def test_missing_usage_defaults(self):
        u = _extract_usage({}, use_responses_api=False)
        assert u["input_tokens"] == 0
        assert u["output_tokens"] == 0
        assert u["total_tokens"] == 0


class TestCostQuality:
    def test_known_pricing(self):
        assert _get_cost_quality("gpt-4.1-mini") == "known_pricing"
        assert _get_cost_quality("gpt-4.1-nano") == "known_pricing"

    def test_unknown_pricing_fallback(self):
        assert _get_cost_quality("gpt-5.5") == "unknown_pricing_fallback"
        assert _get_cost_quality("gpt-5-preview") == "unknown_pricing_fallback"


class TestResponsesApiPathGpt5:
    """GPT-5.5 uses Responses API (not Chat Completions)."""

    def test_uses_responses_endpoint_for_gpt5(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")
        captured = {}

        def fake_urlopen(req, *args, **kwargs):
            captured["url"] = req.full_url
            captured["method"] = req.method
            captured["data"] = json.loads(req.data) if req.data else {}
            import io
            body = {
                "id": "resp-123", "object": "response", "status": "completed",
                "model": "gpt-5.5",
                "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "ok"}]}],
                "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            }
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        import ssl
        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        assert "responses" in captured["url"]
        assert "chat/completions" not in captured["url"]
        assert captured["method"] == "POST"

    def test_max_output_tokens_not_max_tokens(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")
        captured = {}

        def fake_urlopen(req, *args, **kwargs):
            captured["data"] = json.loads(req.data) if req.data else {}
            import io
            body = {
                "id": "resp-123", "object": "response", "status": "completed",
                "model": "gpt-5.5",
                "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "ok"}]}],
                "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            }
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            call_openai("sys", "user", model="gpt-5.5", max_tokens=4096)

        payload = captured["data"]
        assert "max_output_tokens" in payload
        assert payload["max_output_tokens"] == 4096
        assert "max_tokens" not in payload

    def test_no_unsupported_parameters_for_gpt5(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")
        captured = {}

        def fake_urlopen(req, *args, **kwargs):
            captured["data"] = json.loads(req.data) if req.data else {}
            import io
            body = {
                "id": "resp-123", "object": "response", "status": "completed",
                "model": "gpt-5.5",
                "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "ok"}]}],
                "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            }
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            call_openai("sys", "user", model="gpt-5.5", temperature=0.2)

        payload = captured["data"]
        # temperature should NOT be sent for gpt-5.x responses API
        assert "temperature" not in payload
        assert "max_output_tokens" in payload
        assert "instructions" in payload
        assert payload["instructions"] == "sys"
        assert payload["input"] == "user"

    def test_output_text_extracted_successfully(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")

        def fake_urlopen(req, *args, **kwargs):
            body = {
                "id": "resp-123", "object": "response", "status": "completed",
                "model": "gpt-5.5",
                "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "patch content here"}]}],
                "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            }
            import io
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        assert content == "patch content here"
        assert error is None
        assert model == "gpt-5.5"

    def test_tokens_recorded_on_success(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")

        def fake_urlopen(req, *args, **kwargs):
            body = {
                "id": "resp-123", "object": "response", "status": "completed",
                "model": "gpt-5.5",
                "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "ok"}]}],
                "usage": {"input_tokens": 150, "output_tokens": 60, "total_tokens": 210},
            }
            import io
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        assert inp == 150
        assert out == 60
        assert cost is not None

    def test_cost_quality_is_fallback_for_gpt5(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")

        def fake_urlopen(req, *args, **kwargs):
            body = {
                "id": "resp-123", "object": "response", "status": "completed",
                "model": "gpt-5.5",
                "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "ok"}]}],
                "usage": {"input_tokens": 100, "output_tokens": 50, "total_tokens": 150},
            }
            import io
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            from xendris.benchmarking.agentic_programming.agents.openai_provider import _get_cost_quality
            assert _get_cost_quality("gpt-5.5") == "unknown_pricing_fallback"

    def test_latency_recorded_on_success(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")

        def fake_urlopen(req, *args, **kwargs):
            body = {
                "id": "resp-123", "object": "response", "status": "completed",
                "model": "gpt-5.5",
                "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "ok"}]}],
                "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            }
            import io
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        assert latency is not None


class TestChatCompletionsPathGpt4:
    """GPT-4.x continues using Chat Completions API."""

    def test_uses_chat_completions_endpoint(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")
        captured = {}

        def fake_urlopen(req, *args, **kwargs):
            captured["url"] = req.full_url
            import io
            body = {
                "id": "chat-123", "object": "chat.completion",
                "model": "gpt-4.1-mini",
                "choices": [{"message": {"content": "ok"}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            }
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            call_openai("sys", "user", model="gpt-4.1-mini")

        assert "chat/completions" in captured["url"]
        assert "responses" not in captured["url"]

    def test_uses_max_tokens_not_max_output_tokens(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")
        captured = {}

        def fake_urlopen(req, *args, **kwargs):
            captured["data"] = json.loads(req.data) if req.data else {}
            import io
            body = {
                "id": "chat-123", "object": "chat.completion",
                "model": "gpt-4.1-mini",
                "choices": [{"message": {"content": "ok"}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            }
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            call_openai("sys", "user", model="gpt-4.1-mini", max_tokens=2048)

        payload = captured["data"]
        assert "max_tokens" in payload
        assert payload["max_tokens"] == 2048
        assert "max_output_tokens" not in payload

    def test_temperature_sent_for_gpt4(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")
        captured = {}

        def fake_urlopen(req, *args, **kwargs):
            captured["data"] = json.loads(req.data) if req.data else {}
            import io
            body = {
                "id": "chat-123", "object": "chat.completion",
                "model": "gpt-4.1-mini",
                "choices": [{"message": {"content": "ok"}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            }
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            call_openai("sys", "user", model="gpt-4.1-mini", temperature=0.5)

        payload = captured["data"]
        assert "temperature" in payload
        assert payload["temperature"] == 0.5


class TestErrorHandling:
    def test_http_error_body_captured_and_redacted(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")
        body_bytes = b'{"error": {"message": "Invalid model: gpt-5.5", "type": "invalid_request_error"}}'

        def fake_urlopen(req, *args, **kwargs):
            raise _FakeHTTPError(code=400, msg="Bad Request", body=body_bytes)

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        assert content is None
        assert error is not None
        assert "HTTP Error 400" in error
        assert "Invalid model" in error
        assert "sk-test" not in error

    def test_latency_recorded_on_http_error(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")

        def fake_urlopen(req, *args, **kwargs):
            raise _FakeHTTPError(code=401, msg="Unauthorized", body=b'{"error": {"message": "Invalid credentials"}}')

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        assert latency is not None

    def test_api_key_redacted_in_secrets_check(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-abc123def456ghi789jkl")

        def fake_urlopen(req, *args, **kwargs):
            body = {
                "id": "resp-123", "object": "response", "status": "completed",
                "model": "gpt-5.5",
                "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "ok"}]}],
                "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            }
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        result_text = str(content) + str(error) + str(model)
        assert "sk-abc" not in result_text

    def test_generic_exception_records_latency(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")

        def fake_urlopen(req, *args, **kwargs):
            raise ConnectionError("Connection refused")

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        assert latency is not None
        assert error is not None
        assert "Connection refused" in error

    def test_no_body_text_on_http_error(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-12345")

        def fake_urlopen(req, *args, **kwargs):
            raise _FakeHTTPError(code=500, msg="Internal Server Error")

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        assert error is not None
        assert "HTTP Error 500" in error

    def test_no_api_key_returns_error(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")
        assert content is None
        assert error is not None
        assert "No API key" in error


class TestSecretsNotInArtifacts:
    def test_no_secrets_in_nominal_response(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-secret-key-for-testing-only-12345")

        def fake_urlopen(req, *args, **kwargs):
            import io
            body = {
                "id": "resp-123", "object": "response", "status": "completed",
                "model": "gpt-5.5",
                "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "patch here"}]}],
                "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
            }
            return io.BytesIO(json.dumps(body).encode("utf-8"))

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        combined = str(content) + str(error) + str(model) + str(latency) + str(cost) + str(inp) + str(out)
        for secret_pattern in ["sk-secret", "Authorization", "Bearer"]:
            assert secret_pattern not in combined, f"Secret pattern '{secret_pattern}' leaked"

    def test_no_secrets_in_error_body(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-leaked-key-12345")

        class FakeHTTPError(Exception):
            def __init__(self):
                self.code = 400
                self.reason = "Bad Request"
                self.headers = {}
                self._body = b'{"error": {"message": "Invalid API key: sk-leaked-key-12345"}}'

            def read(self):
                return self._body

        def fake_urlopen(req, *args, **kwargs):
            raise FakeHTTPError()

        with patch("urllib.request.urlopen", fake_urlopen), patch("ssl.create_default_context"):
            content, latency, cost, model, error, inp, out = call_openai("sys", "user", model="gpt-5.5")

        assert error is not None
        assert "sk-leaked-key" not in error
