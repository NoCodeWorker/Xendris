"""EvidenceGuard — verifies if a claim has associated evidence; degrades to hypothesis if not."""
from __future__ import annotations

import re
from xendris.core.council.models import GuardResult, GuardOutput

_EVIDENCE_MARKERS = [
    r"\b(?:stud(?:y|ies)|research|paper|publication|experiment|trial)\s+(?:shows?|found|demonstrates?|indicates?|suggests?|proves?|confirms?|reports?)\b",
    r"\baccording to\b",
    r"\bas (?:shown|demonstrated|proven|reported)\s+(?:by|in)\b",
    r"\b(?:data|evidence|results|findings)\s+(?:show|suggest|indicate|demonstrate|support|confirm)\b",
    r"\b(?:meta[-\s]?analysis|systematic review|randomized controlled trial|RCT)\b",
    r"\b(?:published in|journal of|peer[-\s]?reviewed)\b",
    r"\bcitation needed\b",
    r"\breference\b",
    r"\bsource\b",
]

_QUALIFIER_MARKERS = [
    r"\bsuggests?\b",
    r"\bhypothesis\b",
    r"\bmay\b",
    r"\bmight\b",
    r"\bcould\b",
    r"\bpossible\b",
    r"\bunclear\b",
    r"\binsufficient evidence\b",
    r"\bnot enough (?:data|evidence|information)\b",
    r"\bfurther research needed\b",
    r"\brequires more study\b",
]


class EvidenceGuard:
    """Verifies if a claim has evidence; degrades unsupported claims to hypothesis."""

    def evaluate(self, user_input: str, model_output: str) -> GuardOutput:
        lower = model_output.lower()

        has_evidence = any(re.search(p, lower) for p in _EVIDENCE_MARKERS)
        has_qualifier = any(re.search(p, lower) for p in _QUALIFIER_MARKERS)

        if has_evidence:
            return GuardOutput(
                guard_name="EvidenceGuard",
                result=GuardResult.PASS,
                reason="Evidence markers found in response",
                details={"has_evidence": True, "has_qualifier": has_qualifier},
            )

        if has_qualifier:
            return GuardOutput(
                guard_name="EvidenceGuard",
                result=GuardResult.PASS,
                reason="Claim properly qualified as hypothesis",
                details={"has_evidence": False, "has_qualifier": True},
            )

        return GuardOutput(
            guard_name="EvidenceGuard",
            result=GuardResult.FLAG,
            reason="Claim lacks evidence markers and is not qualified as hypothesis",
            details={"has_evidence": False, "has_qualifier": False},
        )
