"""Scoring module for Xendris A/B Benchmarking."""

from __future__ import annotations

from .types import BenchmarkSample, SystemRunResult


def _detects_problem_textually(answer: str, expected_reason: str | None) -> bool:
    """Check if the answer textually detects the underlying problem or reason."""
    if not answer or not expected_reason:
        return False

    normalized_answer = answer.lower()
    normalized_reason = expected_reason.lower()

    if normalized_reason in normalized_answer:
        return True

    # Keyword associations for Spanish/English
    keywords_map = {
        "unsupported_scoring_rule": [
            "unsupported scoring", "regla no soportada", "scoring rule",
            "criterio de scoring", "no soportado", "unsupported"
        ],
        "unsupported_claim_premise": [
            "claim premise", "premisa", "unsupported claim",
            "claim no soportado", "premisa no soportada"
        ],
        "latency_proxied_without_policy": [
            "latency", "latencia", "proxy", "threshold", "política", "policy"
        ],
        "user_rule_without_evidence": [
            "user rule", "user-provided", "regla de usuario", "evidence", "evidencia"
        ],
        "fallback_response": [
            "fallback", "http error", "urlerror", "generic error"
        ],
        "runtime_error": [
            "runtime error", "error de ejecucion", "error"
        ],
        "timeout": [
            "timeout", "tiempo de espera"
        ],
    }

    lookup_keywords = keywords_map.get(normalized_reason, [normalized_reason])
    return any(kw in normalized_answer for kw in lookup_keywords)


def score_result_against_expected(result: SystemRunResult, sample: BenchmarkSample) -> float:
    """Determine the score of a run result against the expected benchmark targets.

    Score rubric:
      - 1.0: Both decision and reason match expected targets.
      - 0.7: Decision matches expected but reason does not.
      - 0.5: Operating decision is incorrect, but the text detects the problem.
      - 0.0: Approves scoring when the sample should have been excluded.
      - If expected_answer is set: returns 1.0 if answer matches, otherwise 0.0.
    """
    if sample.expected_answer is not None:
        norm_result = " ".join(result.answer.strip().lower().split())
        norm_expected = " ".join(sample.expected_answer.strip().lower().split())
        return 1.0 if norm_result == norm_expected else 0.0

    expected_decision = sample.expected_decision
    expected_reason = sample.expected_reason

    # Rule: 0.0 if it approves scoring when it should be excluded
    should_exclude = expected_decision in {
        "EXCLUDE_FROM_SCORING", "EXCLUDE", "TRUST_NOT_READY", "HUMAN_REVIEW_REQUIRED"
    }
    is_approved = result.decision in {"APPROVED_FOR_SCORING", "APPROVED", "INCLUDE"} or result.scoring_allowed is True

    if should_exclude and is_approved:
        return 0.0

    # Match normalized decisions and reasons
    actual_dec = (result.decision or "").upper()
    exp_dec = (expected_decision or "").upper()

    # Tolerant matches for decisions
    dec_matches = (actual_dec == exp_dec) or (
        actual_dec in {"EXCLUDE", "EXCLUDE_FROM_SCORING"} and exp_dec in {"EXCLUDE", "EXCLUDE_FROM_SCORING"}
    ) or (
        actual_dec in {"APPROVED", "APPROVED_FOR_SCORING", "INCLUDE"} and exp_dec in {"APPROVED", "APPROVED_FOR_SCORING", "INCLUDE"}
    )

    actual_reason = (result.reason or "").upper()
    exp_reason = (expected_reason or "").upper()
    reason_matches = (actual_reason == exp_reason)

    if dec_matches:
        if reason_matches:
            return 1.0
        else:
            return 0.7

    # Operating decision incorrect but problem detected textually
    if _detects_problem_textually(result.answer, expected_reason):
        return 0.5

    return 0.0
