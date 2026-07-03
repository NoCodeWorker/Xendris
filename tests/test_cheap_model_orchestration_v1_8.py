"""
Tests v1.8 — Cheap Model Orchestration
"""

import pytest
import json
from phyng.copilot.schemas import HypothesisCardState
from phyng.copilot.orchestration import (
    compose_copilot_prompt_for_model,
    validate_model_structured_output,
    fallback_to_rule_based_question,
    orchestrate_model_assisted_response,
)


def test_model_output_never_authorizes_claim():
    # Model attempts to propose that the ladder level is SOURCE_BACKED_LIMITED,
    # but has_sources is False -> must be validation status "MODEL_OUTPUT_UNTRUSTED"
    # and ladder level reset to DREAM.
    proposal = {
        "clean_hypothesis": "Cleaned up text",
        "current_ladder_level": "SOURCE_BACKED_LIMITED",
        "claims_source_support": False
    }

    res = validate_model_structured_output(proposal, has_sources=False)
    assert res.validation_status in ("MODEL_OUTPUT_UNTRUSTED", "SOURCE_CLAIM_REJECTED")
    assert res.parsed_structured_output["current_ladder_level"] == "DREAM"


def test_rule_based_fallback_generates_question():
    card = HypothesisCardState(raw_idea="social sentiment leads BTC return")
    # Trigger fallback with empty or invalid model output
    res = orchestrate_model_assisted_response(
        user_message="sentiment and BTC",
        hypothesis_card=card,
        mode="HYPOTHESIS_MODE",
        risk_level="RISK_2_INTERNAL_RESEARCH",
        model_raw_response=None,  # triggers fallback
        has_sources=False
    )

    assert res.validation_status == "VALIDATED"
    assert "next_best_question" in res.parsed_structured_output
    q = res.parsed_structured_output["next_best_question"]
    assert q["question_type"] == "CLARIFY_TERM"
