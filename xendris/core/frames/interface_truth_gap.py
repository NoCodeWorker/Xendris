"""InterfaceTruthGap for Xendris Epistemic Frame Layer.

Measures the distance between interface utility (how useful the output looks)
and cognitive certainty (how confident the model actually is). A larger gap
means the presentation promises more certainty than the evidence supports.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class TruthGapSeverity(Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class TruthGapAssessment:
    gap_score: float
    severity: TruthGapSeverity
    reason: str
    details: str = ""


_INTERFACE_CONFIDENCE_SIGNALS = {
    "high": {"guaranteed", "certain", "undoubtedly", "always", "proven", "verified", "confirmed", "absolute", "definitely"},
    "medium": {"likely", "probably", "suggests", "indicates", "supported by", "consistent with", "evidence suggests"},
    "low": {"possibly", "may", "might", "could", "unclear", "not confirmed", "preliminary", "tentative"},
}

_EVIDENCE_QUALITY_SIGNALS = {
    "strong": {"randomized trial", "meta-analysis", "systematic review", "replicated", "large-scale study"},
    "moderate": {"observational study", "case study", "single experiment", "pilot study"},
    "weak": {"anecdotal", "single observation", "hypothetical", "simulated", "synthetic", "laboratory conditions only"},
}


def assess_interface_truth_gap(
    output_text: str,
    evidence_score: float = 0.0,
    evidence_count: int = 0,
    metadata: Mapping[str, Any] | None = None,
) -> TruthGapAssessment:
    """Measure the gap between interface confidence and evidence support.

    Args:
        output_text: The model output.
        evidence_score: 0.0 (no evidence) to 1.0 (fully supported).
        evidence_count: Number of evidence items cited.

    Returns a TruthGapAssessment with the gap score and severity.
    """
    text_lower = output_text.lower()

    high_count = sum(1 for w in _INTERFACE_CONFIDENCE_SIGNALS["high"] if w in text_lower)
    medium_count = sum(1 for w in _INTERFACE_CONFIDENCE_SIGNALS["medium"] if w in text_lower)
    low_count = sum(1 for w in _INTERFACE_CONFIDENCE_SIGNALS["low"] if w in text_lower)

    strong_evidence = sum(1 for w in _EVIDENCE_QUALITY_SIGNALS["strong"] if w in text_lower)
    moderate_evidence = sum(1 for w in _EVIDENCE_QUALITY_SIGNALS["moderate"] if w in text_lower)
    weak_evidence = sum(1 for w in _EVIDENCE_QUALITY_SIGNALS["weak"] if w in text_lower)

    confidence_score = min(1.0, (high_count * 1.0 + medium_count * 0.6 + low_count * 0.2) / max(1, high_count + medium_count + low_count))
    if high_count + medium_count + low_count == 0:
        confidence_score = 0.0

    evidence_quality = (strong_evidence * 1.0 + moderate_evidence * 0.5) / max(1, strong_evidence + moderate_evidence + weak_evidence)
    if strong_evidence + moderate_evidence + weak_evidence == 0:
        evidence_quality = evidence_score

    gap = max(0.0, confidence_score - evidence_quality)

    if gap >= 0.7:
        severity = TruthGapSeverity.CRITICAL
        reason = f"Critical truth gap: interface confidence ({confidence_score:.2f}) far exceeds evidence quality ({evidence_quality:.2f})."
    elif gap >= 0.5:
        severity = TruthGapSeverity.HIGH
        reason = f"High truth gap: interface confidence ({confidence_score:.2f}) significantly exceeds evidence quality ({evidence_quality:.2f})."
    elif gap >= 0.3:
        severity = TruthGapSeverity.MEDIUM
        reason = f"Medium truth gap: interface confidence ({confidence_score:.2f}) exceeds evidence quality ({evidence_quality:.2f})."
    elif gap >= 0.1:
        severity = TruthGapSeverity.LOW
        reason = f"Low truth gap: interface confidence ({confidence_score:.2f}) slightly exceeds evidence quality ({evidence_quality:.2f})."
    else:
        severity = TruthGapSeverity.NONE
        reason = f"No significant truth gap: interface confidence ({confidence_score:.2f}) aligns with evidence quality ({evidence_quality:.2f})."

    details = (
        f"High-confidence signals: {high_count}, Medium: {medium_count}, Low: {low_count}. "
        f"Strong evidence signals: {strong_evidence}, Moderate: {moderate_evidence}, Weak: {weak_evidence}. "
        f"Evidence score: {evidence_score:.2f}, Evidence count: {evidence_count}."
    )

    return TruthGapAssessment(
        gap_score=round(gap, 4),
        severity=severity,
        reason=reason,
        details=details,
    )
