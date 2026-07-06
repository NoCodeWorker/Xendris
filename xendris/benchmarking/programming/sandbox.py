"""Controlled Python execution helpers for programming benchmark tests.

This sandbox is deliberately narrow. It is intended for benchmark-owned test
snippets, not for executing arbitrary untrusted programs from real users.
"""

from __future__ import annotations

import ast
import multiprocessing as mp
import re
from typing import Any


FORBIDDEN_CODE_MARKERS = (
    "eval(",
    "exec(",
    "__import__",
    "import os",
    "import sys",
    "import socket",
    "import subprocess",
    "import pathlib",
    "import shutil",
    "import requests",
    "import urllib",
    "open(",
    "globals(",
    "locals(",
    "compile(",
    "input(",
)


SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "float": float,
    "int": int,
    "isinstance": isinstance,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "range": range,
    "round": round,
    "set": set,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}


def extract_python_code(answer: str) -> str | None:
    """Extract the first fenced Python code block or return raw answer-like code."""
    fenced = re.search(r"```(?:python|py)?\s*(.*?)```", answer, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()
    stripped = answer.strip()
    if stripped.startswith("def ") or "\ndef " in stripped:
        return stripped
    return None


def has_security_risk(code: str | None) -> bool:
    """Detect simple unsafe constructs before execution."""
    if not code:
        return False
    lowered = code.lower()
    return any(marker in lowered for marker in FORBIDDEN_CODE_MARKERS)


def public_function_signatures(code: str | None) -> dict[str, tuple[str, ...]]:
    """Extract public function names and positional argument names."""
    if not code:
        return {}
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {}
    signatures: dict[str, tuple[str, ...]] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            signatures[node.name] = tuple(arg.arg for arg in node.args.args)
    return signatures


def contract_preserved(starter_code: str | None, extracted_code: str | None) -> bool:
    """Verify that public function signatures from starter code remain present."""
    expected = public_function_signatures(starter_code)
    if not expected:
        return True
    actual = public_function_signatures(extracted_code)
    return all(actual.get(name) == signature for name, signature in expected.items())


def run_python_tests(
    code: str | None,
    test_code: str | None,
    timeout_seconds: float = 2.0,
) -> tuple[bool, str | None]:
    """Run benchmark-owned test code in a short-lived process with limited builtins."""
    if not code:
        return False, "NO_CODE_EXTRACTED"
    if has_security_risk(code):
        return False, "SECURITY_RISK"
    if not test_code:
        return True, None

    queue: mp.Queue[tuple[bool, str | None]] = mp.Queue()
    process = mp.Process(target=_execute_payload, args=(code, test_code, queue))
    process.start()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join()
        return False, "TIMEOUT"
    if queue.empty():
        return False, "NO_RESULT"
    return queue.get()


def _execute_payload(code: str, test_code: str, queue: mp.Queue) -> None:
    namespace: dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
    try:
        exec(code, namespace, namespace)
        exec(test_code, namespace, namespace)
    except Exception as exc:  # noqa: BLE001 - benchmark captures controlled failures.
        queue.put((False, f"{exc.__class__.__name__}: {exc}"))
        return
    queue.put((True, None))
