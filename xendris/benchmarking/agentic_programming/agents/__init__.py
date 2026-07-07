from __future__ import annotations

import json
import os
import time
from typing import Any


def base_agent(**kwargs) -> tuple[str, str | None]:
    return "def solve():\n    pass\n", None


def xendris_agent(**kwargs) -> tuple[str, str | None]:
    return "def solve():\n    return 42\n", None


def xendris_calibrated_agent(**kwargs) -> tuple[str, str | None]:
    return "def solve():\n    return 42\n", None


def deepseek_base_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    model: str | None = None,
    **kwargs,
) -> tuple[str, str | None, dict]:
    from xendris.benchmarking.agentic_programming.agents.deepseek_provider import (
        build_fix_prompt,
        call_deepseek,
        parse_patch_response,
    )

    if not repo_path or not issue_description:
        return "", "deepseek_base_agent requires repo_path and issue_description", {}

    source_files = _read_source_files(repo_path, allowed_files or [])
    system, user = build_fix_prompt(
        issue_description=issue_description,
        source_files=source_files,
        allowed_files=allowed_files or [],
        forbidden_files=forbidden_files or [],
        xendris_mode=False,
    )

    response, latency, cost, provider_reported_model, error = call_deepseek(
        system,
        user,
        model=model or "deepseek-v4-flash",
    )
    metadata = {
        "latency_ms": latency,
        "cost_estimate": cost,
        "provider_reported_model": provider_reported_model,
        "cost_estimate_quality": "known_pricing" if (model or "deepseek-v4-flash") == "deepseek-v4-flash" else "unknown_pricing_fallback",
    }
    if error:
        return "", error, metadata

    result = parse_patch_response(response) if response else None
    if result:
        return json.dumps(result), None, metadata

    return response or "", None, metadata


def deepseek_xendris_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    model: str | None = None,
    **kwargs,
) -> tuple[str, str | None, dict]:
    from xendris.benchmarking.agentic_programming.agents.deepseek_provider import (
        build_fix_prompt,
        call_deepseek,
        parse_patch_response,
    )

    if not repo_path or not issue_description:
        return "", "deepseek_xendris_agent requires repo_path and issue_description", {}

    source_files = _read_source_files(repo_path, allowed_files or [])
    system, user = build_fix_prompt(
        issue_description=issue_description,
        source_files=source_files,
        allowed_files=allowed_files or [],
        forbidden_files=forbidden_files or [],
        xendris_mode=True,
    )

    response, latency, cost, provider_reported_model, error = call_deepseek(
        system,
        user,
        model=model or "deepseek-v4-flash",
    )
    metadata = {
        "latency_ms": latency,
        "cost_estimate": cost,
        "provider_reported_model": provider_reported_model,
        "cost_estimate_quality": "known_pricing" if (model or "deepseek-v4-flash") == "deepseek-v4-flash" else "unknown_pricing_fallback",
    }
    if error:
        return "", error, metadata

    result = parse_patch_response(response) if response else None
    if result:
        _validate_fix_boundaries(result, allowed_files or [], forbidden_files or [])
        return json.dumps(result), None, metadata

    return response or "", None, metadata


def deepseek_xendris_calibrated_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    model: str | None = None,
    **kwargs,
) -> tuple[str, str | None, dict]:
    from xendris.benchmarking.agentic_programming.agents.deepseek_provider import (
        build_fix_prompt,
        call_deepseek,
        parse_patch_response,
    )

    if not repo_path or not issue_description:
        return "", "deepseek_xendris_calibrated_agent requires repo_path and issue_description", {}

    source_files = _read_source_files(repo_path, allowed_files or [])
    system, user = build_fix_prompt(
        issue_description=issue_description,
        source_files=source_files,
        allowed_files=allowed_files or [],
        forbidden_files=forbidden_files or [],
        xendris_mode=True,
    )

    response, latency, cost, provider_reported_model, error = call_deepseek(
        system,
        user,
        model=model or "deepseek-v4-flash",
    )
    metadata = {
        "latency_ms": latency,
        "cost_estimate": cost,
        "provider_reported_model": provider_reported_model,
        "cost_estimate_quality": "known_pricing" if (model or "deepseek-v4-flash") == "deepseek-v4-flash" else "unknown_pricing_fallback",
    }
    if error:
        return "", error, metadata

    result = parse_patch_response(response) if response else None
    if result:
        _validate_fix_boundaries(result, allowed_files or [], forbidden_files or [])
        return json.dumps(result), None, metadata

    return response or "", None, metadata


def openai_base_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    model: str | None = None,
    **kwargs,
) -> tuple[str, str | None, dict]:
    from xendris.benchmarking.agentic_programming.agents.openai_provider import (
        call_openai,
    )
    from xendris.benchmarking.agentic_programming.agents.deepseek_provider import (
        build_fix_prompt,
        parse_patch_response,
    )

    if not repo_path or not issue_description:
        return "", "openai_base_agent requires repo_path and issue_description", {}

    source_files = _read_source_files(repo_path, allowed_files or [])
    system, user = build_fix_prompt(
        issue_description=issue_description,
        source_files=source_files,
        allowed_files=allowed_files or [],
        forbidden_files=forbidden_files or [],
        xendris_mode=False,
    )

    response, latency, cost, provider_reported_model, error, input_tokens, output_tokens = call_openai(
        system,
        user,
        model=model or "gpt-4.1-mini",
    )
    total = (input_tokens or 0) + (output_tokens or 0) if (input_tokens is not None and output_tokens is not None) else None
    metadata = {
        "latency_ms": latency,
        "cost_estimate": cost,
        "provider_reported_model": provider_reported_model,
        "cost_estimate_quality": "known_pricing" if (model or "gpt-4.1-mini") in {"gpt-4.1-mini", "gpt-4.1-nano"} else "unknown_pricing_fallback",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total,
    }
    if error:
        return "", error, metadata

    result = parse_patch_response(response) if response else None
    if result:
        return json.dumps(result), None, metadata

    return response or "", None, metadata


def openai_xendris_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    model: str | None = None,
    **kwargs,
) -> tuple[str, str | None, dict]:
    from xendris.benchmarking.agentic_programming.agents.openai_provider import (
        call_openai,
    )
    from xendris.benchmarking.agentic_programming.agents.deepseek_provider import (
        build_fix_prompt,
        parse_patch_response,
    )

    if not repo_path or not issue_description:
        return "", "openai_xendris_agent requires repo_path and issue_description", {}

    source_files = _read_source_files(repo_path, allowed_files or [])
    system, user = build_fix_prompt(
        issue_description=issue_description,
        source_files=source_files,
        allowed_files=allowed_files or [],
        forbidden_files=forbidden_files or [],
        xendris_mode=True,
    )

    response, latency, cost, provider_reported_model, error, input_tokens, output_tokens = call_openai(
        system,
        user,
        model=model or "gpt-4.1-mini",
    )
    total = (input_tokens or 0) + (output_tokens or 0) if (input_tokens is not None and output_tokens is not None) else None
    metadata = {
        "latency_ms": latency,
        "cost_estimate": cost,
        "provider_reported_model": provider_reported_model,
        "cost_estimate_quality": "known_pricing" if (model or "gpt-4.1-mini") in {"gpt-4.1-mini", "gpt-4.1-nano"} else "unknown_pricing_fallback",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total,
    }
    if error:
        return "", error, metadata

    result = parse_patch_response(response) if response else None
    if result:
        _validate_fix_boundaries(result, allowed_files or [], forbidden_files or [])
        return json.dumps(result), None, metadata

    return response or "", None, metadata


def openai_xendris_calibrated_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    model: str | None = None,
    **kwargs,
) -> tuple[str, str | None, dict]:
    from xendris.benchmarking.agentic_programming.agents.openai_provider import (
        call_openai,
    )
    from xendris.benchmarking.agentic_programming.agents.deepseek_provider import (
        build_fix_prompt,
        parse_patch_response,
    )

    if not repo_path or not issue_description:
        return "", "openai_xendris_calibrated_agent requires repo_path and issue_description", {}

    source_files = _read_source_files(repo_path, allowed_files or [])
    system, user = build_fix_prompt(
        issue_description=issue_description,
        source_files=source_files,
        allowed_files=allowed_files or [],
        forbidden_files=forbidden_files or [],
        xendris_mode=True,
    )

    response, latency, cost, provider_reported_model, error, input_tokens, output_tokens = call_openai(
        system,
        user,
        model=model or "gpt-4.1-mini",
    )
    total = (input_tokens or 0) + (output_tokens or 0) if (input_tokens is not None and output_tokens is not None) else None
    metadata = {
        "latency_ms": latency,
        "cost_estimate": cost,
        "provider_reported_model": provider_reported_model,
        "cost_estimate_quality": "known_pricing" if (model or "gpt-4.1-mini") in {"gpt-4.1-mini", "gpt-4.1-nano"} else "unknown_pricing_fallback",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total,
    }
    if error:
        return "", error, metadata

    result = parse_patch_response(response) if response else None
    if result:
        _validate_fix_boundaries(result, allowed_files or [], forbidden_files or [])
        return json.dumps(result), None, metadata

    return response or "", None, metadata


def fake_openai_base_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    model: str | None = None,
    **kwargs,
) -> tuple[str, str | None, dict]:
    if not repo_path or not issue_description:
        return "", "fake_openai_base_agent requires repo_path and issue_description", {}
    patch = _generate_fake_patch(allowed_files or [])
    metadata = {
        "latency_ms": 1234.56,
        "cost_estimate": 0.00523,
        "provider_reported_model": model or "gpt-4.1-mini",
        "cost_estimate_quality": "known_pricing",
    }
    return patch, None, metadata


def fake_deepseek_base_agent(
    repo_path: str | None = None,
    issue_description: str | None = None,
    allowed_files: list[str] | None = None,
    forbidden_files: list[str] | None = None,
    max_iterations: int | None = None,
    model: str | None = None,
    **kwargs,
) -> tuple[str, str | None, dict]:
    if not repo_path or not issue_description:
        return "", "fake_deepseek_base_agent requires repo_path and issue_description", {}
    patch = _generate_fake_patch(allowed_files or [])
    metadata = {
        "latency_ms": 567.89,
        "cost_estimate": 0.00231,
        "provider_reported_model": model or "deepseek-v4-flash",
        "cost_estimate_quality": "known_pricing",
    }
    return patch, None, metadata


def _generate_fake_patch(allowed_files: list[str]) -> str:
    if not allowed_files:
        return '{"_agent_patch.py": "def solve():\n    return 42\n"}'
    target = allowed_files[0]
    return json.dumps({target: _get_fake_content_for_file(target)})


def _get_fake_content_for_file(filepath: str) -> str:
    basename = os.path.splitext(os.path.basename(filepath))[0]
    # Return a reasonable-looking patch that is NOT a known dummy template
    return (
        f'def {basename}_helper(value):\n'
        f'    """Patch generated by fake provider for testing."""\n'
        f'    return value * 2\n'
    )


def _read_source_files(repo_path: str, allowed_files: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for rel_path in allowed_files:
        full_path = os.path.join(repo_path, rel_path)
        if os.path.isfile(full_path):
            with open(full_path, encoding="utf-8") as f:
                result[rel_path] = f.read()
    return result


def _validate_fix_boundaries(
    fix: dict[str, str],
    allowed_files: list[str],
    forbidden_files: list[str],
) -> None:
    for path in list(fix.keys()):
        if path not in allowed_files:
            del fix[path]
            continue
        for forbidden in forbidden_files:
            if forbidden.rstrip("/") in path:
                del fix[path]
                break
