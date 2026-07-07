from __future__ import annotations

import json
import os
import re
import time
from typing import Any

OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_MAX_TOKENS = 4096

GPT5_MODEL_PREFIXES = ("gpt-5",)


def _is_gpt5_model(model: str) -> bool:
    base = model.split("/")[-1] if "/" in model else model
    return base.startswith(GPT5_MODEL_PREFIXES)


def get_openai_api_key() -> str | None:
    return os.environ.get("OPENAI_API_KEY")


def get_openai_transport() -> str:
    if os.environ.get("OPENAI_API_KEY"):
        return "direct"
    return "unknown"


def _redact_secrets(text: str) -> str:
    redacted = re.sub(r"sk-[A-Za-z0-9]{8,}", "sk-...REDACTED", text)
    redacted = re.sub(r"Bearer\s+\S+", "Bearer REDACTED", redacted)
    redacted = re.sub(r"Authorization\s*:\s*\S+", "Authorization: REDACTED", redacted)
    return redacted


def _build_redacted_error_message(
    status_code: int,
    reason: str,
    body_text: str | None,
) -> str:
    if body_text:
        redacted_body = _redact_secrets(body_text[:500])
        return f"HTTP Error {status_code}: {reason} | Body: {redacted_body}"
    return f"HTTP Error {status_code}: {reason}"


def _extract_content_from_responses(body: dict) -> str | None:
    output = body.get("output", [])
    for item in output:
        if item.get("type") != "message":
            continue
        content_list = item.get("content", [])
        for content_item in content_list:
            if content_item.get("type") == "output_text":
                return content_item.get("text")
    return None


def _extract_content_from_chat(body: dict) -> str | None:
    choices = body.get("choices", [])
    if not choices:
        return None
    return choices[0].get("message", {}).get("content")


def _extract_usage(body: dict, use_responses_api: bool) -> dict[str, int]:
    usage = body.get("usage", {})
    if use_responses_api:
        return {
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }
    return {
        "input_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
    }


def _estimate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    model: str,
) -> float:
    pricing = {
        "gpt-4.1-mini": (0.0004, 0.0016),
        "gpt-4.1-nano": (0.0001, 0.0004),
    }
    base = model.split("/")[-1] if "/" in model else model
    input_price, output_price = pricing.get(base, (0.001, 0.002))
    return (prompt_tokens / 1000 * input_price) + (completion_tokens / 1000 * output_price)


def _get_cost_quality(model: str) -> str:
    known_models = {"gpt-4.1-mini", "gpt-4.1-nano"}
    base = model.split("/")[-1] if "/" in model else model
    return "known_pricing" if base in known_models else "unknown_pricing_fallback"


def call_openai(
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float | None = None,
) -> tuple[str | None, float | None, float | None, str | None, str | None, int | None, int | None]:
    api_key = get_openai_api_key()
    if not api_key:
        return None, None, None, None, "No API key found. Set OPENAI_API_KEY.", None, None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    use_responses_api = _is_gpt5_model(model)

    if use_responses_api:
        payload: dict[str, Any] = {
            "model": model,
            "input": user_prompt,
            "instructions": system_prompt,
            "max_output_tokens": max_tokens,
        }
        endpoint = f"{OPENAI_BASE_URL}/responses"
    else:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_tokens,
        }
        if temperature is not None:
            payload["temperature"] = temperature
        endpoint = f"{OPENAI_BASE_URL}/chat/completions"

    try:
        import ssl
        import urllib.error
        import urllib.request

        data = json.dumps(payload).encode("utf-8")
        ctx = ssl.create_default_context()
        req = urllib.request.Request(endpoint, data=data, headers=headers, method="POST")
        start = time.time()
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            latency = (time.time() - start) * 1000
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        latency = (time.time() - start) * 1000
        body_bytes: bytes | None = None
        try:
            body_bytes = exc.read()
        except Exception:
            pass
        body_text = body_bytes.decode("utf-8", errors="replace") if body_bytes else None
        error_msg = _build_redacted_error_message(exc.code, str(exc.reason), body_text)
        return None, latency, None, None, error_msg, None, None
    except Exception as exc:
        latency = (time.time() - start) * 1000
        return None, latency, None, None, f"API call failed (no body): {_redact_secrets(str(exc))}", None, None

    if use_responses_api:
        content = _extract_content_from_responses(body)
        if content is None:
            status = body.get("status", "unknown")
            error_info = body.get("error", {})
            error_detail = json.dumps(error_info) if error_info else f"status={status}"
            redacted = _redact_secrets(error_detail)
            return None, latency, None, body.get("model"), f"Responses API: no output_text ({redacted})", None, None
    else:
        content = _extract_content_from_chat(body)
        if content is None:
            return None, latency, None, body.get("model"), "No choices in chat completion response", None, None

    usage = _extract_usage(body, use_responses_api)
    input_tokens = usage["input_tokens"]
    output_tokens = usage["output_tokens"]
    cost = _estimate_cost(input_tokens, output_tokens, model)

    return content, latency, cost, body.get("model"), None, input_tokens, output_tokens


def estimate_openai_cost(prompt_tokens: int, completion_tokens: int, model: str) -> tuple[float, str]:
    cost = _estimate_cost(prompt_tokens, completion_tokens, model)
    return cost, _get_cost_quality(model)
