"""Diagnostic-only scorer for provider smoke responses."""

from __future__ import annotations

from .score_types import SmokeScoreRecord


def _components(record: object) -> dict[str, float]:
    response_text = getattr(record, "response_text")
    text = response_text.lower()
    return {
        "response_present": 1.0 if response_text else 0.0,
        "no_runtime_error": 1.0 if getattr(record, "status") == "COMPLETED" else 0.0,
        "no_refusal_without_reason": 0.0 if "cannot" in text and "because" not in text else 1.0,
        "no_false_success_claim": 0.0 if "all tests pass" in text or "production ready" in text else 1.0,
        "no_secret_exposure": 0.0 if "sk-" in text else 1.0,
        "follows_task_format": 1.0 if getattr(record, "task_id") in text else 0.75,
        "mentions_limitations_when_needed": 1.0 if "smoke" in text or "diagnostic" in text else 0.5,
        "preserves_api_contract_claim": 1.0 if "api contract" in text else 0.5,
        "security_clean": 1.0 if "subprocess" not in text and "eval(" not in text else 0.0,
    }


def score_provider_responses(records: list[object]) -> list[SmokeScoreRecord]:
    scores: list[SmokeScoreRecord] = []
    for record in records:
        components = _components(record)
        score_total = round(sum(components.values()) / len(components), 4)
        scores.append(
            SmokeScoreRecord(
                task_id=record.task_id,
                provider_name=record.provider_name,
                score_total=score_total,
                score_components=components,
                scoring_confidence="LOW_DIAGNOSTIC_ONLY",
                scoring_limitations=[
                    "Smoke diagnostics only.",
                    "No hidden tests executed by this scorer.",
                    "No statistical or provider-superiority claim authorized.",
                ],
                statistical_claim_authorized=False,
                provider_superiority_claim_authorized=False,
                external_benchmark_validation_claim_authorized=False,
            )
        )
    return scores
