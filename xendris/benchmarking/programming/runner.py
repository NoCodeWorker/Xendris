"""Runner and dataset loader for Programming Reliability Benchmark v0.1."""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import inspect
import json
from pathlib import Path
import time
from typing import Any, Callable, Mapping, Sequence

from .sandbox import (
    contract_preserved,
    extract_python_code,
    has_security_risk,
    run_python_tests,
)
from .scoring import score_programming_result
from .types import ProgrammingBenchmarkSummary, ProgrammingRunResult, ProgrammingSample


EXPECTED_DISTRIBUTION = {
    "bug_fixing": 20,
    "unit_tests": 15,
    "refactor_safety": 15,
    "edge_cases": 15,
    "security_basics": 10,
    "performance": 10,
    "api_contracts": 10,
    "normal_control": 5,
}


def load_programming_reliability_v0_1() -> list[ProgrammingSample]:
    """Load and validate Programming Reliability Dataset v0.1."""
    path = _dataset_path()
    if not path.exists():
        _write_default_dataset(path)
    samples = _load_samples_jsonl(path)
    _validate_dataset(samples)
    return samples


def run_programming_benchmark(
    samples: Sequence[ProgrammingSample],
    model_callable: Callable[..., Mapping[str, Any]],
    config: Mapping[str, Any] | None = None,
) -> list[ProgrammingRunResult]:
    """Run programming samples against an injected model callable."""
    config = config or {}
    timeout = float(config.get("timeout_seconds", 2.0))
    system_name = str(config.get("system_name", "model"))
    results: list[ProgrammingRunResult] = []

    for sample in samples:
        started = time.perf_counter()
        try:
            raw = _call_model(model_callable, sample, config)
        except Exception as exc:  # noqa: BLE001 - benchmark isolates callable failures.
            raw = {
                "answer": "",
                "decision": "EXCLUDE",
                "reason": "CALLABLE_ERROR",
                "runtime_error": str(exc),
                "estimated_cost_usd": 0.0,
            }
        latency_ms = float(raw.get("latency_ms") or ((time.perf_counter() - started) * 1000.0))
        result = _build_result(sample, raw, system_name, timeout, latency_ms)
        results.append(result)
    return results


def summarize_programming_results(
    results: Sequence[ProgrammingRunResult],
) -> ProgrammingBenchmarkSummary:
    """Summarize programming benchmark results."""
    total = len(results)
    if total == 0:
        return ProgrammingBenchmarkSummary(
            total_samples=0,
            average_score=0.0,
            tests_passed_count=0,
            contract_preserved_count=0,
            runtime_error_count=0,
            security_risk_count=0,
            exclusion_rate=0.0,
            production_overclaim_rate=0.0,
            cost_per_correct_solution=None,
            score_by_category={},
        )

    by_category: dict[str, list[ProgrammingRunResult]] = defaultdict(list)
    for result in results:
        by_category[_category_from_sample_id(result.sample_id)].append(result)

    correct = [result for result in results if result.score >= 1.0]
    total_cost = sum(result.estimated_cost_usd for result in results)
    return ProgrammingBenchmarkSummary(
        total_samples=total,
        average_score=round(sum(result.score for result in results) / total, 4),
        tests_passed_count=sum(result.tests_passed for result in results),
        contract_preserved_count=sum(result.contract_preserved for result in results),
        runtime_error_count=sum(result.runtime_error is not None for result in results),
        security_risk_count=sum(result.security_risk for result in results),
        exclusion_rate=round(
            sum(result.decision == "EXCLUDE" for result in results) / total,
            4,
        ),
        production_overclaim_rate=round(
            sum(result.reason == "PRODUCTION_OVERCLAIM" for result in results) / total,
            4,
        ),
        cost_per_correct_solution=round(total_cost / len(correct), 8) if correct else None,
        score_by_category={
            category: round(sum(result.score for result in items) / len(items), 4)
            for category, items in sorted(by_category.items())
        },
    )


def _build_result(
    sample: ProgrammingSample,
    raw: Mapping[str, Any],
    default_system_name: str,
    timeout: float,
    latency_ms: float,
) -> ProgrammingRunResult:
    answer = str(raw.get("answer", ""))
    extracted_code = raw.get("extracted_code") or extract_python_code(answer)
    security_risk = bool(raw.get("security_risk")) or has_security_risk(extracted_code)
    preserved = contract_preserved(sample.starter_code, extracted_code)
    tests_passed = False
    runtime_error = _optional_string(raw.get("runtime_error"))
    if not security_risk and preserved:
        tests_passed, runtime_error = run_python_tests(extracted_code, sample.test_code, timeout)

    performance_regression = bool(raw.get("performance_regression"))
    reason = _derive_reason(sample, raw, tests_passed, preserved, runtime_error, security_risk)
    decision = "INCLUDE" if tests_passed and preserved and not security_risk else "EXCLUDE"
    if reason == "PRODUCTION_OVERCLAIM":
        decision = "EXCLUDE"

    provisional = ProgrammingRunResult(
        sample_id=sample.sample_id,
        system_name=str(raw.get("system_name", default_system_name)),
        language=sample.language,
        answer=answer,
        extracted_code=extracted_code,
        tests_passed=tests_passed,
        contract_preserved=preserved,
        runtime_error=runtime_error,
        security_risk=security_risk,
        performance_regression=performance_regression,
        decision=decision,
        reason=reason,
        score=0.0,
        latency_ms=round(latency_ms, 4),
        estimated_cost_usd=float(raw.get("estimated_cost_usd", 0.0) or 0.0),
        fingerprint="",
    )
    score = score_programming_result(provisional, sample)
    fingerprint = _fingerprint(provisional, score)
    return ProgrammingRunResult(**{**provisional.to_dict(), "score": score, "fingerprint": fingerprint})


def _derive_reason(
    sample: ProgrammingSample,
    raw: Mapping[str, Any],
    tests_passed: bool,
    preserved: bool,
    runtime_error: str | None,
    security_risk: bool,
) -> str | None:
    raw_reason = _optional_string(raw.get("reason"))
    if security_risk:
        return "SECURITY_RISK"
    if not preserved:
        return "CONTRACT_BROKEN"
    if "production" in sample.prompt.lower() and "ready" in raw.get("answer", "").lower():
        return "PRODUCTION_OVERCLAIM"
    if runtime_error:
        return raw_reason or "RUNTIME_ERROR"
    if tests_passed:
        return raw_reason or "PASS"
    return raw_reason or "TESTS_FAILED"


def _fingerprint(result: ProgrammingRunResult, score: float) -> str:
    payload = {
        "answer": result.answer,
        "decision": result.decision,
        "extracted_code": result.extracted_code,
        "reason": result.reason,
        "sample_id": result.sample_id,
        "score": score,
        "system_name": result.system_name,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]


def _call_model(
    model_callable: Callable[..., Mapping[str, Any]],
    sample: ProgrammingSample,
    config: Mapping[str, Any],
) -> Mapping[str, Any]:
    parameters = inspect.signature(model_callable).parameters
    if len(parameters) >= 2:
        return model_callable(sample, config)
    return model_callable(sample)


def _load_samples_jsonl(path: Path) -> list[ProgrammingSample]:
    samples = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            item = json.loads(line)
            samples.append(
                ProgrammingSample(
                    sample_id=item["sample_id"],
                    category=item["category"],
                    language=item["language"],
                    prompt=item["prompt"],
                    starter_code=item.get("starter_code"),
                    test_code=item.get("test_code"),
                    expected_behavior=item["expected_behavior"],
                    expected_decision=item["expected_decision"],
                    expected_reason=item.get("expected_reason"),
                    forbidden_changes=tuple(item.get("forbidden_changes") or ()),
                    metadata=item.get("metadata") or {},
                )
            )
    return samples


def _validate_dataset(samples: Sequence[ProgrammingSample]) -> None:
    if len(samples) != 100:
        raise ValueError("Programming Reliability v0.1 must contain exactly 100 samples")
    ids = [sample.sample_id for sample in samples]
    if len(ids) != len(set(ids)):
        raise ValueError("Programming Reliability v0.1 sample_id values must be unique")
    distribution = Counter(sample.category for sample in samples)
    if dict(distribution) != EXPECTED_DISTRIBUTION:
        raise ValueError(f"Unexpected Programming Reliability v0.1 distribution: {dict(distribution)}")


def _dataset_path() -> Path:
    return Path(__file__).resolve().parents[1] / "datasets" / "programming_reliability_v0_1.jsonl"


def _write_default_dataset(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for item in _default_dataset_items():
            handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def _default_dataset_items() -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    category_templates = {
        "bug_fixing": (20, "Fix the bug while preserving the public function contract."),
        "unit_tests": (15, "Write useful tests that cover edge cases, not only happy paths."),
        "refactor_safety": (15, "Refactor for readability without changing behavior or public names."),
        "edge_cases": (15, "Handle empty strings, Unicode, negatives, duplicates, and nested inputs."),
        "security_basics": (10, "Avoid unsafe eval, path abuse, secrets exposure, and injection."),
        "performance": (10, "Improve obvious O(n^2) behavior without unmeasured production claims."),
        "api_contracts": (10, "Preserve JSON fields, error shape, types, and public names."),
        "normal_control": (5, "Solve the simple task directly."),
    }
    for category, (count, prompt) in category_templates.items():
        for index in range(1, count + 1):
            sample_id = f"PR-{category.upper().replace('_', '-')}-{index:03d}"
            items.append(_sample_item(sample_id, category, prompt, index))
    return items


def _sample_item(sample_id: str, category: str, prompt: str, index: int) -> dict[str, object]:
    function_name = f"solve_{sample_id.lower().replace('-', '_')}"
    starter_code = f"def {function_name}(value):\n    return value\n"
    test_code = f"assert {function_name}(2) == 2\n"
    if category == "bug_fixing":
        starter_code = f"def {function_name}(items):\n    return items[0]\n"
        test_code = f"assert {function_name}([1, 2]) == 1\nassert {function_name}([]) is None\n"
    elif category == "security_basics":
        starter_code = f"def {function_name}(expr):\n    return eval(expr)\n"
        test_code = f"assert {function_name}('abc') == 'abc'\n"
    elif category == "performance":
        starter_code = f"def {function_name}(items):\n    return len(set(items))\n"
        test_code = f"assert {function_name}([1, 1, 2]) == 2\n"
    elif category == "api_contracts":
        starter_code = f"def {function_name}(payload):\n    return {{'ok': True, 'data': payload}}\n"
        test_code = f"assert {function_name}('x') == {{'ok': True, 'data': 'x'}}\n"
    return {
        "sample_id": sample_id,
        "category": category,
        "language": "python",
        "prompt": f"{prompt} Case {index}.",
        "starter_code": starter_code,
        "test_code": test_code,
        "expected_behavior": "Return the expected value while preserving the public contract.",
        "expected_decision": "INCLUDE",
        "expected_reason": "PASS",
        "forbidden_changes": ["public_function_name", "public_signature"],
        "metadata": {"dataset": "programming_reliability_v0_1", "case_index": index},
    }


def _category_from_sample_id(sample_id: str) -> str:
    normalized = sample_id.lower()
    for category in EXPECTED_DISTRIBUTION:
        if category.replace("_", "-") in normalized:
            return category
    return "unknown"


def _optional_string(value: object) -> str | None:
    return str(value) if value is not None else None
