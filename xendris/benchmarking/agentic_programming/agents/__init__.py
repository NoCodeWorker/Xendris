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
    }
    if error:
        return "", error, metadata

    result = parse_patch_response(response) if response else None
    if result:
        _validate_fix_boundaries(result, allowed_files or [], forbidden_files or [])
        return json.dumps(result), None, metadata

    return response or "", None, metadata


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
