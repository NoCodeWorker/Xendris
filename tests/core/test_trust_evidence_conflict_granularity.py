from xendris.core.trust import evaluate_reasoning_transversally


def test_contradictory_evidence_does_not_allow_automatic_scoring():
    result = evaluate_reasoning_transversally(
        "La fuente A dice 9.81 y la fuente B dice 9.49. Conflicto de datos.",
        [{"text": "Fuentes contradictorias.", "origin_type": "INFERRED", "support_status": "PARTIALLY_SUPPORTED"}],
    )

    assert result["decision"] == "HUMAN_REVIEW_REQUIRED"
    assert result["reason"] == "EVIDENCE_CONFLICT"


def test_partially_supported_claim_is_not_fully_verified():
    result = evaluate_reasoning_transversally(
        "El claim está parcialmente soportado por el paper, pero hay ambigüedad no resuelta.",
        [{"text": "Claim parcialmente soportado.", "origin_type": "INFERRED", "support_status": "VERIFIED"}],
    )

    assert result["decision"] == "HUMAN_REVIEW_REQUIRED"
    assert result["reason"] == "HUMAN_REVIEW_POLICY"
    assert result["claims"][0]["support_status"] == "PARTIALLY_SUPPORTED"


def test_claim_stronger_than_evidence_is_claim_overreach():
    result = evaluate_reasoning_transversally(
        "La conclusión es más fuerte que la evidencia disponible.",
        [{"text": "Conclusión más fuerte que evidencia.", "origin_type": "INFERRED", "support_status": "PARTIALLY_SUPPORTED"}],
    )

    assert result["decision"] == "EXCLUDE_FROM_SCORING"
    assert result["reason"] == "CLAIM_OVERREACH"


def test_missing_source_is_insufficient_evidence():
    result = evaluate_reasoning_transversally(
        "La afirmación se presenta sin fuentes ni validación.",
        [{"text": "Afirmación sin fuentes.", "origin_type": "FACTUAL", "support_status": "VERIFIED"}],
    )

    assert result["decision"] == "EXCLUDE_FROM_SCORING"
    assert result["reason"] == "INSUFFICIENT_EVIDENCE"


def test_human_review_only_for_real_unresolved_conflict():
    result = evaluate_reasoning_transversally(
        "La inferencia es altamente plausible, pero no hay demostración empírica sólida.",
        [{"text": "Inferencia plausible sin demostración.", "origin_type": "INFERRED", "support_status": "PARTIALLY_SUPPORTED"}],
    )

    assert result["decision"] == "HUMAN_REVIEW_REQUIRED"
    assert result["reason"] == "HUMAN_REVIEW_POLICY"


def test_deterministic_exclusion_does_not_escalate_to_human_review():
    result = evaluate_reasoning_transversally(
        "Timeout con ambigüedad no resuelta.",
        [],
        {"timeout": True, "has_unresolved_ambiguity": True},
    )

    assert result["decision"] == "EXCLUDE_FROM_SCORING"
    assert result["reason"] == "TIMEOUT"
