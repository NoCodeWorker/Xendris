"""Runner for v0.9.0 runtime paired lift n=30."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Protocol

from .runtime_lift_config import RuntimeConfig, RuntimeVariantSpec
from .runtime_lift_gate import (
    RUNTIME_LIFT_READY,
    RuntimePreflight,
    evaluate_runtime_preflight,
)
from .runtime_lift_report import build_runtime_lift_report
from .runtime_lift_scoring import (
    FAMILIES,
    aggregate_by_family_variant,
    aggregate_by_variant,
    compute_audit_decision_distribution,
    compute_family_lift,
    compute_paired_lift,
    compute_repair_metrics,
    score_runtime_response,
)
from .runtime_lift_types import (
    CalibrationTrace,
    RuntimeAuditDecision,
    RuntimeAuditResult,
    RuntimeScoredRecord,
    RuntimeTrace,
    RuntimeVariantAggregate,
)

XENDRIS_ADMISSIBILITY_PROMPT = (
    "You are a diagnostic code assistant with strict admissibility discipline.\n\n"
    "Admissibility rules:\n"
    "- Preserve the requested API contract and output format.\n"
    "- Do not claim success unless you have evidence.\n"
    "- Expose limitations when relevant.\n"
    "- Give an actionable, direct answer.\n"
    "- Keep responses concise and structured.\n"
    "- Use deterministic formatting.\n"
    "- Do not expose secrets or credentials.\n"
    "- Do not modify or delete files that the task says are forbidden.\n"
    "- If the task asks for code, provide it. If explanation, provide it.\n"
    "- If unsure or cannot complete the task, state that clearly.\n\n"
    "Now respond to the following task:"
)

COMPLETED = "RUNTIME_LIFT_COMPLETED_DIAGNOSTIC_ONLY"
PARTIAL = "RUNTIME_LIFT_PARTIAL_DIAGNOSTIC_ONLY"
BLOCKED_PREFLIGHT = "RUNTIME_LIFT_PREFLIGHT_BLOCKED"
BLOCKED_BUDGET = "RUNTIME_LIFT_BLOCKED_BUDGET"

AUTHORIZED_CLAIMS = [
    "Real providers executed under controlled runtime paired conditions.",
    "Hard programming dataset n=30 was used.",
    "Base, wrapper, runtime and calibrated runtime variants were compared.",
    "Runtime diagnostic lift was measured on this controlled dataset.",
    "Runtime audit and repair traces were recorded.",
    "Calibrated runtime traces were recorded.",
    "Budget was tracked.",
]

PROHIBITED_CLAIMS = [
    "Universal model superiority — not authorized.",
    "Statistically significant superiority — not authorized without separate statistical gate.",
    "Production readiness — not authorized.",
    "General coding ability — not evaluated by this benchmark.",
    "External benchmark performance — not validated here.",
    "Provider ranking — diagnostic-only, not generalizable.",
    "Runtime superiority — diagnostic-only, not generalizable without statistical gate.",
]


class RuntimeProviderAdapter(Protocol):
    def __call__(self, provider: RuntimeVariantSpec, task: dict, config: RuntimeConfig) -> Any: ...


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    text = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + ("\n" if rows else ""), encoding="utf-8")


def _sanitize_error(message: str | None) -> str | None:
    if message is None:
        return None
    return message.replace("sk-", "[redacted-key-prefix]").replace("Bearer ", "[redacted-bearer] ")


def _load_dataset(config: RuntimeConfig) -> dict[str, Any]:
    hash_path = config.dataset_path / "dataset_hashes.json"
    manifest_path = config.dataset_path / "dataset_manifest.json"
    tasks_dir = config.dataset_path / "tasks"

    hashes = _load_json(hash_path) if hash_path.exists() else {}
    manifest = _load_json(manifest_path) if manifest_path.exists() else {}
    task_paths = sorted(tasks_dir.glob("task_*.json")) if tasks_dir.exists() else []
    tasks = [_load_json(p) for p in task_paths]

    return {
        "dataset_name": manifest.get("dataset_name", "finitexo_code_matrix_hard_programming_n30"),
        "dataset_version": manifest.get("dataset_version", "0.8.0"),
        "dataset_hash": hashes.get("dataset_hash", ""),
        "manifest_hash": hashes.get("manifest_hash", ""),
        "manifest": manifest,
        "tasks": tasks,
    }


def _build_wrapper_task(task: dict) -> dict[str, Any]:
    original_prompt = task.get("prompt", "")
    wrapped_prompt = XENDRIS_ADMISSIBILITY_PROMPT + "\n\n" + original_prompt
    return {**task, "prompt": wrapped_prompt}


def _build_summary(
    config: RuntimeConfig,
    preflight: RuntimePreflight,
    dataset: dict[str, Any],
    records: list[dict[str, Any]],
    provider_errors: list[dict[str, Any]],
    metadata: list[dict[str, Any]],
    scored: list[RuntimeScoredRecord],
    aggregates: list[RuntimeVariantAggregate],
    paired_lift: dict[str, Any],
    family_lift: dict[str, Any],
    traces: list[RuntimeTrace],
    calibration_traces: list[CalibrationTrace],
    budget_decision: str,
    final_decision: str,
) -> dict[str, Any]:
    total_attempts = len(records)
    total_completed = sum(1 for r in records if r.get("status") == "COMPLETED")
    total_failed = sum(1 for r in records if r.get("status") == "FAILED")
    total_cost = sum(r.get("estimated_cost_usd") or 0.0 for r in records)

    cost_by_variant: dict[str, float] = defaultdict(float)
    for r in records:
        cost_by_variant[r.get("variant_name", "unknown")] += r.get("estimated_cost_usd") or 0.0

    repair_metrics = compute_repair_metrics(traces) if traces else {}
    audit_distribution = compute_audit_decision_distribution(traces) if traces else {}

    return {
        "run_id": config.run_id,
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "v0.9.0",
        "experiment_type": "runtime_paired_lift",
        "dataset_name": dataset.get("dataset_name", ""),
        "dataset_version": dataset.get("dataset_version", ""),
        "dataset_size": len(dataset.get("tasks", [])),
        "dataset_hash": dataset.get("dataset_hash", ""),
        "manifest_hash": dataset.get("manifest_hash", ""),
        "provider_mode": config.provider_mode,
        "variants": [v.variant_name for v in config.variants],
        "total_expected": preflight.expected_attempts,
        "total_attempted": total_attempts,
        "total_completed": total_completed,
        "total_failed": total_failed,
        "total_cost_usd": round(total_cost, 8),
        "cost_by_variant": {k: round(v, 8) for k, v in sorted(cost_by_variant.items())},
        "budget_cap_usd": config.budget_cap_usd,
        "budget_decision": budget_decision,
        "mean_score_overall": (
            sum(a.mean_score for a in aggregates) / len(aggregates) if aggregates else 0.0
        ),
        "aggregates": [a.to_dict() for a in aggregates],
        "paired_lift": paired_lift,
        "family_lift": family_lift,
        "repair_metrics": repair_metrics,
        "audit_decision_distribution": audit_distribution,
        "runtime_variant_trace_count": len(traces),
        "calibration_trace_count": len(calibration_traces),
        "authorized_claims": list(AUTHORIZED_CLAIMS),
        "prohibited_claims": list(PROHIBITED_CLAIMS),
        "preflight_decision": preflight.decision,
        "preflight_blockers": list(preflight.blockers),
        "final_decision": final_decision,
    }


def _empty_result(
    config: RuntimeConfig,
    dataset: dict[str, Any],
    preflight: RuntimePreflight,
    final_decision: str,
) -> dict[str, Any]:
    return {
        "config": config,
        "dataset": dataset,
        "preflight": preflight.to_dict(),
        "records": [],
        "provider_errors": [],
        "request_metadata": [],
        "scored": [],
        "aggregates": [],
        "paired_lift": {},
        "family_lift": {},
        "traces": [],
        "calibration_traces": [],
        "summary": _build_summary(
            config, preflight, dataset, [], [], [], [], [], {}, {}, [], [],
            "BLOCKED", final_decision,
        ),
    }


def run_runtime_paired_lift(
    config: RuntimeConfig,
    adapter: RuntimeProviderAdapter | None = None,
    skip_dataset_load: bool = False,
    preloaded_dataset: dict[str, Any] | None = None,
) -> dict[str, Any]:
    from .runtime_lift_audit import build_repair_prompt, run_audit

    if preloaded_dataset is not None:
        dataset = preloaded_dataset
    elif skip_dataset_load:
        dataset = {"dataset_name": "", "dataset_version": "", "dataset_hash": "", "manifest_hash": "", "tasks": []}
    else:
        dataset = _load_dataset(config)

    ds_hash = dataset.get("dataset_hash", None)
    manifest_h = dataset.get("manifest_hash", None)
    task_cnt = len(dataset.get("tasks", []))

    preflight = evaluate_runtime_preflight(config, ds_hash, manifest_h, task_cnt)
    if not preflight.can_execute:
        return _empty_result(config, dataset, preflight, BLOCKED_PREFLIGHT)

    selected_tasks = dataset["tasks"][: config.expected_task_count]
    estimated_projected = (
        sum(v.estimated_cost_per_task_usd for v in config.variants) * len(selected_tasks)
    )
    if estimated_projected > config.budget_cap_usd:
        return _empty_result(config, dataset, preflight, BLOCKED_BUDGET)

    if adapter is None:
        from benchmarks.finitexo_code_matrix_v0_5.real_provider_authorized.direct_transport import (
            direct_provider_adapter,
        )
        base_adapter = direct_provider_adapter
    else:
        base_adapter = adapter

    records: list[dict[str, Any]] = []
    provider_errors: list[dict[str, Any]] = []
    request_metadata: list[dict[str, Any]] = []
    traces: list[RuntimeTrace] = []
    calibration_traces: list[CalibrationTrace] = []
    total_cost: float = 0.0
    budget_exhausted = False

    for variant in config.variants:
        for task in selected_tasks:
            if budget_exhausted:
                continue

            est_cost = variant.estimated_cost_per_task_usd
            if total_cost + est_cost > config.budget_cap_usd:
                budget_exhausted = True
                continue

            task_payload = _build_wrapper_task(task) if variant.use_xendris_wrapper else task
            task_family = task.get("family", "unknown")

            meta = {
                "run_id": config.run_id,
                "variant_name": variant.variant_name,
                "provider_name": variant.provider_name,
                "model_name": variant.model_name,
                "task_id": task.get("task_id", ""),
                "task_family": task_family,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "dataset_hash": ds_hash,
                "manifest_hash": manifest_h,
                "use_xendris_wrapper": variant.use_xendris_wrapper,
                "use_runtime_loop": variant.use_runtime_loop,
            }
            request_metadata.append(meta)

            start = perf_counter()
            try:
                result = base_adapter(variant, task_payload, config)
                latency_ms = round((perf_counter() - start) * 1000, 3)
                raw_text = getattr(result, "raw_response_text", result if isinstance(result, str) else "")
                cost = getattr(result, "estimated_cost_usd", est_cost) or est_cost
                total_cost += cost

                if variant.use_calibrated_runtime:
                    # Calibrated runtime: runtime loop + calibration
                    initial_response = raw_text
                    initial_audit = run_audit(initial_response, task)

                    if initial_audit.decision == RuntimeAuditDecision.REPAIR_REQUIRED:
                        repair_prompt = build_repair_prompt(
                            task.get("prompt", ""), initial_response, initial_audit
                        )
                        repair_task = {**task, "prompt": repair_prompt}
                        start_r = perf_counter()
                        try:
                            repair_result = base_adapter(variant, repair_task, config)
                            repair_latency_ms = round((perf_counter() - start_r) * 1000, 3)
                            repair_raw = getattr(repair_result, "raw_response_text", repair_result if isinstance(repair_result, str) else "")
                            repair_cost = getattr(repair_result, "estimated_cost_usd", est_cost * 0.5) or est_cost * 0.5
                            total_cost += repair_cost
                            repair_audit = run_audit(repair_raw, task)
                            repair_attempted = True
                            repair_response = repair_raw
                            if repair_audit.score >= initial_audit.score:
                                runtime_final = repair_raw
                                runtime_final_audit = repair_audit
                            else:
                                runtime_final = initial_response
                                runtime_final_audit = initial_audit
                        except Exception:
                            repair_attempted = True
                            repair_response = None
                            repair_audit = None
                            runtime_final = initial_response
                            runtime_final_audit = initial_audit
                    elif initial_audit.decision == RuntimeAuditDecision.BLOCK:
                        runtime_final = _controlled_block_response(initial_audit)
                        runtime_final_audit = run_audit(runtime_final, task)
                        repair_attempted = False
                        repair_response = None
                        repair_audit = None
                    else:
                        runtime_final = initial_response
                        runtime_final_audit = initial_audit
                        repair_attempted = False
                        repair_response = None
                        repair_audit = None

                    # Calibration step
                    claim_classification = _run_claim_classification(runtime_final, task)
                    evidence_status = _run_evidence_resolution(claim_classification)
                    confidence_band = _run_confidence_banding(runtime_final, evidence_status)
                    allowed_lang, blocked_lang = _run_language_selection(runtime_final, claim_classification)
                    calibrated_final = _produce_calibrated_final(
                        runtime_final, claim_classification, evidence_status,
                        confidence_band, allowed_lang, blocked_lang,
                    )

                    trace = RuntimeTrace(
                        task_id=task.get("task_id", ""),
                        provider_name=variant.provider_name,
                        variant_name=variant.variant_name,
                        initial_response=initial_response,
                        initial_audit=initial_audit,
                        audit_decision=initial_audit.decision,
                        repair_attempted=repair_attempted,
                        repair_response=repair_response,
                        repair_audit=repair_audit,
                        final_response=calibrated_final,
                        final_audit=runtime_final_audit,
                        prompt_tokens=getattr(result, "prompt_tokens", None),
                        completion_tokens=getattr(result, "completion_tokens", None),
                        total_tokens=getattr(result, "total_tokens", None),
                        estimated_cost_usd=cost,
                    )
                    traces.append(trace)

                    calibration_trace = CalibrationTrace(
                        task_id=task.get("task_id", ""),
                        provider_name=variant.provider_name,
                        variant_name=variant.variant_name,
                        initial_response=runtime_final,
                        claim_classification=claim_classification,
                        evidence_status=evidence_status,
                        confidence_band=confidence_band,
                        allowed_language=allowed_lang,
                        blocked_language=blocked_lang,
                        final_calibrated_response=calibrated_final,
                        estimated_cost_usd=cost,
                    )
                    calibration_traces.append(calibration_trace)

                    records.append({
                        "run_id": config.run_id,
                        "variant_name": variant.variant_name,
                        "provider_name": variant.provider_name,
                        "model_name": getattr(result, "provider_reported_model", variant.model_name),
                        "provider_mode": config.provider_mode,
                        "task_id": task.get("task_id", ""),
                        "task_family": task_family,
                        "task_version": task.get("task_version", ""),
                        "status": "COMPLETED",
                        "response_text": calibrated_final,
                        "normalized_response_text": " ".join(calibrated_final.split()),
                        "error_type": None,
                        "error_message_sanitized": None,
                        "latency_ms": latency_ms,
                        "prompt_tokens": getattr(result, "prompt_tokens", None),
                        "completion_tokens": getattr(result, "completion_tokens", None),
                        "total_tokens": getattr(result, "total_tokens", None),
                        "estimated_cost_usd": cost,
                        "budget_status": "WITHIN_BUDGET" if not budget_exhausted else "BUDGET_EXHAUSTED",
                        "frozen_task_hash": task.get("content_hash", task.get("task_id", "")),
                        "use_xendris_wrapper": variant.use_xendris_wrapper,
                        "use_runtime_loop": variant.use_runtime_loop,
                        "use_calibrated_runtime": variant.use_calibrated_runtime,
                        "audit_decision": initial_audit.decision.value,
                        "repair_attempted": repair_attempted,
                    })
                elif variant.use_runtime_loop:
                    # Runtime variant: audit, decide, repair if needed
                    initial_response = raw_text
                    initial_audit = run_audit(initial_response, task)

                    if initial_audit.decision == RuntimeAuditDecision.REPAIR_REQUIRED:
                        repair_prompt = build_repair_prompt(
                            task.get("prompt", ""), initial_response, initial_audit
                        )
                        repair_task = {**task, "prompt": repair_prompt}
                        start_r = perf_counter()
                        try:
                            repair_result = base_adapter(variant, repair_task, config)
                            repair_latency_ms = round((perf_counter() - start_r) * 1000, 3)
                            repair_raw = getattr(repair_result, "raw_response_text", repair_result if isinstance(repair_result, str) else "")
                            repair_cost = getattr(repair_result, "estimated_cost_usd", est_cost * 0.5) or est_cost * 0.5
                            total_cost += repair_cost
                            repair_audit = run_audit(repair_raw, task)
                            repair_attempted = True
                            repair_response = repair_raw

                            # Use repair response if it improved, otherwise degrade gracefully
                            if repair_audit.score >= initial_audit.score:
                                final_response = repair_raw
                                final_audit = repair_audit
                            else:
                                final_response = initial_response
                                final_audit = initial_audit
                        except Exception:
                            repair_attempted = True
                            repair_response = None
                            repair_audit = None
                            final_response = initial_response
                            final_audit = initial_audit
                    elif initial_audit.decision == RuntimeAuditDecision.BLOCK:
                        final_response = _controlled_block_response(initial_audit)
                        final_audit = run_audit(final_response, task)
                        repair_attempted = False
                        repair_response = None
                        repair_audit = None
                    else:
                        # ALLOW or ALLOW_WITH_LIMITATIONS
                        final_response = initial_response
                        final_audit = initial_audit
                        repair_attempted = False
                        repair_response = None
                        repair_audit = None

                    trace = RuntimeTrace(
                        task_id=task.get("task_id", ""),
                        provider_name=variant.provider_name,
                        variant_name=variant.variant_name,
                        initial_response=initial_response,
                        initial_audit=initial_audit,
                        audit_decision=initial_audit.decision,
                        repair_attempted=repair_attempted,
                        repair_response=repair_response,
                        repair_audit=repair_audit,
                        final_response=final_response,
                        final_audit=final_audit,
                        prompt_tokens=getattr(result, "prompt_tokens", None),
                        completion_tokens=getattr(result, "completion_tokens", None),
                        total_tokens=getattr(result, "total_tokens", None),
                        estimated_cost_usd=cost,
                    )
                    traces.append(trace)

                    records.append({
                        "run_id": config.run_id,
                        "variant_name": variant.variant_name,
                        "provider_name": variant.provider_name,
                        "model_name": getattr(result, "provider_reported_model", variant.model_name),
                        "provider_mode": config.provider_mode,
                        "task_id": task.get("task_id", ""),
                        "task_family": task_family,
                        "task_version": task.get("task_version", ""),
                        "status": "COMPLETED",
                        "response_text": final_response,
                        "normalized_response_text": " ".join(final_response.split()),
                        "error_type": None,
                        "error_message_sanitized": None,
                        "latency_ms": latency_ms,
                        "prompt_tokens": getattr(result, "prompt_tokens", None),
                        "completion_tokens": getattr(result, "completion_tokens", None),
                        "total_tokens": getattr(result, "total_tokens", None),
                        "estimated_cost_usd": cost,
                        "budget_status": "WITHIN_BUDGET" if not budget_exhausted else "BUDGET_EXHAUSTED",
                        "frozen_task_hash": task.get("content_hash", task.get("task_id", "")),
                        "use_xendris_wrapper": variant.use_xendris_wrapper,
                        "use_runtime_loop": variant.use_runtime_loop,
                        "use_calibrated_runtime": variant.use_calibrated_runtime,
                        "audit_decision": initial_audit.decision.value,
                        "repair_attempted": repair_attempted,
                    })
                else:
                    # Base or wrapper variant: score directly
                    records.append({
                        "run_id": config.run_id,
                        "variant_name": variant.variant_name,
                        "provider_name": variant.provider_name,
                        "model_name": getattr(result, "provider_reported_model", variant.model_name),
                        "provider_mode": config.provider_mode,
                        "task_id": task.get("task_id", ""),
                        "task_family": task_family,
                        "task_version": task.get("task_version", ""),
                        "status": "COMPLETED",
                        "response_text": raw_text,
                        "normalized_response_text": " ".join(raw_text.split()),
                        "error_type": None,
                        "error_message_sanitized": None,
                        "latency_ms": latency_ms,
                        "prompt_tokens": getattr(result, "prompt_tokens", None),
                        "completion_tokens": getattr(result, "completion_tokens", None),
                        "total_tokens": getattr(result, "total_tokens", None),
                        "estimated_cost_usd": cost,
                        "budget_status": "WITHIN_BUDGET" if not budget_exhausted else "BUDGET_EXHAUSTED",
                        "frozen_task_hash": task.get("content_hash", task.get("task_id", "")),
                        "use_xendris_wrapper": variant.use_xendris_wrapper,
                        "use_runtime_loop": variant.use_runtime_loop,
                        "use_calibrated_runtime": variant.use_calibrated_runtime,
                        "audit_decision": None,
                        "repair_attempted": False,
                    })
            except Exception as exc:
                latency_ms = round((perf_counter() - start) * 1000, 3)
                error_type = type(exc).__name__
                error_msg = _sanitize_error(str(exc))
                provider_errors.append({
                    "variant_name": variant.variant_name,
                    "provider_name": variant.provider_name,
                    "model_name": variant.model_name,
                    "task_id": task.get("task_id", ""),
                    "task_family": task_family,
                    "error_type": error_type,
                    "error_message_sanitized": error_msg,
                })
                records.append({
                    "run_id": config.run_id,
                    "variant_name": variant.variant_name,
                    "provider_name": variant.provider_name,
                    "model_name": variant.model_name,
                    "provider_mode": config.provider_mode,
                    "task_id": task.get("task_id", ""),
                    "task_family": task_family,
                    "task_version": task.get("task_version", ""),
                    "status": "FAILED",
                    "response_text": "",
                    "normalized_response_text": "",
                    "error_type": error_type,
                    "error_message_sanitized": error_msg,
                    "latency_ms": latency_ms,
                    "prompt_tokens": None,
                    "completion_tokens": None,
                    "total_tokens": None,
                    "estimated_cost_usd": None,
                    "budget_status": "WITHIN_BUDGET" if not budget_exhausted else "BUDGET_EXHAUSTED",
                    "frozen_task_hash": task.get("content_hash", task.get("task_id", "")),
                    "use_xendris_wrapper": variant.use_xendris_wrapper,
                    "use_runtime_loop": variant.use_runtime_loop,
                    "use_calibrated_runtime": variant.use_calibrated_runtime,
                    "audit_decision": None,
                    "repair_attempted": False,
                })

    budget_decision = "WITHIN_BUDGET" if total_cost <= config.budget_cap_usd and not budget_exhausted else "BUDGET_EXHAUSTED"

    scored: list[RuntimeScoredRecord] = []
    for r in records:
        sr = score_runtime_response(
            variant_name=r["variant_name"],
            provider_name=r["provider_name"],
            model_name=r["model_name"],
            task_id=r["task_id"],
            task_family=r.get("task_family", "unknown"),
            response_text=r.get("response_text", ""),
            estimated_cost_usd=r.get("estimated_cost_usd"),
        )
        scored.append(sr)

    aggregates = aggregate_by_variant(scored)
    paired_lift = compute_paired_lift(scored, aggregates)
    family_lift = compute_family_lift(scored)

    has_failures = any(r["status"] == "FAILED" for r in records)
    final_decision = COMPLETED if not has_failures and not budget_exhausted else PARTIAL

    summary = _build_summary(
        config, preflight, dataset, records, provider_errors, request_metadata,
        scored, aggregates, paired_lift, family_lift, traces, calibration_traces,
        budget_decision, final_decision,
    )

    return {
        "config": config,
        "dataset": dataset,
        "preflight": preflight.to_dict(),
        "records": records,
        "provider_errors": provider_errors,
        "request_metadata": request_metadata,
        "scored": scored,
        "aggregates": aggregates,
        "paired_lift": paired_lift,
        "family_lift": family_lift,
        "traces": traces,
        "calibration_traces": calibration_traces,
        "summary": summary,
    }


def _run_claim_classification(response_text: str, task: dict) -> dict[str, str]:
    claims: dict[str, str] = {}
    lines = response_text.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line and len(line) > 10:
            claim_type = "functional" if any(w in line.lower() for w in ["fix", "implement", "return", "create"]) else "explanatory"
            claims[line[:80]] = claim_type
    return claims if claims else {"response": "functional"}


def _run_evidence_resolution(claims: dict[str, str]) -> dict[str, str]:
    return {k: "diagnostic_only" for k in claims}


def _run_confidence_banding(response_text: str, evidence: dict[str, str]) -> str:
    return "diagnostic"


def _run_language_selection(response_text: str, claims: dict[str, str]) -> tuple[list[str], list[str]]:
    blocked = []
    if "superior" in response_text.lower():
        blocked.append("superiority claim")
    if "best" in response_text.lower() and "one of the" not in response_text.lower():
        blocked.append("absolute best claim")
    safe_lines = [l for l in response_text.split("\n") if not any(b in l.lower() for b in ["sk-", "secret", "api_key"])]
    allowed = safe_lines if safe_lines else [response_text]
    return allowed, blocked


def _calibrated_claim_classification(
    response_text: str,
    calibration_prompt: str,
) -> dict[str, str]:
    claims: dict[str, str] = {}
    for line in response_text.split("."):
        lower = line.strip().lower()
        if not lower:
            continue
        if "claim" in lower or "assert" in lower:
            key = line.strip()[:60]
            claims[key] = "diagnostic_signal_only"
    return claims or {"diagnostic_stub": "diagnostic_signal_only"}


def _calibrated_evidence_resolution(
    response_text: str,
    calibration_prompt: str,
) -> dict[str, str]:
    evidence: dict[str, str] = {}
    for line in response_text.split("."):
        lower = line.strip().lower()
        if not lower:
            continue
        if "evidence" in lower or "example" in lower or "source" in lower:
            key = line.strip()[:60]
            evidence[key] = "diagnostic_signal_only"
    return evidence or {"diagnostic_stub": "diagnostic_signal_only"}


def _calibrated_confidence_banding(response_text: str) -> str:
    if not response_text.strip():
        return "uncertain"
    length = len(response_text.split())
    if length > 100:
        return "moderate"
    elif length > 30:
        return "high"
    return "low"


def _calibrated_language_selection(
    response_text: str,
) -> tuple[list[str], list[str]]:
    blocked: list[str] = []
    for b in ["sk-", "secret", "api_key", "password", "token"]:
        if b in response_text.lower():
            blocked.append(b)
    safe_lines = [
        l for l in response_text.split("\n")
        if not any(b in l.lower() for b in ["sk-", "secret", "api_key"])
    ]
    allowed = safe_lines if safe_lines else [response_text]
    return allowed, blocked


def _perform_calibration_pass(
    response_text: str,
    claims: dict[str, str],
    evidence: dict[str, str],
    confidence_band: str,
    allowed_lang: list[str],
) -> str:
    return _produce_calibrated_final(response_text, claims, evidence, confidence_band, allowed_lang, [])


def _produce_calibrated_final(
    response_text: str,
    claims: dict[str, str],
    evidence: dict[str, str],
    confidence_band: str,
    allowed_lang: list[str],
    blocked_lang: list[str],
) -> str:
    header = f"[Confidence: {confidence_band} | Claims: {len(claims)} | Evidence: diagnostic_only]"
    body = "\n".join(allowed_lang) if allowed_lang else response_text
    disclaimer = "\nNote: This response is diagnostic-only and does not imply production readiness."
    return header + "\n\n" + body + disclaimer


def _controlled_block_response(audit: RuntimeAuditResult) -> str:
    lines = [
        "I cannot complete this request as stated due to the following audit findings:",
    ]
    for reason in audit.reasons:
        lines.append(f"- {reason}")
    lines.append("")
    lines.append("This is a controlled limitation response. The request requires modification or human review.")
    return "\n".join(lines)


def write_runtime_lift_artifacts(run_result: dict[str, Any]) -> dict[str, Any]:
    summary = run_result["summary"]
    outdir = run_result["config"].output_dir
    outdir.mkdir(parents=True, exist_ok=True)

    _write_json(outdir / "summary.json", summary)
    (outdir / "report.md").write_text(
        build_runtime_lift_report(summary), encoding="utf-8"
    )
    _write_jsonl(outdir / "responses.jsonl", run_result["records"])
    _write_jsonl(
        outdir / "scores.jsonl",
        [s.to_dict() for s in run_result["scored"]],
    )
    _write_json(outdir / "costs.json", {
        "total_cost_usd": summary.get("total_cost_usd"),
        "cost_by_variant": summary.get("cost_by_variant"),
        "budget_cap_usd": summary.get("budget_cap_usd"),
        "budget_decision": summary.get("budget_decision"),
    })
    _write_jsonl(outdir / "errors.jsonl", run_result["provider_errors"])
    _write_jsonl(outdir / "metadata.jsonl", run_result["request_metadata"])
    _write_json(outdir / "preflight.json", run_result["preflight"])
    _write_json(outdir / "gate.json", {
        "preflight": run_result["preflight"],
        "final_decision": summary.get("final_decision"),
    })

    if run_result.get("paired_lift"):
        _write_json(outdir / "paired_lift.json", run_result["paired_lift"])

    if run_result.get("family_lift"):
        _write_json(outdir / "family_lift.json", run_result["family_lift"])

    if run_result.get("calibration_traces"):
        _write_jsonl(outdir / "calibration_traces.jsonl", [ct.to_dict() for ct in run_result["calibration_traces"]])

        claim_status_rows = []
        confidence_band_rows = []
        allowed_blocked_rows = []
        calibrated_final_rows = []
        for ct in run_result["calibration_traces"]:
            claim_status_rows.append({
                "task_id": ct.task_id,
                "provider": ct.provider_name,
                "variant": ct.variant_name,
                "claim_classification": ct.claim_classification,
                "evidence_status": ct.evidence_status,
            })
            confidence_band_rows.append({
                "task_id": ct.task_id,
                "provider": ct.provider_name,
                "variant": ct.variant_name,
                "confidence_band": ct.confidence_band,
            })
            allowed_blocked_rows.append({
                "task_id": ct.task_id,
                "provider": ct.provider_name,
                "variant": ct.variant_name,
                "allowed_language": ct.allowed_language,
                "blocked_language": ct.blocked_language,
            })
            calibrated_final_rows.append({
                "task_id": ct.task_id,
                "provider": ct.provider_name,
                "variant": ct.variant_name,
                "final_calibrated_response": ct.final_calibrated_response,
            })
        _write_jsonl(outdir / "claim_status.jsonl", claim_status_rows)
        _write_jsonl(outdir / "confidence_bands.jsonl", confidence_band_rows)
        _write_jsonl(outdir / "allowed_blocked_language.jsonl", allowed_blocked_rows)
        _write_jsonl(outdir / "calibrated_final_responses.jsonl", calibrated_final_rows)

    if run_result.get("traces"):
        _write_jsonl(outdir / "runtime_traces.jsonl", [t.to_dict() for t in run_result["traces"]])

        audit_decisions = [
            {
                "task_id": t.task_id,
                "provider": t.provider_name,
                "variant": t.variant_name,
                "audit_decision": t.audit_decision.value,
                "reasons": t.initial_audit.reasons,
                "blocked_claims": t.initial_audit.blocked_claims,
                "repair_reasons": t.initial_audit.repair_reasons,
            }
            for t in run_result["traces"]
        ]
        _write_jsonl(outdir / "audit_decisions.jsonl", audit_decisions)

        # Score before vs after only meaningful for repaired traces
        repair_attempts = []
        for t in run_result["traces"]:
            if t.repair_attempted:
                from .runtime_lift_scoring import score_runtime_response as _scr
                score_before = _scr(t.variant_name, t.provider_name, "", t.task_id, "",
                                   t.initial_response).score_total if t.initial_response else 0.0
                score_after_raw = t.final_response if t.final_response != t.initial_response else (
                    t.repair_response if t.repair_response else t.final_response
                )
                score_after = _scr(t.variant_name, t.provider_name, "", t.task_id, "",
                                  score_after_raw).score_total if score_after_raw else 0.0
                repair_success = score_after > score_before if (score_after_raw and t.initial_response) else None
                repair_attempts.append({
                    "task_id": t.task_id,
                    "provider": t.provider_name,
                    "repair_attempted": True,
                    "repair_reason": "; ".join(t.initial_audit.repair_reasons),
                    "repair_success": repair_success,
                    "score_before": round(score_before, 4),
                    "score_after": round(score_after, 4),
                })
        _write_jsonl(outdir / "repair_attempts.jsonl", repair_attempts)

    _check_integrity(run_result, outdir)

    return summary


def _check_integrity(run_result: dict[str, Any], outdir: Path) -> None:
    records = run_result.get("records", [])
    scored = run_result.get("scored", [])
    metadata = run_result.get("request_metadata", [])
    errors = run_result.get("provider_errors", [])
    traces = run_result.get("traces", [])

    responses_count = len(records)
    scores_count = len(scored)
    metadata_count = len(metadata)
    trace_count = len(traces)
    cal_trace_count = len(run_result.get("calibration_traces", []))
    expected_traces = 120  # 4 runtime-loop variants * 30 tasks

    integrity = {
        "responses_count": responses_count,
        "scores_count": scores_count,
        "metadata_count": metadata_count,
        "trace_count": trace_count,
        "calibration_trace_count": cal_trace_count,
        "errors_count": len(errors),
        "responses_match_240": responses_count == 240,
        "scores_match_240": scores_count == 240,
        "metadata_match_240": metadata_count == 240,
        "traces_match_120": trace_count == expected_traces,
        "calibration_traces_match_60": cal_trace_count == 60,
        "evidence_integrity_ready": (
            responses_count == 240
            and scores_count == 240
            and metadata_count == 240
            and trace_count == expected_traces
            and cal_trace_count == 60
        ),
    }
    _write_json(outdir / "evidence_integrity.json", integrity)


def _load_dotenv_for_main() -> None:
    dotenv_path = Path("frontend/.env.local")
    if not dotenv_path.exists():
        return
    for line in dotenv_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("\"'")
        if key in ("DEEPSEEK_API_KEY", "OPENAI_API_KEY", "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM"):
            os.environ.setdefault(key, value)


def main() -> int:
    _load_dotenv_for_main()
    suffix = os.environ.get("FINITEXO_RUNTIME_LIFT_RUN_ID_SUFFIX", "").strip()
    base_config = RuntimeConfig()
    config = base_config.with_run_id_suffix(suffix) if suffix else base_config
    result = run_runtime_paired_lift(config)
    summary = write_runtime_lift_artifacts(result)
    print(summary.get("final_decision"))
    return 0 if summary.get("final_decision") in (COMPLETED, PARTIAL) else 1


if __name__ == "__main__":
    raise SystemExit(main())
