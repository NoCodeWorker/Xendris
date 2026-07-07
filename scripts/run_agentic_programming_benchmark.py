from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from xendris.benchmarking.agentic_programming import (
    BenchmarkConfig,
    BenchmarkRunOutput,
    compute_scores,
    evaluate_excellence_gate,
    export_to_jsonl,
    generate_markdown_report,
    load_dataset,
    run_benchmark,
)
from xendris.benchmarking.agentic_programming.types import AgentVariant, BenchmarkRunOutput, TaskResult
from xendris.benchmarking.agentic_programming.agents.deepseek_provider import get_deepseek_api_key
from xendris.benchmarking.agentic_programming.agents.openai_provider import get_openai_api_key
from xendris.benchmarking.agentic_programming.runner import (
    LIVE_DEEPSEEK_AGENTS,
    LIVE_OPENAI_AGENTS,
)


ORACLE_SCORE = 1.0
DEEPSEEK_KEY_NAME = "DEEPSEEK_API_KEY"
OPENAI_KEY_NAME = "OPENAI_API_KEY"
PROVIDER_KEY_NAMES = {
    "deepseek": DEEPSEEK_KEY_NAME,
    "openai": OPENAI_KEY_NAME,
}
DEFAULT_PROVIDER_MODELS = {
    "deepseek": "deepseek-v4-flash",
    "openai": "gpt-4.1-mini",
}
READY = "READY_FOR_INTERPRETATION"
WARNINGS = "WARNINGS_PRESENT"
BLOCKED = "BLOCKED_FOR_INTERPRETATION"


def _parse_env_file_value(path: str, key_name: str = DEEPSEEK_KEY_NAME) -> str | None:
    if not os.path.isfile(path):
        return None

    with open(path, encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() != key_name:
                continue
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            return value or None

    return None


def load_api_key_from_env_files(key_name: str, repo_root: str | None = None) -> dict[str, object]:
    if os.environ.get(key_name):
        return {
            "detected": True,
            "key_name": key_name,
            "source": "process_env",
            "credential_source": f"env:{key_name}",
        }

    root = repo_root or os.getcwd()
    candidates = [
        (".env.local", os.path.join(root, ".env.local")),
        (".env", os.path.join(root, ".env")),
        ("frontend/.env.local", os.path.join(root, "frontend", ".env.local")),
        ("frontend/.env", os.path.join(root, "frontend", ".env")),
    ]
    for source, path in candidates:
        value = _parse_env_file_value(path, key_name)
        if value:
            os.environ[key_name] = value
            return {
                "detected": True,
                "key_name": key_name,
                "source": source,
                "credential_source": f"dotenv:{source}/{key_name}",
            }

    return {
        "detected": False,
        "key_name": key_name,
        "source": "missing",
        "credential_source": "missing",
    }


def load_deepseek_api_key_from_env_files(repo_root: str | None = None) -> dict[str, object]:
    return load_api_key_from_env_files(DEEPSEEK_KEY_NAME, repo_root)


def load_openai_api_key_from_env_files(repo_root: str | None = None) -> dict[str, object]:
    return load_api_key_from_env_files(OPENAI_KEY_NAME, repo_root)


def _compute_category_breakdown(results: list[TaskResult], dataset_path: str) -> dict:
    tasks = load_dataset(dataset_path)
    task_map = {t.sample_id: t for t in tasks}
    by_category: dict[str, dict] = {}
    for r in results:
        task = task_map.get(r.sample_id)
        cat = task.category if task else "unknown"
        if cat not in by_category:
            by_category[cat] = {"total": 0, "visible_passed": 0, "hidden_passed_or_none": 0}
        by_category[cat]["total"] += 1
        if r.visible_tests_passed:
            by_category[cat]["visible_passed"] += 1
        if r.hidden_tests_passed is not False:
            by_category[cat]["hidden_passed_or_none"] += 1
    return by_category


def _compute_commercial_metrics(results: list[TaskResult]) -> dict:
    total = len(results) or 1
    visible_pass = sum(1 for r in results if r.visible_tests_passed)
    hidden_pass = sum(1 for r in results if r.hidden_tests_passed)
    api_ok = sum(1 for r in results if r.api_contract_preserved)
    forbidden_ok = sum(1 for r in results if r.no_forbidden_files_touched)
    false_success_ok = sum(1 for r in results if r.no_false_success_claim)
    minimal = sum(1 for r in results if r.minimal_patch)
    security_ok = sum(1 for r in results if r.security_clean)
    verified_success = sum(1 for r in results if r.visible_tests_passed and r.hidden_tests_passed is not False)
    total_cost = sum(r.cost_estimate for r in results if r.cost_estimate is not None)
    latencies = [r.latency_ms for r in results if r.latency_ms is not None]

    return {
        "task_success_rate": round(
            verified_success / total, 4
        ),
        "verified_successful_count": verified_success,
        "visible_test_pass_rate": round(visible_pass / total, 4),
        "hidden_test_pass_rate": round(hidden_pass / total, 4),
        "api_preservation_rate": round(api_ok / total, 4),
        "forbidden_file_touch_rate": round((total - forbidden_ok) / total, 4),
        "false_success_claim_rate": round((total - false_success_ok) / total, 4),
        "unauthorized_dependency_rate": 0.0,
        "minimal_patch_rate": round(minimal / total, 4),
        "security_clean_rate": round(security_ok / total, 4),
        "average_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else None,
        "estimated_cost_total": round(total_cost, 6) if total_cost else None,
        "cost_per_verified_successful_task": round(total_cost / verified_success, 6) if total_cost and verified_success > 0 else None,
    }


def _group_by_variant(results: list[TaskResult]) -> dict[str, list[TaskResult]]:
    grouped: dict[str, list[TaskResult]] = {}
    for result in results:
        grouped.setdefault(result.agent_variant, []).append(result)
    return grouped


def _compute_metrics_by_variant(results: list[TaskResult], scores: dict[str, dict]) -> dict[str, dict]:
    metrics: dict[str, dict] = {}
    for variant, variant_results in _group_by_variant(results).items():
        commercial = _compute_commercial_metrics(variant_results)
        score = scores.get(variant, {})
        total = len(variant_results)
        avg_iterations = (
            sum(r.iterations_used for r in variant_results) / total
            if total
            else 0
        )
        metrics[variant] = {
            "total_samples": total,
            "avg_score": score.get("total_score"),
            "task_success_rate": commercial["task_success_rate"],
            "verified_success_rate": commercial["task_success_rate"],
            "visible_test_pass_rate": commercial["visible_test_pass_rate"],
            "hidden_test_pass_rate": commercial["hidden_test_pass_rate"],
            "api_preservation_rate": commercial["api_preservation_rate"],
            "forbidden_file_touch_rate": commercial["forbidden_file_touch_rate"],
            "false_success_claim_rate": commercial["false_success_claim_rate"],
            "unauthorized_dependency_rate": commercial["unauthorized_dependency_rate"],
            "minimal_patch_rate": commercial["minimal_patch_rate"],
            "average_iterations": round(avg_iterations, 4),
            "average_latency_ms": commercial["average_latency_ms"],
            "estimated_cost_total": commercial["estimated_cost_total"],
            "cost_per_verified_successful_task": commercial["cost_per_verified_successful_task"],
            "distance_to_oracle": round(ORACLE_SCORE - score.get("total_score", 0), 4),
        }
    return metrics


def _get_base_variant(variant: str) -> str | None:
    if variant.startswith("deepseek_"):
        return "deepseek_base_agent"
    if variant.startswith("openai_"):
        return "openai_base_agent"
    return None


def _compute_deltas(scores: dict[str, dict]) -> dict:
    deepseek_base = None
    openai_base = None
    for variant, data in scores.items():
        if variant == "deepseek_base_agent":
            deepseek_base = data.get("total_score", 0)
        if variant == "openai_base_agent":
            openai_base = data.get("total_score", 0)

    deltas: dict[str, dict] = {}
    for variant, data in scores.items():
        variant_score = data.get("total_score", 0)
        base_variant = _get_base_variant(variant)
        base_score = None
        if base_variant == "deepseek_base_agent":
            base_score = deepseek_base
        elif base_variant == "openai_base_agent":
            base_score = openai_base

        delta_entry: dict = {
            "distance_to_oracle": round(ORACLE_SCORE - variant_score, 4),
        }
        if base_score is not None:
            delta_entry["delta_vs_base"] = round(variant_score - base_score, 4)
        if deepseek_base is not None:
            delta_entry["delta_vs_deepseek_base"] = round(variant_score - deepseek_base, 4)
        deltas[variant] = delta_entry
    return deltas


def _blocked_variant_reasons(
    scores: dict[str, dict],
    excellence_decisions: dict[str, str],
    results: list[TaskResult] | None = None,
) -> dict[str, str]:
    reasons: dict[str, str] = {}
    block_reasons_by_variant: dict[str, str] = {}
    if results:
        for r in results:
            if r.block_reason and r.agent_variant not in block_reasons_by_variant:
                block_reasons_by_variant[r.agent_variant] = r.block_reason
    for variant, decision in excellence_decisions.items():
        if decision != BLOCKED:
            continue
        data = scores.get(variant, {})
        specific_reason = block_reasons_by_variant.get(variant)
        if specific_reason:
            reasons[variant] = (
                f"Result-level gate blocked this variant: {specific_reason}. "
                f"(score={data.get('total_score')}, pass_rate={data.get('pass_rate')}). "
                "It is retained for comparison only and is not admitted as positive evidence."
            )
        else:
            reasons[variant] = (
                "Variant-level interpretation gate blocked this result "
                f"(score={data.get('total_score')}, pass_rate={data.get('pass_rate')}). "
                "It is retained for comparison only and is not admitted as positive evidence."
            )
    return reasons


def _evaluate_benchmark_level_decision(summary: dict, comparison_mode: bool) -> str:
    required_fields = [
        "dataset_name",
        "dataset_version",
        "dataset_size",
        "transport",
        "limitations",
        "no_universal_superiority_warning",
    ]
    missing = [field for field in required_fields if not summary.get(field)]
    if missing:
        return BLOCKED

    if not summary.get("providers") and not summary.get("provider"):
        return BLOCKED
    if not summary.get("models_by_variant") and not summary.get("model"):
        return BLOCKED

    warning_text = str(summary.get("no_universal_superiority_warning", "")).lower()
    if "superiority" not in warning_text or ("no " not in warning_text and "not " not in warning_text):
        return BLOCKED

    if not summary.get("no_openrouter_used"):
        return BLOCKED

    if summary.get("transport") != "direct":
        return BLOCKED

    if not summary.get("total_results") or not summary.get("scores_by_variant"):
        return BLOCKED

    if summary.get("blocked_variants"):
        return WARNINGS if comparison_mode else BLOCKED

    return READY


@dataclass(frozen=True)
class ExecutionIdentity:
    providers: list[str]
    transports: list[str]
    transport: str | None
    execution_provenance: dict[str, Any]


def _empty_benchmark_config() -> BenchmarkConfig:
    return BenchmarkConfig(
        dataset_path="", agent_variants=(), execution_mode="dry-run",
        output_dir="", agent_module="", max_concurrent=1, seed=42,
    )


def resolve_execution_identity(
    agents: list[str],
    config: BenchmarkConfig,
    results: list[TaskResult],
) -> ExecutionIdentity:
    # --- Provider resolution: variant prefix > config.provider > result.provider ---
    providers: list[str] = []
    has_variant_prefix = False

    if any(v.startswith("deepseek_") for v in agents):
        providers.append("deepseek")
        has_variant_prefix = True
    if any(v.startswith("openai_") for v in agents):
        providers.append("openai")
        has_variant_prefix = True

    if not providers and config.provider:
        providers.append(config.provider)

    if not providers:
        seen: set[str] = set()
        for r in results:
            if r.provider and r.provider not in seen:
                seen.add(r.provider)
                providers.append(r.provider)

    # --- Transport resolution: config.transport > result.transport (live only) ---
    is_live = config.execution_mode == "live"
    transport: str | None = None
    if is_live:
        transport = config.transport
        if not transport:
            for r in results:
                if r.transport:
                    transport = r.transport
                    break

    transports: list[str] = [transport] if transport else []

    # --- Provenance: describe which source was actually used ---
    if has_variant_prefix:
        provider_source = "variant_name_prefix"
        config_fallback = False
        result_fallback = False
    elif config.provider:
        provider_source = "config.provider"
        config_fallback = True
        result_fallback = False
    elif any(r.provider for r in results):
        provider_source = "result.provider"
        config_fallback = False
        result_fallback = True
    else:
        provider_source = "none"
        config_fallback = False
        result_fallback = False

    if config.transport and is_live:
        transport_source = "explicit_provider_default"
        transport_result_fallback = False
    elif any(r.transport for r in results):
        transport_source = "result.transport"
        transport_result_fallback = True
    else:
        transport_source = "none"
        transport_result_fallback = False

    execution_provenance: dict[str, Any] = {
        "provider_source": provider_source,
        "transport_source": transport_source,
        "variant_provider_inference": has_variant_prefix,
        "config_provider_fallback_used": config_fallback,
        "result_provider_fallback_used": result_fallback,
        "result_transport_fallback_used": transport_result_fallback,
    }

    return ExecutionIdentity(
        providers=providers,
        transports=transports,
        transport=transport,
        execution_provenance=execution_provenance,
    )


def _get_providers_from_variants(
    agents: list[str],
    config: BenchmarkConfig | None = None,
    results: list[TaskResult] | None = None,
) -> list[str]:
    _config = config if config is not None else _empty_benchmark_config()
    _results = results if results is not None else []
    return resolve_execution_identity(agents, _config, _results).providers


@dataclass(frozen=True)
class ModelSpec:
    alias: str
    provider: str
    model_id: str
    api_surface: str
    default_transport: str
    supports_reasoning: bool
    supports_structured_output: bool


_MODEL_REGISTRY: dict[tuple[str, str], ModelSpec] = {
    ("openai", "gpt-4.1-mini"): ModelSpec(
        alias="gpt-4.1-mini",
        provider="openai",
        model_id="gpt-4.1-mini",
        api_surface="chat_completions",
        default_transport="direct",
        supports_reasoning=False,
        supports_structured_output=True,
    ),
    ("openai", "gpt-4.1-nano"): ModelSpec(
        alias="gpt-4.1-nano",
        provider="openai",
        model_id="gpt-4.1-nano",
        api_surface="chat_completions",
        default_transport="direct",
        supports_reasoning=False,
        supports_structured_output=True,
    ),
    ("openai", "gpt-5.5"): ModelSpec(
        alias="gpt-5.5",
        provider="openai",
        model_id="gpt-5.5",
        api_surface="responses",
        default_transport="direct",
        supports_reasoning=True,
        supports_structured_output=True,
    ),
    ("deepseek", "deepseek-v4-flash"): ModelSpec(
        alias="deepseek-v4-flash",
        provider="deepseek",
        model_id="deepseek-v4-flash",
        api_surface="chat_completions",
        default_transport="direct",
        supports_reasoning=False,
        supports_structured_output=True,
    ),
}


def resolve_model_spec(
    provider: str | None,
    model_alias: str | None,
) -> ModelSpec | None:
    if not provider or not model_alias:
        return None
    return _MODEL_REGISTRY.get((provider, model_alias))


def _build_model_identity(
    config: BenchmarkConfig,
    providers: list[str],
    model_str: str,
) -> dict:
    provider = providers[0] if providers else config.provider
    model_alias = config.model or (model_str if model_str != "unknown" else None)
    spec = resolve_model_spec(provider, model_alias) if provider else None
    if spec is not None:
        return {
            "model_identity": {
                "provider": spec.provider,
                "model_alias": spec.alias,
                "model_id": spec.model_id,
                "api_surface": spec.api_surface,
                "default_transport": spec.default_transport,
                "supports_reasoning": spec.supports_reasoning,
                "supports_structured_output": spec.supports_structured_output,
                "resolved": True,
            }
        }
    return {
        "model_identity": {
            "provider": provider or "unknown",
            "model_alias": model_alias,
            "resolved": False,
        }
    }


@dataclass(frozen=True)
class InterpretationAdmissibility:
    provider_metadata_sufficient: bool
    transport_metadata_sufficient: bool
    model_metadata_sufficient: bool
    admissible: bool
    limitations: list[str]


def evaluate_interpretation_admissibility(
    identity: ExecutionIdentity,
    model_identity: dict[str, Any],
    execution_mode: str,
) -> InterpretationAdmissibility:
    ep = identity.execution_provenance
    limitations: list[str] = []

    is_live = execution_mode == "live"

    provider_source = ep.get("provider_source", "none")
    transport_source = ep.get("transport_source", "none")

    provider_metadata_sufficient = (
        provider_source in ("variant_name_prefix", "config.provider")
        if is_live else False
    )
    if is_live and provider_source == "result.provider":
        provider_metadata_sufficient = False
        limitations.append("provider_metadata_only_resolved_from_result_level")

    transport_metadata_sufficient = (
        transport_source == "explicit_provider_default"
        if is_live else False
    )
    if is_live and transport_source == "result.transport":
        transport_metadata_sufficient = False
        limitations.append("transport_metadata_only_resolved_from_result_level")

    model_metadata_sufficient = model_identity.get("resolved", False)
    if not model_metadata_sufficient and is_live:
        limitations.append("model_identity_not_resolved")

    admissible = provider_metadata_sufficient and transport_metadata_sufficient

    return InterpretationAdmissibility(
        provider_metadata_sufficient=provider_metadata_sufficient,
        transport_metadata_sufficient=transport_metadata_sufficient,
        model_metadata_sufficient=model_metadata_sufficient,
        admissible=admissible,
        limitations=limitations,
    )


@dataclass(frozen=True)
class EvidenceContract:
    contract_version: str
    identity_resolved: bool
    provenance_recorded: bool
    model_identity_resolved: bool
    interpretation_admissible: bool
    scoring_complete: bool
    decision: str
    limitations: list[str]


def build_evidence_contract(
    identity: ExecutionIdentity,
    model_identity: dict[str, Any],
    interpretation_admissibility: InterpretationAdmissibility,
    summary: dict,
    results: list[TaskResult],
    scores: dict,
) -> EvidenceContract:
    limitations: list[str] = []

    identity_resolved = bool(identity.providers) and identity.transport is not None

    ep = identity.execution_provenance
    provenance_recorded = bool(ep.get("provider_source", "")) and bool(ep.get("transport_source", ""))

    model_identity_resolved = model_identity.get("resolved", False)

    interpretation_admissible = interpretation_admissibility.admissible

    variants_in_results = sorted(set(r.agent_variant for r in results))
    scores_by_variant = summary.get("scores_by_variant", {}) or {}
    scoring_complete = bool(scores_by_variant) and all(
        isinstance(scores_by_variant.get(v), dict) and scores_by_variant[v].get("total_score") is not None
        for v in variants_in_results
    )

    limitations.extend(interpretation_admissibility.limitations)

    if not identity_resolved:
        limitations.append("identity_not_resolved")
    if not model_identity_resolved:
        if "model_identity_not_resolved" not in limitations:
            limitations.append("model_identity_not_resolved")
    if not scoring_complete:
        limitations.append("scoring_incomplete")

    if not interpretation_admissible:
        decision = "BLOCKED"
    elif (
        identity_resolved
        and provenance_recorded
        and model_identity_resolved
        and interpretation_admissible
        and scoring_complete
        and not limitations
    ):
        decision = "INTERPRETABLE"
    else:
        decision = "INTERPRETABLE_WITH_LIMITATIONS"

    return EvidenceContract(
        contract_version="0.1",
        identity_resolved=identity_resolved,
        provenance_recorded=provenance_recorded,
        model_identity_resolved=model_identity_resolved,
        interpretation_admissible=interpretation_admissible,
        scoring_complete=scoring_complete,
        decision=decision,
        limitations=limitations,
    )


def build_evidence_report_markdown(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    def a(val: Any) -> str:
        return str(val) if val is not None else ""

    lines.append("# Agentic Programming Benchmark Evidence Report")
    lines.append("")

    ec = summary.get("evidence_contract", {})
    decision = a(ec.get("decision", "unknown"))
    lines.append("## Evidence Decision")
    lines.append("")
    lines.append(f"Decision: {decision}")
    lines.append("")

    lines.append("## Execution Identity")
    lines.append("")
    ep = summary.get("execution_provenance", {})
    lines.append(f"- Providers: {a(summary.get('providers', summary.get('provider', 'N/A')))}")
    lines.append(f"- Transport: {a(summary.get('transport', 'N/A'))}")
    lines.append(f"- Transports: {a(summary.get('transports', []))}")
    lines.append(f"- Provider source: {a(ep.get('provider_source', 'N/A'))}")
    lines.append(f"- Transport source: {a(ep.get('transport_source', 'N/A'))}")
    lines.append("")

    lines.append("## Model Identity")
    lines.append("")
    mi = summary.get("model_identity", {})
    lines.append(f"- Resolved: {mi.get('resolved', False)}")
    lines.append(f"- Provider: {a(mi.get('provider', 'N/A'))}")
    lines.append(f"- Model alias: {a(mi.get('model_alias', 'N/A'))}")
    lines.append(f"- Model ID: {a(mi.get('model_id', 'N/A'))}")
    lines.append(f"- API surface: {a(mi.get('api_surface', 'N/A'))}")
    lines.append(f"- Supports reasoning: {mi.get('supports_reasoning', False)}")
    lines.append(f"- Supports structured output: {mi.get('supports_structured_output', False)}")
    lines.append("")

    lines.append("## Interpretation Admissibility")
    lines.append("")
    ia = summary.get("interpretation_admissibility", {})
    lines.append(f"- Provider metadata sufficient: {ia.get('provider_metadata_sufficient', False)}")
    lines.append(f"- Transport metadata sufficient: {ia.get('transport_metadata_sufficient', False)}")
    lines.append(f"- Model metadata sufficient: {ia.get('model_metadata_sufficient', False)}")
    lines.append(f"- Admissible: {ia.get('admissible', False)}")
    ia_lims = ia.get("limitations", [])
    if ia_lims:
        for lim in ia_lims:
            lines.append(f"  - Limitation: {lim}")
    else:
        lines.append("- Limitations: (none)")
    lines.append("")

    lines.append("## Evidence Contract")
    lines.append("")
    lines.append(f"- Contract version: {a(ec.get('contract_version', 'N/A'))}")
    lines.append(f"- Identity resolved: {ec.get('identity_resolved', False)}")
    lines.append(f"- Provenance recorded: {ec.get('provenance_recorded', False)}")
    lines.append(f"- Model identity resolved: {ec.get('model_identity_resolved', False)}")
    lines.append(f"- Interpretation admissible: {ec.get('interpretation_admissible', False)}")
    lines.append(f"- Scoring complete: {ec.get('scoring_complete', False)}")
    lines.append(f"- Decision: {decision}")
    ec_lims = ec.get("limitations", [])
    if ec_lims:
        for lim in ec_lims:
            lines.append(f"  - Limitation: {lim}")
    else:
        lines.append("- Limitations: (none)")
    lines.append("")

    lines.append("## Score Summary")
    lines.append("")
    lines.append(f"- Benchmark name: {a(summary.get('benchmark_name', 'N/A'))}")
    lines.append(f"- Dataset: {a(summary.get('dataset_name', 'N/A'))}")
    lines.append(f"- Dataset size: {a(summary.get('dataset_size', 'N/A'))}")
    lines.append(f"- Execution mode: {a(summary.get('execution_mode', 'N/A'))}")
    lines.append(f"- Provider mode: {a(summary.get('provider_mode', 'N/A'))}")
    lines.append(f"- Variants: {a(summary.get('variants', []))}")
    lines.append("")
    lines.append("### Scores by Variant")
    lines.append("")
    sbv = summary.get("scores_by_variant", {}) or {}
    if sbv:
        sorted_variants = sorted(sbv.keys())
        for variant in sorted_variants:
            data = sbv[variant]
            total = data.get("total_score", "N/A")
            pass_rate = data.get("pass_rate", "N/A")
            lines.append(f"- **{variant}**: total_score={total}, pass_rate={pass_rate}")
    else:
        lines.append("(no scores)")
    lines.append("")

    lines.append("## Final Interpretation")
    lines.append("")
    if decision == "INTERPRETABLE":
        lines.append(
            "This benchmark run is interpretable as evidence because execution identity, "
            "provenance, model identity, interpretation admissibility, and scoring completeness "
            "are all satisfied."
        )
    elif decision == "INTERPRETABLE_WITH_LIMITATIONS":
        lines.append(
            "This benchmark run may be interpreted with limitations. "
            "The limitations listed above must be disclosed when citing the result."
        )
    elif decision == "BLOCKED":
        lines.append(
            "This benchmark run should not be used as evidence for model or framework "
            "superiority because the evidence contract is blocked."
        )
    else:
        lines.append(f"Evidence contract decision is '{decision}'. Refer to limitations above.")

    lines.append("")
    return "\n".join(lines)


def _build_canonical_summary(
    results: list[TaskResult],
    config: BenchmarkConfig,
    scores: dict,
    excellence_decisions: dict[str, str],
    comparison_mode: bool = False,
) -> dict:
    total_tasks = len(load_dataset(config.dataset_path)) if config.max_samples is None else config.max_samples
    agents = sorted(set(r.agent_variant for r in results))
    category_breakdown = _compute_category_breakdown(results, config.dataset_path)
    commercial = _compute_commercial_metrics(results)
    metrics_by_variant = _compute_metrics_by_variant(results, scores)
    is_live = config.execution_mode == "live"
    identity = resolve_execution_identity(agents, config, results)
    providers = identity.providers
    transport = identity.transport
    blocked_variant_reasons = _blocked_variant_reasons(scores, excellence_decisions, results)
    blocked_variants = sorted(blocked_variant_reasons)
    is_deepseek = "deepseek" in providers
    is_openai = "openai" in providers

    models_by_variant: dict[str, str | None] = {}
    for r in results:
        if r.agent_variant not in models_by_variant:
            models_by_variant[r.agent_variant] = r.model

    provider_list_str = ", ".join(providers) if providers else config.provider or "unknown"
    model_str = config.model or (list(models_by_variant.values())[0] if models_by_variant else "unknown")

    summary: dict = {
        "benchmark_name": "Agentic Programming Reliability",
        "benchmark_version": "v0.1",
        "dataset_name": "Xendris Agentic Programming v0.1",
        "dataset_version": "0.1",
        "dataset_size": total_tasks,
        "execution_mode": config.execution_mode,
        "provider_mode": "real" if is_live else "mock",
        "variants": agents,
        "total_results": len(results),
        "scoring_formula": {
            "weighted_components": {
                "hidden_tests_pass": 0.35,
                "visible_tests_pass": 0.20,
                "api_contract_preserved": 0.15,
                "no_forbidden_files_touched": 0.10,
                "no_false_success_claim": 0.10,
                "minimal_patch": 0.05,
                "security_clean": 0.05,
            },
            "hard_penalties": {
                "critical_error": -1.0,
                "forbidden_file_touch": -0.5,
                "false_success_claim": -0.5,
            },
        },
        "scores_by_variant": scores,
        "deltas": _compute_deltas(scores),
        "metrics_by_variant": metrics_by_variant,
        "category_breakdown": category_breakdown,
        "commercial_metrics": commercial,
        "excellence_gate_decisions": excellence_decisions,
        "variant_gate_decisions": excellence_decisions,
        "blocked_variants": blocked_variants,
        "blocked_variant_reasons": blocked_variant_reasons,
        "comparison_mode": comparison_mode,
        "comparison_interpretation_scope": "Blocked variants are included for comparison only and are not admitted as positive evidence.",
        "no_universal_superiority_warning": "This benchmark evaluates Xendris variants against provider base models on specific closed dataset. No claim of universal superiority over any other model or agent framework is made or implied.",
        "no_general_coding_superiority_warning": "This benchmark is not evidence of general coding superiority. Results are limited to the closed Agentic Programming v0.1 dataset, providers, models, and configuration.",
        "evidence_interpretation": "Admitted as real-provider pilot evidence for Agentic Programming v0.1 only. Not admissible as evidence of general coding superiority, production readiness, or performance on open-ended programming tasks.",
    }

    if is_live:
        summary["providers"] = providers
        summary["transports"] = identity.transports
        summary["models_by_variant"] = models_by_variant
        summary["transport"] = transport
        summary["no_openrouter_used"] = True
        if config.credential_sources_by_provider:
            summary["credential_sources_by_provider"] = config.credential_sources_by_provider
        summary["cost_disclosure"] = "Cost estimates are based on token counts from API responses using published per-token pricing. Actual costs may vary."
        summary["latency_disclosure"] = "Latency is measured as wall-clock time for the API call to complete. Does not include sandbox test execution time."

    if is_live and is_deepseek and not is_openai:
        summary["provider"] = config.provider or "deepseek"
        summary["model"] = config.model or model_str
        summary["credential_source"] = config.credential_source or "env:DEEPSEEK_API_KEY"
    elif is_live and is_openai and not is_deepseek:
        summary["provider"] = config.provider or "openai"
        summary["model"] = config.model or model_str
        summary["credential_source"] = config.credential_source or "env:OPENAI_API_KEY"
    elif is_live and is_deepseek and is_openai:
        summary["provider"] = provider_list_str
        summary["model"] = model_str
        if config.credential_sources_by_provider:
            summary["credential_source"] = "provider_specific"

    if is_live:
        reported_models = sorted({r.provider_reported_model for r in results if r.provider_reported_model})
        if reported_models:
            summary["provider_reported_model"] = reported_models[0] if len(reported_models) == 1 else reported_models
        provider_names = ", ".join(p for p in providers) if providers else config.provider or "unknown"
        summary["limitations"] = [
            f"Execution mode is live: direct provider APIs were used ({provider_names}). Not OpenRouter.",
            "Dataset is closed synthetic (20 samples); does not represent real-world programming diversity.",
            "Results are specific to the Agentic Programming v0.1 benchmark and should not be generalized.",
            "Results do not transfer to OpenRouter or any other transport.",
            "Deterministic controls (oracle_agent, partial_agent, bad_agent) are reference baselines only, not evidence of real-provider performance.",
            "Cost/latency estimates depend on API response conditions and may not be reproducible.",
            "No comparison against Claude, Codex, Kimi, GLM, or any non-measured model is included. No superior generalization is claimed.",
            "Pre-existing fitz import error in test_master_goal_frontera_c_decision.py is unrelated and persists.",
        ]
    else:
        summary["limitations"] = [
            "Execution mode is dry-run: no real provider was called, no real model output was evaluated.",
            "Provider mode is mock: patches are generic stubs, not real agent output.",
            "These results are NOT evidence of real-provider agent programming performance.",
            "These results are NOT evidence of general programming superiority.",
            "These results are NOT evidence of production readiness.",
            "Dataset is closed synthetic (20 samples); does not represent real-world programming diversity.",
            "Pre-existing fitz import error in test_master_goal_frontera_c_decision.py is unrelated and persists.",
        ]

    if not is_live:
        summary["no_real_provider_performance_warning"] = "No real provider was called. All task results use mock/stub patches. Real-provider performance requires a separate live-mode run with provider credentials and real agent implementations."
        summary["no_universal_superiority_warning"] = "This dry-run does not compare against any other model or agent framework. No claim of universal superiority is made or implied."

    summary["benchmark_level_decision"] = _evaluate_benchmark_level_decision(summary, comparison_mode)

    summary.update({"execution_provenance": identity.execution_provenance})
    model_identity = _build_model_identity(config, providers, model_str)
    summary.update(model_identity)

    admissibility = evaluate_interpretation_admissibility(
        identity,
        model_identity.get("model_identity", {}),
        config.execution_mode,
    )
    summary["interpretation_admissibility"] = {
        "provider_metadata_sufficient": admissibility.provider_metadata_sufficient,
        "transport_metadata_sufficient": admissibility.transport_metadata_sufficient,
        "model_metadata_sufficient": admissibility.model_metadata_sufficient,
        "admissible": admissibility.admissible,
        "limitations": admissibility.limitations,
    }

    contract = build_evidence_contract(
        identity,
        model_identity.get("model_identity", {}),
        admissibility,
        summary,
        results,
        scores,
    )
    summary["evidence_contract"] = {
        "contract_version": contract.contract_version,
        "identity_resolved": contract.identity_resolved,
        "provenance_recorded": contract.provenance_recorded,
        "model_identity_resolved": contract.model_identity_resolved,
        "interpretation_admissible": contract.interpretation_admissible,
        "scoring_complete": contract.scoring_complete,
        "decision": contract.decision,
        "limitations": contract.limitations,
    }

    return summary


def _build_execution_provenance(
    agents: list[str],
    config: BenchmarkConfig,
    results: list[TaskResult],
    resolved_providers: list[str],
    resolved_transport: str | None,
) -> dict:
    identity = resolve_execution_identity(agents, config, results)
    return {"execution_provenance": identity.execution_provenance}


def _get_default_model_for_provider(provider: str) -> str:
    return DEFAULT_PROVIDER_MODELS.get(provider, "unknown")


def _build_provider_model_map(args: argparse.Namespace) -> dict[str, str] | None:
    if not args.provider_model:
        return None
    mapping: dict[str, str] = {}
    for entry in args.provider_model:
        if "=" not in entry:
            print(f"WARNING: --provider-model entries must be provider=model (got '{entry}')")
            continue
        provider, model = entry.split("=", 1)
        mapping[provider.strip()] = model.strip()
    return mapping or None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Xendris Agentic Programming Benchmark v0.1"
    )
    parser.add_argument(
        "--dataset-path",
        default="benchmarks/agentic_programming/v0_1",
        help="Path to benchmark dataset directory",
    )
    parser.add_argument(
        "--execution-mode",
        default="dry-run",
        choices=["dry-run", "live"],
        help="Execution mode (default: dry-run)",
    )
    valid_variants = [v.value for v in AgentVariant]
    parser.add_argument(
        "--agent-variants", "--variants",
        nargs="+",
        default=["base_agent", "xendris_agent", "xendris_calibrated_agent"],
        help="Agent variants to evaluate (space-separated or comma-separated)",
    )
    parser.add_argument(
        "--output-dir", "--outdir",
        default="benchmarks/agentic_programming/v0_1/output",
        help="Output directory for results",
        dest="output_dir",
    )
    parser.add_argument(
        "--agent-module",
        default="xendris.benchmarking.agentic_programming.agents",
        help="Python module path for agent implementations",
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=4,
        help="Maximum concurrent tasks per variant",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )
    parser.add_argument(
        "--provider",
        default=None,
        help="Provider name (e.g. deepseek)",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model name (e.g. deepseek-v4-flash). Ignored per-provider if --provider-model is set.",
    )
    parser.add_argument(
        "--provider-model",
        nargs="+",
        default=None,
        help="Per-provider model mapping: provider=model (e.g. deepseek=deepseek-v4-flash openai=gpt-4.1-mini)",
    )
    parser.add_argument(
        "--transport",
        default=None,
        choices=["direct"],
        help="Transport for live runs. This pilot supports direct only.",
    )
    parser.add_argument(
        "--budget-usd",
        type=float,
        default=None,
        help="Maximum budget in USD",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=None,
        help="Maximum number of samples to evaluate (for budget control)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum agent iterations per sample",
    )
    parser.add_argument(
        "--fail-on-gate-blockers",
        action="store_true",
        help="Exit with non-zero status if any variant is BLOCKED_FOR_INTERPRETATION",
    )
    parser.add_argument(
        "--task-suite",
        default=None,
        choices=["real_world_v0_2"],
        help="Task suite to run (e.g. real_world_v0_2 for repository-local tasks)",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Check credential discovery without running the benchmark",
    )
    parser.add_argument(
        "--comparison-mode",
        action="store_true",
        help="Allow blocked variants to remain in comparative artifacts without aborting if the benchmark-level decision is not blocked",
    )

    args = parser.parse_args()

    raw_variants: list[str] = []
    for item in args.agent_variants:
        raw_variants.extend(item.split(","))

    valid_variants = [v.value for v in AgentVariant]
    for v in raw_variants:
        if v not in valid_variants:
            print(f"Invalid variant '{v}'. Choose from: {valid_variants}")
            sys.exit(1)

    has_deepseek = any("deepseek" in v for v in raw_variants)
    has_openai = any("openai" in v for v in raw_variants)
    is_live = args.execution_mode == "live"
    explicit_provider = args.provider
    explicit_model = args.model

    provider_model_map = _build_provider_model_map(args)
    model_to_check = provider_model_map or {}
    if not model_to_check:
        if has_deepseek:
            model_to_check["deepseek"] = explicit_model or _get_default_model_for_provider("deepseek")
        if has_openai:
            model_to_check["openai"] = explicit_model or _get_default_model_for_provider("openai")

    credential_metadata_list: list[dict[str, object]] = []

    if is_live or (args.preflight_only and explicit_provider):
        providers_to_check: list[str] = []
        if has_deepseek:
            providers_to_check.append("deepseek")
        if has_openai:
            providers_to_check.append("openai")
        if args.preflight_only and explicit_provider and explicit_provider not in providers_to_check:
            providers_to_check.append(explicit_provider)

        for prov in providers_to_check:
            if prov == "deepseek":
                meta = load_deepseek_api_key_from_env_files()
                credential_metadata_list.append(meta)
            elif prov == "openai":
                meta = load_openai_api_key_from_env_files()
                credential_metadata_list.append(meta)

        if not providers_to_check:
            credential_metadata_list.append({
                "detected": False,
                "key_name": DEEPSEEK_KEY_NAME,
                "source": "missing",
                "credential_source": "missing",
            })
    else:
        credential_metadata_list.append({
            "detected": False,
            "key_name": DEEPSEEK_KEY_NAME,
            "source": "missing",
            "credential_source": "missing",
        })

    if args.preflight_only:
        success = True
        for meta in credential_metadata_list:
            provider = "deepseek" if meta["key_name"] == DEEPSEEK_KEY_NAME else "openai"
            detected = bool(meta["detected"])
            model_str = explicit_model or model_to_check.get(provider, _get_default_model_for_provider(provider))
            print(f"provider: {provider}")
            print("transport: direct")
            print(f"model: {model_str}")
            print(f"key_name: {meta['key_name']}")
            print(f"{meta['key_name']} detected: {str(detected).lower()}")
            print(f"  credential_source: {meta['credential_source']}")
            if not detected:
                success = False
        if success:
            return
        sys.exit(1)

    if is_live:
        if args.transport != "direct":
            print("ERROR: Live provider pilots require --transport direct.")
            sys.exit(1)
        for provider_key, provider_model_val in model_to_check.items():
            if provider_key == "deepseek" and provider_model_val != "deepseek-v4-flash":
                print(f"ERROR: DeepSeek model must be 'deepseek-v4-flash', got '{provider_model_val}'.")
                sys.exit(1)
            if provider_key == "openai" and not provider_model_val:
                print("ERROR: OpenAI requires a model (default: gpt-4.1-mini).")
                sys.exit(1)
        if has_deepseek and not get_deepseek_api_key():
            print("ERROR: Live DeepSeek direct variants require DEEPSEEK_API_KEY.")
            sys.exit(1)
        if has_openai and not get_openai_api_key():
            print("ERROR: Live OpenAI direct variants require OPENAI_API_KEY.")
            sys.exit(1)
        if args.budget_usd is not None:
            estimated_calls = len(raw_variants) * (args.max_samples or 20)
            estimated_cost = estimated_calls * 0.002
            if estimated_cost > args.budget_usd:
                print(f"ERROR: Estimated cost (${estimated_cost:.4f}) exceeds budget (${args.budget_usd:.2f}).")
                print("Reduce --max-samples or --variants, or increase --budget-usd.")
                sys.exit(1)

    transport = args.transport if is_live and (has_deepseek or has_openai or explicit_provider) else None

    credential_source_str = "; ".join(
        str(m.get("credential_source", "missing"))
        for m in credential_metadata_list
        if m.get("detected")
    ) or None
    credential_sources_by_provider: dict[str, str] = {}
    for meta in credential_metadata_list:
        if not meta.get("detected"):
            continue
        provider = "deepseek" if meta["key_name"] == DEEPSEEK_KEY_NAME else "openai"
        credential_sources_by_provider[provider] = str(meta.get("credential_source", "missing"))

    config = BenchmarkConfig(
        dataset_path=args.dataset_path,
        agent_variants=tuple(AgentVariant(v) for v in raw_variants),
        execution_mode=args.execution_mode,
        output_dir=args.output_dir,
        agent_module=args.agent_module,
        max_concurrent=args.max_concurrent,
        seed=args.seed,
        provider=args.provider or (",".join(sorted(model_to_check.keys())) if model_to_check else None),
        model=args.model,
        transport=transport,
        budget_usd=args.budget_usd,
        max_samples=args.max_samples,
        max_iterations=args.max_iterations,
        credential_source=credential_source_str,
        model_map=provider_model_map if provider_model_map else None,
        task_suite=args.task_suite,
    )

    print(f"Xendris Agentic Programming Benchmark")
    print(f"  Dataset: {config.dataset_path}")
    print(f"  Mode: {config.execution_mode}")
    print(f"  Task Suite: {config.task_suite or 'synthetic v0.1'}")
    print(f"  Variants: {[v.value for v in config.agent_variants]}")
    if provider_model_map:
        print(f"  Provider-Model Map: {provider_model_map}")
    elif args.provider:
        print(f"  Provider: {args.provider}")
    if args.model or provider_model_map:
        print(f"  Model: {args.model or 'per-provider'}")
    if transport:
        print(f"  Transport: {transport}")
    if args.budget_usd:
        print(f"  Budget: ${args.budget_usd:.2f}")
    if args.max_samples:
        print(f"  Max Samples: {args.max_samples}")
    if args.max_iterations:
        print(f"  Max Iterations: {args.max_iterations}")
    print()

    start = time.time()
    results = run_benchmark(config)
    elapsed = time.time() - start

    scores = compute_scores(results)
    excellence_decisions = evaluate_excellence_gate(scores)
    deltas = _compute_deltas(scores)

    os.makedirs(args.output_dir, exist_ok=True)

    jsonl_path = os.path.join(args.output_dir, "results.jsonl")
    export_to_jsonl(results, jsonl_path)
    print(f"Results exported to: {jsonl_path}")

    md_path = os.path.join(args.output_dir, "report.md")
    summary = _build_canonical_summary(results, config, scores, excellence_decisions, comparison_mode=args.comparison_mode)
    generate_markdown_report(scores, summary, excellence_decisions, md_path)
    print(f"Report written to: {md_path}")

    summary_path = os.path.join(args.output_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Summary exported to: {summary_path}")

    evidence_path = os.path.join(args.output_dir, "evidence_report.md")
    with open(evidence_path, "w", encoding="utf-8") as f:
        f.write(build_evidence_report_markdown(summary))
    print(f"Evidence report written to: {evidence_path}")

    print()
    print("=== Scores ===")
    for variant, data in scores.items():
        print(f"  {variant}: score={data['total_score']}, pass_rate={data['pass_rate']}")

    print()
    print("=== Deltas ===")
    for variant, delta in deltas.items():
        base_str = f", delta_vs_base={delta.get('delta_vs_base', 'N/A')}"
        print(f"  {variant}: distance_to_oracle={delta['distance_to_oracle']}{base_str}")

    print()
    print("=== Excellence Gate ===")
    for variant, decision in excellence_decisions.items():
        print(f"  {variant}: {decision}")

    print()
    print("=== Benchmark-Level Decision ===")
    print(f"  {summary.get('benchmark_level_decision')}")

    print()
    print(f"Completed in {elapsed:.2f}s")

    if args.fail_on_gate_blockers:
        blocked = [v for v, d in excellence_decisions.items() if d == "BLOCKED_FOR_INTERPRETATION"]
        if args.comparison_mode:
            if summary.get("benchmark_level_decision") == "BLOCKED_FOR_INTERPRETATION":
                print(f"\nERROR: --fail-on-gate-blockers: benchmark-level gate blocked. Blocked variants: {blocked}")
                sys.exit(1)
        elif blocked:
            print(f"\nERROR: --fail-on-gate-blockers: blocked variants: {blocked}")
            sys.exit(1)


if __name__ == "__main__":
    main()
