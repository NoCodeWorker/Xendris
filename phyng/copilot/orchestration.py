"""
Phygn v1.8 — Cheap Model Orchestration

Implements the orchestration protocol hooks to safely leverage cheap/open-source models.
Enforces that model outputs are treated as proposals, while Phygn determines permissions.
"""

from __future__ import annotations

import json
from typing import Any
from phyng.copilot.schemas import ModelOrchestrationResult, NextBestQuestion, HypothesisCardState
from phyng.copilot.question_engine import generate_next_best_question


def compose_copilot_prompt_for_model(
    user_message: str,
    hypothesis_card: HypothesisCardState | None,
    mode: str,
) -> str:
    """Compose the LLM prompt, instructing the model to propose structures and language."""
    card_info = json.dumps(hypothesis_card.model_dump()) if hypothesis_card else "None"
    return f"""Task: Assist the user in refining their hypothesis.
Current Mode: {mode}
Current Hypothesis Card: {card_info}
User Message: {user_message}

Instructions:
1. Paraphrase the user's idea.
2. Suggest candidate variables, observables, and proxies.
3. Keep claims grounded. Do not claim truth.
"""


def validate_model_structured_output(
    structured_output: dict[str, Any],
    has_sources: bool = False,
) -> ModelOrchestrationResult:
    """
    Validate the model's structured proposals.
    Rule: invalid model output cannot elevate claims; source hallucination is rejected.
    """
    notes = []
    status = "VALIDATED"

    # 1. Check for hallucinated source / benchmark claim
    if structured_output.get("claims_source_support") and not has_sources:
        status = "SOURCE_CLAIM_REJECTED"
        notes.append("Rejected: model claimed source support but no sources were verified.")
        # Strip out any elevated claim levels from the model
        structured_output["current_ladder_level"] = "DREAM"

    # 2. Check for invalid structure or overclaiming status
    elif structured_output.get("current_ladder_level") in ("SOURCE_BACKED_LIMITED", "BENCHMARK_SUPPORTED", "OPERATIONALLY_ACTIONABLE", "AUTOMATED_EXECUTION_ALLOWED") and not has_sources:
        status = "MODEL_OUTPUT_UNTRUSTED"
        notes.append("Untrusted: model proposed high ladder level without source verification.")
        structured_output["current_ladder_level"] = "DREAM"

    # 3. Basic formatting verification
    elif "clean_hypothesis" not in structured_output:
        status = "MODEL_OUTPUT_UNTRUSTED"
        notes.append("Untrusted: missing clean_hypothesis field in model output.")

    return ModelOrchestrationResult(
        raw_response=json.dumps(structured_output),
        parsed_structured_output=structured_output,
        validation_status=status,
        validation_notes=notes
    )


def fallback_to_rule_based_question(
    input_text: str,
    hypothesis_card: HypothesisCardState | None,
    mode: str,
    risk_level: str,
) -> NextBestQuestion:
    """Fallback to deterministic Socratic Engine question if model fails or outputs invalid structure."""
    return generate_next_best_question(input_text, hypothesis_card, mode, risk_level)


def orchestrate_model_assisted_response(
    user_message: str,
    hypothesis_card: HypothesisCardState | None,
    mode: str,
    risk_level: str,
    model_raw_response: str | None = None,
    has_sources: bool = False,
) -> ModelOrchestrationResult:
    """
    Orchestrate the response generation using the LLM output if valid, or falling back to rule-based verification.
    """
    if not model_raw_response:
        # Fallback case immediately
        fallback_q = fallback_to_rule_based_question(user_message, hypothesis_card, mode, risk_level)
        return ModelOrchestrationResult(
            raw_response="Fallback triggered",
            parsed_structured_output={
                "clean_hypothesis": user_message,
                "next_best_question": fallback_q.model_dump()
            },
            validation_status="VALIDATED",
            validation_notes=["Triggered fallback directly due to empty model response."]
        )

    # Attempt to parse json
    try:
        data = json.loads(model_raw_response)
    except json.JSONDecodeError:
        fallback_q = fallback_to_rule_based_question(user_message, hypothesis_card, mode, risk_level)
        return ModelOrchestrationResult(
            raw_response=model_raw_response,
            parsed_structured_output={
                "clean_hypothesis": user_message,
                "next_best_question": fallback_q.model_dump()
            },
            validation_status="MODEL_OUTPUT_UNTRUSTED",
            validation_notes=["JSON decode failed. Used rule-based fallback question."]
        )

    return validate_model_structured_output(data, has_sources=has_sources)
