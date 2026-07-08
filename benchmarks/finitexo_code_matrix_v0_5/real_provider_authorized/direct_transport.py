"""Direct provider transport for v0.5.4.

This module uses only process-environment keys supplied through config. It does
not read .env files and does not print or serialize secrets.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from .authorized_config import AuthorizedDiagnosticConfig, AuthorizedProviderSpec


def _task_prompt(task: dict) -> str:
    return (
        "You are participating in a diagnostic-only programming benchmark smoke run. "
        "Return a concise answer, preserve the requested API contract, and do not claim production readiness.\n\n"
        f"Task id: {task.get('task_id')}\n"
        f"Prompt:\n{task.get('prompt', '')}"
    )


def direct_provider_adapter(provider: AuthorizedProviderSpec, task: dict, config: AuthorizedDiagnosticConfig):
    from .authorized_runner import AuthorizedProviderResult

    api_key = config.environ.get(provider.required_env_var)
    if not api_key:
        raise RuntimeError(f"missing API key for provider {provider.provider_name}")
    if not provider.endpoint_url:
        raise RuntimeError(f"missing endpoint for provider {provider.provider_name}")

    payload = {
        "model": provider.model_name,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "messages": [
            {"role": "system", "content": "You are a diagnostic benchmark participant. Do not overclaim."},
            {"role": "user", "content": _task_prompt(task)},
        ],
    }
    request = urllib.request.Request(
        provider.endpoint_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.request_timeout_seconds) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:300]
        raise RuntimeError(f"provider HTTP error {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"provider network error: {type(exc.reason).__name__}") from exc

    choices = response_data.get("choices") or []
    if not choices:
        raise RuntimeError("provider response contains no choices")
    message = choices[0].get("message", {})
    text = message.get("content") or ""
    usage = response_data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens")
    completion_tokens = usage.get("completion_tokens")
    total_tokens = usage.get("total_tokens")
    return AuthorizedProviderResult(
        raw_response_text=text,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        estimated_cost_usd=provider.estimated_cost_per_task_usd,
        provider_reported_model=response_data.get("model") or provider.model_name,
    )
