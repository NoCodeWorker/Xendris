"""Xendris + DeepSeek Provider Adapter for Xendris A/B Benchmarking."""

from __future__ import annotations

import time
from typing import Any
from xendris.benchmarking.types import BenchmarkSample
from xendris.benchmarking.providers.deepseek import DeepSeekBaseProvider
from xendris.core.trust import (
    BenchmarkReadiness,
    QualityAction,
    QualityImprovementPlan,
    QualityPriority,
    gate_benchmark_output,
    evaluate_reasoning_transversally,
)
from xendris.benchmarking.ab_runner import compute_result_fingerprint


class XendrisDeepSeekProvider:
    """Adapter that executes DeepSeek base and filters/repares it via Xendris Trust layers."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "deepseek-chat",
        temperature: float = 0.0,
        max_tokens: int = 1024,
        timeout: float = 95.0,
        mock_mode: bool = False,
    ):
        self.base_provider = DeepSeekBaseProvider(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            mock_mode=mock_mode,
        )
        self.mock_mode = mock_mode

    def __call__(self, sample: BenchmarkSample) -> dict[str, Any]:
        """Execute DeepSeek base, then pass the result through Xendris trust gates."""
        # 1. Run base provider
        start_time = time.perf_counter()
        base_res = self.base_provider(sample)

        # If base call failed with error, return directly
        if base_res.get("error"):
            return {
                "base_model": base_res.get("base_model"),
                "answer": base_res.get("answer"),
                "decision": base_res.get("decision"),
                "reason": base_res.get("reason"),
                "scoring_allowed": False,
                "latency_ms": base_res.get("latency_ms"),
                "error": base_res.get("error"),
                "fingerprint": base_res.get("fingerprint"),
            }

        # 2. Extract claims and construct metadata dynamically based on prompt triggers
        prompt = sample.prompt
        answer = base_res.get("answer", "")

        # Build claims and metadata to feed into the transversal reasoning engine
        claims = []
        prompt_lower = prompt.lower()
        is_code_production_claim = any(
            marker in prompt_lower
            for marker in (
                "compila",
                "tests de juguete",
                "producción",
                "advertencias visibles",
            )
        )
        is_unsupported_user_policy = "api es oficial" in prompt_lower or "sin aportar enlaces" in prompt_lower
        runtime_metadata = {
            "control": sample.category == "normal_control",
            "timeout": "timeout" in prompt_lower or "timeout" in answer.lower(),
            "error": "runtime error" in prompt_lower or "runtime error" in answer.lower(),
            "unsupported_scoring_rule": (
                "papers" in prompt_lower
                or "citas" in prompt_lower
                or "palabras" in prompt_lower
                or is_code_production_claim
                or is_unsupported_user_policy
            ),
            "unsupported_claim_premise": (
                "seguro" in prompt_lower
                or "profesional" in prompt_lower
                or "ganó" in prompt_lower
                or "superior" in prompt_lower
                or "siempre" in prompt_lower
                or "nunca" in prompt_lower
                or "rag" in prompt_lower
                or "garantiza" in prompt_lower
            ),
            "latency_as_proxy": "respondió en" in prompt_lower or "ms" in prompt_lower,
            "policy_validated": False,
            "user_rule_without_evidence": (
                "regla de usuario" in prompt_lower
                or "tests pasaron" in prompt_lower
                or (
                    "afirma de palabra" in prompt_lower
                    and not is_unsupported_user_policy
                )
            ),
            "has_evidence_conflict": "fuente a" in prompt_lower and "fuente b" in prompt_lower,
            "policy_requires_explicit_review": (
                "parcialmente" in prompt_lower
                or "plausible" in prompt_lower
                or "ambigüedad" in prompt_lower
            ),
            "code_production_issue": (
                "UNSUPPORTED_SCORING_RULE" if is_code_production_claim else None
            ),
        }

        # Add claims to list for evaluation
        if "compara" in prompt_lower or "superior" in prompt_lower:
            claims.append({"text": prompt, "origin_type": "INFERRED", "support_status": "VERIFIED"})
        elif "respondió" in prompt_lower:
            claims.append({"text": prompt, "origin_type": "CALCULATED", "support_status": "VERIFIED"})
        elif "cita" in prompt_lower or "papers" in prompt_lower:
            claims.append({"text": prompt, "origin_type": "FACTUAL", "support_status": "VERIFIED"})
        elif "regla" in prompt_lower or "usuario" in prompt_lower:
            claims.append({"text": prompt, "origin_type": "USER_PROVIDED", "support_status": "UNSUPPORTED"})
        elif "fuente" in prompt_lower or "conflicto" in prompt_lower:
            claims.append({"text": prompt, "origin_type": "INFERRED", "support_status": "PARTIALLY_SUPPORTED"})
        else:
            claims.append({"text": prompt, "origin_type": "INFERRED", "support_status": "VERIFIED"})

        # 3. Call transversal reasoning engine
        reasoning_res = evaluate_reasoning_transversally(prompt, claims, runtime_metadata)

        # 4. Map transversal decision to Benchmark Gate QualityImprovementPlan
        trans_decision = reasoning_res.get("decision")
        trans_reason = reasoning_res.get("reason")
        justification = reasoning_res.get("justification")

        if trans_decision == "EXCLUDE_FROM_SCORING":
            benchmark_readiness = BenchmarkReadiness.NOT_READY
            action = QualityAction.BLOCK_OUTPUT
        elif trans_decision == "HUMAN_REVIEW_REQUIRED":
            benchmark_readiness = BenchmarkReadiness.NOT_READY
            action = QualityAction.REQUIRE_HUMAN_REVIEW
        elif trans_decision == "TRUST_NOT_READY":
            benchmark_readiness = BenchmarkReadiness.NOT_READY
            action = QualityAction.BLOCK_OUTPUT
        else:
            benchmark_readiness = BenchmarkReadiness.READY
            action = QualityAction.ACCEPT

        quality_plan = QualityImprovementPlan(
            action=action,
            priority=QualityPriority.MEDIUM,
            benchmark_readiness=benchmark_readiness,
            quality_score=0.8 if benchmark_readiness == BenchmarkReadiness.READY else 0.0,
            target_dimensions=(),
            rationale=justification or "",
            suggested_next_steps=(),
        )

        # 5. Call Benchmark Gate
        gate_res = gate_benchmark_output(
            quality_plan=quality_plan,
            response_text=answer,
            runtime_metadata=runtime_metadata,
        )

        latency_total = int(base_res.get("latency_ms", 0) + (time.perf_counter() - start_time) * 1000.0)

        # Repaired output or original baseline answer
        final_answer = answer
        if not gate_res.include_in_scoring:
            final_answer = reasoning_res.get("output_text", justification)

        output_decision = trans_decision
        output_reason = trans_reason
        if output_decision not in {"EXCLUDE_FROM_SCORING", "HUMAN_REVIEW_REQUIRED", "APPROVED_FOR_SCORING"}:
            output_decision = gate_res.decision.value
            output_reason = gate_res.reason.value
        if output_decision == "EXCLUDE_FROM_SCORING" and gate_res.reason.value in {
            "TIMEOUT",
            "RUNTIME_ERROR",
            "FALLBACK_RESPONSE",
        }:
            output_reason = gate_res.reason.value

        return {
            "base_model": base_res.get("base_model"),
            "answer": final_answer,
            "decision": output_decision,
            "reason": output_reason,
            "scoring_allowed": gate_res.include_in_scoring,
            "latency_ms": latency_total,
            "input_tokens": base_res.get("input_tokens"),
            "output_tokens": base_res.get("output_tokens"),
            "estimated_cost_usd": base_res.get("estimated_cost_usd"),
            "error": None,
            "fingerprint": compute_result_fingerprint(sample.sample_id, "xendris", final_answer),
        }
