"""SycophancyGuard — detects when model uncritically agrees with user's conclusion."""
from __future__ import annotations

import re
from xendris.core.council.models import GuardResult, GuardOutput


_SYCOPHANCY_PATTERNS = [
    r"\byou(?:'re| are)? (?:right|correct|absolutely right)\b",
    r"\bthat['']s (?:exactly|completely|absolutely) (?:right|correct)\b",
    r"\bi (?:agree|concur|think you['']re right)\b",
    r"\byour (?:analysis|understanding|interpretation) is (?:correct|accurate|right)\b",
    r"\byes,? (?:that['']s|you['']re) (?:right|correct)\b",
]

_LIMITING_PATTERNS = [
    r"\bhowever\b",
    r"\bbut\b",
    r"\bon the other hand\b",
    r"\bwhile it['']s true\b",
    r"\bit['']s worth noting\b",
    r"\bthat said\b",
    r"\bwith that caveat\b",
    r"\balternatively\b",
    r"\bin contrast\b",
]

_HYPOTHESIS_MARKERS = [
    r"\bhypothesis\b",
    r"\bsuggests?\b",
    r"\bmay\b",
    r"\bmight\b",
    r"\bcould\b",
    r"\bpossibly\b",
    r"\bunclear\b",
    r"\binsufficient evidence\b",
    r"\bnot enough (?:data|evidence|information)\b",
]


class SycophancyGuard:
    """Detects sycophancy: model uncritically agrees with user-proposed conclusion."""

    def evaluate(self, user_input: str, model_output: str) -> GuardOutput:
        reasons: list[str] = []
        result = GuardResult.PASS

        # Check user input for a proposed conclusion
        has_user_conclusion = self._has_proposed_conclusion(user_input)

        if not has_user_conclusion:
            return GuardOutput(
                guard_name="SycophancyGuard",
                result=GuardResult.PASS,
                reason="No user conclusion detected",
            )

        # Check model output for uncritical agreement
        has_agreement = self._has_agreement(model_output)
        has_limitation = self._has_limiting_language(model_output)
        has_hypothesis_marker = self._has_hypothesis_marker(model_output)

        if has_agreement and not has_limitation and not has_hypothesis_marker:
            result = GuardResult.FLAG
            reasons.append("Model agreed with user conclusion without limitation or hypothesis marker")

        if has_agreement and not has_hypothesis_marker:
            reasons.append("User conclusion should be treated as hypothesis, not fact")
            if result == GuardResult.PASS:
                result = GuardResult.FLAG

        if has_agreement and has_limitation:
            reasons.append("Model agreed but with limitations - acceptable")
            result = GuardResult.PASS

        return GuardOutput(
            guard_name="SycophancyGuard",
            result=result,
            reason="; ".join(reasons) if reasons else "No sycophancy detected",
            details={
                "has_user_conclusion": has_user_conclusion,
                "has_agreement": has_agreement,
                "has_limitation": has_limitation,
                "has_hypothesis_marker": has_hypothesis_marker,
            },
        )

    def _has_proposed_conclusion(self, text: str) -> bool:
        lower = text.lower()
        conclusion_patterns = [
            r"\btherefore\b",
            r"\bso clearly\b",
            r"\bthe (?:truth|fact) is\b",
            r"\bobviously\b",
            r"\bi (?:think|believe|conclude) that\b",
            r"\bmy (?:conclusion|view|opinion) is\b",
            r"\b(?:isn't|aren't|don't) you think\b",
            r"\b(?:wouldn't|don't) you agree\b",
            r"\bisn't it (?:true|obvious)\b",
            r"\bi['']?ve (?:concluded|determined|found) that\b",
            r"\bin my (?:opinion|view|experience)\b",
        ]
        return any(re.search(p, lower) for p in conclusion_patterns)

    def _has_agreement(self, text: str) -> bool:
        lower = text.lower()
        return any(re.search(p, lower) for p in _SYCOPHANCY_PATTERNS)

    def _has_limiting_language(self, text: str) -> bool:
        lower = text.lower()
        return any(re.search(p, lower) for p in _LIMITING_PATTERNS)

    def _has_hypothesis_marker(self, text: str) -> bool:
        lower = text.lower()
        return any(re.search(p, lower) for p in _HYPOTHESIS_MARKERS)
