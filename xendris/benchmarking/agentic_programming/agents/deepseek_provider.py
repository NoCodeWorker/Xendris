from __future__ import annotations

import json
import os
import time
from typing import Any

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_MAX_TOKENS = 4096


def get_deepseek_api_key() -> str | None:
    return os.environ.get("DEEPSEEK_API_KEY")


def get_transport() -> str:
    if os.environ.get("DEEPSEEK_API_KEY"):
        return "direct"
    return "unknown"


def call_deepseek(
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = 0.2,
) -> tuple[str | None, float | None, float | None, str | None, str | None]:
    api_key = get_deepseek_api_key()
    if not api_key:
        return None, None, None, None, "No API key found. Set DEEPSEEK_API_KEY."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        import urllib.request
        import ssl

        data = json.dumps(payload).encode("utf-8")
        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            data=data,
            headers=headers,
            method="POST",
        )
        start = time.time()
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            latency = (time.time() - start) * 1000
            body = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        return None, None, None, None, f"API call failed: {exc}"

    choices = body.get("choices", [])
    if not choices:
        return None, None, None, body.get("model"), "No choices in API response"

    content = choices[0].get("message", {}).get("content", "")
    usage = body.get("usage", {})

    cost = _estimate_cost(
        prompt_tokens=usage.get("prompt_tokens", 0),
        completion_tokens=usage.get("completion_tokens", 0),
        model=model,
    )

    return content, latency, cost, body.get("model"), None


def _estimate_cost(prompt_tokens: int, completion_tokens: int, model: str) -> float:
    pricing = {
        "deepseek-v4-flash": (0.0005, 0.0005),
    }
    base = model.split("/")[-1] if "/" in model else model
    input_price, output_price = pricing.get(base, (0.001, 0.001))
    return (prompt_tokens / 1000 * input_price) + (completion_tokens / 1000 * output_price)


def estimate_deepseek_cost(prompt_tokens: int, completion_tokens: int, model: str) -> tuple[float, str]:
    pricing = {
        "deepseek-v4-flash": (0.0005, 0.0005),
    }
    base = model.split("/")[-1] if "/" in model else model
    quality = "known_pricing" if base in pricing else "unknown_pricing_fallback"
    return _estimate_cost(prompt_tokens, completion_tokens, model), quality


def build_fix_prompt(
    issue_description: str,
    source_files: dict[str, str],
    allowed_files: list[str],
    forbidden_files: list[str],
    test_command: str | None = None,
    xendris_mode: bool = False,
) -> tuple[str, str]:
    file_list = "\n".join(f"### {path}\n```python\n{content}\n```" for path, content in source_files.items())

    system = "You are a Python coding agent. Fix the bug in the source code below."

    if xendris_mode:
        system += (
            "\n\nRULES:"
            "\n1. Only modify files listed in allowed files."
            "\n2. Do NOT touch any file in forbidden directories."
            "\n3. Do NOT add new imports of pytest, os, subprocess, or eval."
            "\n4. Preserve all existing function signatures (names and parameters)."
            "\n5. Return ONLY the updated file contents as a JSON dict mapping filename to new content."
            "\n6. Do NOT claim success unless you have verified the fix matches the issue description."
        )

    user = f"Issue: {issue_description}\n\nAllowed files: {allowed_files}\nForbidden files: {forbidden_files}\n\nSource files:\n{file_list}"

    if test_command:
        user += f"\n\nTest command: {test_command}"

    if xendris_mode:
        user += "\n\nReturn ONLY a JSON object with keys being file paths (relative to repo root) and values being the updated file contents."

    return system, user


def parse_patch_response(response: str) -> dict[str, str] | None:
    import re

    json_match = re.search(r"\{[^{}]*\}", response, re.DOTALL)
    if json_match:
        try:
            parsed = json.loads(json_match.group())
            if isinstance(parsed, dict) and all(isinstance(v, str) for v in parsed.values()):
                return parsed
        except json.JSONDecodeError:
            pass

    file_blocks: dict[str, str] = {}
    pattern = re.compile(r'###\s*(.+?)\n```(?:python)?\n(.*?)```', re.DOTALL)
    for match in pattern.finditer(response):
        path = match.group(1).strip()
        content = match.group(2).strip()
        if path and content:
            file_blocks[path] = content

    return file_blocks if file_blocks else None
