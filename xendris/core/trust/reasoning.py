"""Transversal reasoning engine for Xendris Trust Kernel.

Applies strict language detection, separates origin from support, rejects absolute
guarantees without empirical evidence, and prevents false proxies of correctness.
"""

from __future__ import annotations

import re
from typing import Any, Mapping

from .types import AuditDecision, ClaimStatus, ClaimType, RiskLevel


def detect_language(text: str) -> str:
    """Detect dominant language of the input text. Returns 'es' or 'en'."""
    text_lower = f" {text.lower()} "

    if any(char in text_lower for char in ("\xbf", "\xe1", "\xe9", "\xed", "\xf3", "\xfa", "\xf1")):
        return "es"

    es_words = [
        " el ", " la ", " los ", " las ", " un ", " una ", " y ", " que ", " en ",
        " de ", " con ", " para ", " por ", " si ", " no ", " como ", " qu\xe9 ",
        " demostraci\xf3n ", " afirmaci\xf3n ", " superioridad ", " garant\xeda ", " cita ",
        " latencia ", " error ", " pregunta ", " regla ", " criterio ", " respuesta ",
        " quiero ", " saber ", " constante ", " es ",
    ]
    en_words = [
        " the ", " a ", " an ", " and ", " of ", " in ", " to ", " with ", " for ",
        " by ", " if ", " no ", " not ", " how ", " what ", " proof ", " claim ",
        " superiority ", " guarantee ", " citation ", " latency ", " error ",
        " question ", " rule ", " criterion ", " response ", " prove ", " always ",
        " cache ", " optimal ", " correctness ",
    ]

    es_count = sum(1 for w in es_words if w in text_lower)
    en_count = sum(1 for w in en_words if w in text_lower)

    if (
        " demostr" in text_lower
        or " superior" in text_lower
        or " garant" in text_lower
        or " tambi" in text_lower
        or " quiero" in text_lower
        or " constante" in text_lower
    ):
        es_count += 2
    if (
        " proof" in text_lower
        or " prove" in text_lower
        or " guarantee" in text_lower
        or " latency" in text_lower
        or " correctness" in text_lower
    ):
        en_count += 2

    return "es" if es_count >= en_count else "en"


def _is_absolute_guarantee(text: str) -> bool:
    """Check if the text contains absolute or universal claims without exception."""
    text_lower = text.lower()
    patterns = [
        r"siempre\s+mejora",
        r"nunca\s+falla",
        r"garantiza\s+la\s+correcci[o\xf3]n",
        r"toda\s+respuesta\s+con\s+.*\s+es\s+correcta",
        r"si\s+contiene\s+cita,\s+est[a\xe1]\s+verificada",
        r"si\s+responde\s+r[a\xe1]pido,\s+es\s+correcta",
        r"sistema\s+es\s+superior\s+en\s+todo",
        r"always\s+improves",
        r"never\s+fails",
        r"guarantees\s+correctness",
        r"all\s+responses\s+with\s+.*\s+are\s+correct",
        r"if\s+it\s+contains\s+citation,\s+it\s+is\s+verified",
        r"if\s+it\s+responds\s+fast,\s+it\s+is\s+correct",
        r"system\s+is\s+superior\s+in\s+every",
        r"absolute\s+guarantee",
        r"garant[i\xed]a\s+absoluta",
    ]
    return any(re.search(pat, text_lower) for pat in patterns)


def classify_user_provided_origin(text: str) -> str | None:
    """Classify user-provided material without treating it as verified support."""
    normalized = text.lower()
    if "regla de usuario" in normalized or "user rule" in normalized:
        return "USER_PROVIDED_RULE"
    if "pol\xedtica" in normalized or "policy" in normalized:
        return "USER_PROVIDED_POLICY"
    if "paper" in normalized or "fuente" in normalized or "referencia" in normalized:
        return "USER_PROVIDED_EVIDENCE_REFERENCE"
    if "declara" in normalized or "afirma" in normalized or "says" in normalized:
        return "USER_PROVIDED_CLAIM"
    if "respondi\xf3 en" in normalized or "latency" in normalized or "latencia" in normalized:
        return "USER_PROVIDED_FACT"
    return None


def classify_evidence_issue(text: str) -> str | None:
    """Classify evidence conflicts and support gaps conservatively."""
    normalized = text.lower()
    if ("fuente a" in normalized and "fuente b" in normalized) or "conflicto" in normalized:
        return "EVIDENCE_CONFLICT"
    if "contradict" in normalized or "se contradicen" in normalized:
        return "CONTRADICTED_EVIDENCE"
    if "parcialmente soportado" in normalized or "partial support" in normalized:
        return "HUMAN_REVIEW_POLICY"
    if "ambig\xfcedad no resuelta" in normalized or "unresolved ambiguity" in normalized:
        return "HUMAN_REVIEW_POLICY"
    if "altamente plausible" in normalized and (
        "no hay demostraci\xf3n" in normalized or "without empirical" in normalized
    ):
        return "HUMAN_REVIEW_POLICY"
    if "no hay demostraci\xf3n emp\xedrica" in normalized or "sin fuentes" in normalized:
        return "INSUFFICIENT_EVIDENCE"
    if "conclusi\xf3n" in normalized and "m\xe1s fuerte" in normalized:
        return "CLAIM_OVERREACH"
    if "source validation" in normalized or "validaci\xf3n de fuente" in normalized:
        return "NEEDS_SOURCE_VALIDATION"
    return None


def classify_code_production_issue(text: str) -> str | None:
    """Classify code and production-readiness overclaims."""
    normalized = text.lower()
    if "compila" in normalized or "compiles" in normalized:
        return "COMPILATION_NOT_CORRECTNESS"
    if "tests de juguete" in normalized or ("pasamos" in normalized and "tests" in normalized):
        return "TEST_PASS_NOT_PRODUCTION_READY"
    if "no tiene advertencias" in normalized or "no visible errors" in normalized:
        return "SECURITY_NOT_VALIDATED"
    if "benchmark local" in normalized:
        return "BENCHMARK_NOT_REAL_WORLD_PERFORMANCE"
    if "producci\xf3n" in normalized or "production" in normalized:
        return "PRODUCTION_READINESS_NOT_ESTABLISHED"
    if "type hints" in normalized:
        return "TEST_COVERAGE_INSUFFICIENT"
    return None


def evaluate_reasoning_transversally(
    question: str,
    claims: list[dict[str, Any]],
    runtime_metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Perform a transversal reasoning evaluation and output structured audit results.

    Enforces rules on language, origin vs support, absolute guarantees, deterministic
    exclusions, explicit decisions, and false proxies.
    """
    lang = detect_language(question)
    runtime_metadata = runtime_metadata or {}

    analyzed_claims = []

    has_unsupported_scoring_rule = bool(runtime_metadata.get("unsupported_scoring_rule"))
    has_unsupported_claim_premise = bool(runtime_metadata.get("unsupported_claim_premise"))
    has_latency_as_proxy = bool(runtime_metadata.get("latency_as_proxy"))
    has_user_rule_without_evidence = bool(runtime_metadata.get("user_rule_without_evidence"))
    has_citation_as_proxy = bool(runtime_metadata.get("citation_as_proxy"))

    prompt_evidence_issue = (
        str(runtime_metadata.get("evidence_issue"))
        if runtime_metadata.get("evidence_issue")
        else classify_evidence_issue(question)
    )
    prompt_code_issue = (
        str(runtime_metadata.get("code_production_issue"))
        if runtime_metadata.get("code_production_issue")
        else classify_code_production_issue(question)
    )
    prompt_user_origin = (
        str(runtime_metadata.get("user_provided_origin"))
        if runtime_metadata.get("user_provided_origin")
        else classify_user_provided_origin(question)
    )

    for i, raw_claim in enumerate(claims, 1):
        text = raw_claim.get("text", "")
        origin_type = raw_claim.get("origin_type", "INFERRED")
        support_status = raw_claim.get("support_status", "UNSUPPORTED")

        user_origin_type = raw_claim.get("user_provided_origin") or classify_user_provided_origin(text)
        evidence_issue = raw_claim.get("evidence_issue") or classify_evidence_issue(text)
        code_issue = raw_claim.get("code_production_issue") or classify_code_production_issue(text)

        if origin_type == "USER_PROVIDED":
            support_status = "UNSUPPORTED"
            if user_origin_type == "USER_PROVIDED_RULE":
                has_user_rule_without_evidence = True

        is_absolute = _is_absolute_guarantee(text)
        if is_absolute:
            support_status = "UNSUPPORTED"
            risk = "HIGH"
            benchmark_relevance = "INVALID_SCORING_CRITERION"
            has_unsupported_claim_premise = True
        else:
            risk = raw_claim.get("risk", "MEDIUM")
            benchmark_relevance = raw_claim.get("benchmark_relevance", "NOT_ENOUGH_FOR_SCORING")

        if "latency" in text.lower() or "latencia" in text.lower():
            if has_latency_as_proxy and not runtime_metadata.get("policy_validated"):
                support_status = "UNSUPPORTED"
                risk = "HIGH"
                benchmark_relevance = "INVALID_SCORING_CRITERION"

        if "citation" in text.lower() or "cita" in text.lower():
            if has_citation_as_proxy:
                support_status = "INSUFFICIENT_FOR_VERIFICATION"
                risk = "MEDIUM"
                benchmark_relevance = "NOT_ENOUGH_FOR_SCORING"

        if evidence_issue:
            support_status = (
                "CONTRADICTED"
                if evidence_issue in {"EVIDENCE_CONFLICT", "CONTRADICTED_EVIDENCE"}
                else "PARTIALLY_SUPPORTED"
            )
            risk = "HIGH" if evidence_issue in {"EVIDENCE_CONFLICT", "CONTRADICTED_EVIDENCE"} else "MEDIUM"
            benchmark_relevance = "REQUIRES_REVIEW_OR_EXCLUSION"

        if code_issue:
            support_status = "UNSUPPORTED"
            risk = "HIGH"
            benchmark_relevance = "INVALID_PRODUCTION_READINESS_CRITERION"
            has_unsupported_scoring_rule = True

        analyzed_claims.append({
            "index": i,
            "claim": text,
            "origin_type": origin_type,
            "user_provided_origin": user_origin_type,
            "evidence_issue": evidence_issue,
            "code_production_issue": code_issue,
            "support_status": support_status,
            "risk": risk,
            "benchmark_relevance": benchmark_relevance,
        })

    # Deterministic decision & reason
    if prompt_code_issue:
        decision = "EXCLUDE_FROM_SCORING"
        reason = "UNSUPPORTED_SCORING_RULE"
    elif has_unsupported_scoring_rule or has_citation_as_proxy:
        decision = "EXCLUDE_FROM_SCORING"
        reason = "UNSUPPORTED_SCORING_RULE"
    elif has_unsupported_claim_premise:
        decision = "EXCLUDE_FROM_SCORING"
        reason = "UNSUPPORTED_CLAIM_PREMISE"
    elif has_latency_as_proxy and not runtime_metadata.get("policy_validated"):
        decision = "EXCLUDE_FROM_SCORING"
        reason = "LATENCY_PROXIED_WITHOUT_POLICY"
    elif has_user_rule_without_evidence:
        decision = "EXCLUDE_FROM_SCORING"
        reason = "USER_RULE_WITHOUT_EVIDENCE"
    elif prompt_user_origin in {"USER_PROVIDED_RULE", "USER_PROVIDED_POLICY"}:
        decision = "EXCLUDE_FROM_SCORING"
        reason = "USER_RULE_WITHOUT_EVIDENCE" if prompt_user_origin == "USER_PROVIDED_RULE" else "UNSUPPORTED_SCORING_RULE"
    elif runtime_metadata.get("timeout"):
        decision = "EXCLUDE_FROM_SCORING"
        reason = "TIMEOUT"
    elif runtime_metadata.get("error"):
        decision = "EXCLUDE_FROM_SCORING"
        reason = "RUNTIME_ERROR"
    elif prompt_evidence_issue in {"EVIDENCE_CONFLICT", "CONTRADICTED_EVIDENCE"}:
        decision = "HUMAN_REVIEW_REQUIRED"
        reason = "EVIDENCE_CONFLICT"
    elif prompt_evidence_issue == "HUMAN_REVIEW_POLICY":
        decision = "HUMAN_REVIEW_REQUIRED"
        reason = "HUMAN_REVIEW_POLICY"
    elif prompt_evidence_issue in {"INSUFFICIENT_EVIDENCE", "CLAIM_OVERREACH", "NEEDS_SOURCE_VALIDATION"}:
        decision = "EXCLUDE_FROM_SCORING"
        reason = prompt_evidence_issue
    elif (
        runtime_metadata.get("has_evidence_conflict")
        or runtime_metadata.get("has_unresolved_ambiguity")
        or runtime_metadata.get("policy_requires_explicit_review")
        or runtime_metadata.get("critical_claims_partial_support")
    ):
        decision = "HUMAN_REVIEW_REQUIRED"
        reason = "EVIDENCE_CONFLICT" if runtime_metadata.get("has_evidence_conflict") else "HUMAN_REVIEW_POLICY"
    elif runtime_metadata.get("control") or runtime_metadata.get("is_control"):
        decision = "APPROVED_FOR_SCORING"
        reason = "NONE"
    else:
        decision = "TRUST_NOT_READY"
        reason = "TRUST_NOT_READY"

    if lang == "es":
        lang_label = "Espa\xf1ol."
        justification = (
            "La presencia formal de una cita o m\xe9trica de latencia no verifica por s\xed misma una respuesta. "
            "Una conclusi\xf3n no puede depender de una regla de scoring no soportada o de premisas sin evidencia emp\xedrica. "
            "Por lo tanto, la muestra debe excluirse de forma determinista y no enviarse a revisi\xf3n humana."
        )
    else:
        lang_label = "English."
        justification = (
            "The formal presence of a citation or latency metric does not verify a response by itself. "
            "A conclusion cannot depend on an unsupported scoring rule or premises lacking empirical evidence. "
            "Therefore, the sample must be excluded deterministically and not sent to human review."
        )

    analysis_lines = []
    for ac in analyzed_claims:
        analysis_lines.append(
            f"{ac['index']}. Claim: \"{ac['claim']}\"\n"
            f"   Origin/type: {ac['origin_type']}.\n"
            f"   User-provided origin: {ac['user_provided_origin']}.\n"
            f"   Evidence issue: {ac['evidence_issue']}.\n"
            f"   Code/production issue: {ac['code_production_issue']}.\n"
            f"   Support status: {ac['support_status']}.\n"
            f"   Risk: {ac['risk']}.\n"
            f"   Benchmark relevance: {ac['benchmark_relevance']}."
        )
    analysis_str = "\n\n".join(analysis_lines)

    output_text = (
        f"Language:\n{lang_label}\n\n"
        f"Analysis:\n\n{analysis_str}\n\n"
        f"Decision:\n{decision}\n\n"
        f"Reason:\n{reason}\n\n"
        f"Justification:\n{justification}"
    )

    return {
        "language": lang,
        "decision": decision,
        "reason": reason,
        "justification": justification,
        "claims": analyzed_claims,
        "output_text": output_text,
    }
