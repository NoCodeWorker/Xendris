"""Conservative observable-location classification for v5.7.2."""

from __future__ import annotations

import re


ALLOWED_CLASSES = {
    "VISIBILITY",
    "FRINGE_VISIBILITY",
    "INTERFERENCE_CONTRAST",
    "CONTRAST_DECAY",
    "COHERENCE_LOSS",
    "DECOHERENCE_RATE",
    "PHASE_DECAY",
    "THERMAL_DECOHERENCE_VISIBILITY",
    "MATTER_WAVE_VISIBILITY",
    "COLLISIONAL_DECOHERENCE_RATE",
}


KEYWORDS = {
    "VISIBILITY": ["visibility", "visibilities"],
    "FRINGE_VISIBILITY": ["fringe visibility", "visibility", "contrast"],
    "INTERFERENCE_CONTRAST": ["interference contrast", "contrast", "visibility"],
    "CONTRAST_DECAY": ["contrast decay", "decrease of contrast", "loss of contrast"],
    "COHERENCE_LOSS": ["decoherence", "coherence loss"],
    "DECOHERENCE_RATE": ["decoherence rate", "decay rate"],
    "PHASE_DECAY": ["phase decay", "dephasing"],
    "THERMAL_DECOHERENCE_VISIBILITY": ["thermal decoherence", "visibility"],
    "MATTER_WAVE_VISIBILITY": ["matter-wave", "matter wave", "visibility", "contrast"],
    "COLLISIONAL_DECOHERENCE_RATE": ["collisional decoherence", "decoherence rate"],
}

NUMERIC_PATTERN = re.compile(r"(?i)(?:visibility|contrast|visibilities|v)\s*(?:of|=|:)?\s*(?:\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?)|(?:\d+(?:\.\d+)?\s*%)")
FIGURE_PATTERN = re.compile(r"(?i)\b(?:fig\.?|figure)\s*([0-9]+[a-z]?)")
TABLE_PATTERN = re.compile(r"(?i)\btable\s*([0-9]+[a-z]?)")


def classify_snippet(observable_class: str, snippet: str) -> tuple[str, str | None, str | None, list[str], str]:
    lower = snippet.lower()
    if "supplement" in lower or "supporting" in lower:
        return "SUPPLEMENTARY_POINTER", None, None, ["SUPPLEMENTARY_POINTER_ONLY"], "Review supplementary files before y_true extraction."
    if "equation" in lower or re.search(r"\b(eq\.|equation)\s*\(?\d+", lower):
        return "THEORETICAL_EQUATION", None, None, ["NOT_OBSERVED_MEASUREMENT"], "Do not use equation-only locations as y_true."
    model_terms = ["model", "simulation", "theory", "theoretical", "calculation", "predicts", "expected from theory"]
    observed_terms = ["raw data", "measured", "experimental data", "experimentally", "observed", "we achieve"]
    if any(term in lower for term in model_terms) and not any(term in lower for term in observed_terms):
        return "MODEL_PARAMETER", _numeric(snippet), _unit(snippet), ["NOT_OBSERVED_MEASUREMENT"], "Reject model/theory/simulation context."
    if "bound" in lower or "limit" in lower or "constraint" in lower:
        return "BOUND_OR_CONSTRAINT", _numeric(snippet), _unit(snippet), ["NOT_OBSERVED_MEASUREMENT"], "Reject bound/constraint context."
    numeric = _numeric(snippet)
    unit = _unit(snippet)
    if numeric:
        if not any(term in lower for term in observed_terms):
            return "QUALITATIVE_PROSE", numeric, unit, ["OBSERVED_MEASUREMENT_CONTEXT_UNCLEAR"], "Require human review before treating this as an observed measurement candidate."
        return "OBSERVED_MEASUREMENT_CANDIDATE", numeric, unit, ["REQUIRES_HUMAN_FIGURE_REVIEW"], "Review figure/table before v5.7.3 y_true extraction."
    return "QUALITATIVE_PROSE", None, None, ["NO_NUMERIC_VALUE"], "Reject qualitative prose for y_true extraction."


def find_figure_id(snippet: str) -> str | None:
    match = FIGURE_PATTERN.search(snippet)
    return f"FIG. {match.group(1)}" if match else None


def find_table_id(snippet: str) -> str | None:
    match = TABLE_PATTERN.search(snippet)
    return f"TABLE {match.group(1)}" if match else None


def matches_observable(observable_class: str, text: str) -> bool:
    lower = text.lower()
    return any(keyword in lower for keyword in KEYWORDS.get(observable_class, []))


def snippet_windows(text: str, observable_class: str, radius: int = 320) -> list[str]:
    lower = text.lower()
    windows: list[str] = []
    for keyword in KEYWORDS.get(observable_class, []):
        start = 0
        while True:
            index = lower.find(keyword, start)
            if index == -1:
                break
            left = max(0, index - radius)
            right = min(len(text), index + len(keyword) + radius)
            snippet = " ".join(text[left:right].split())
            if snippet and snippet not in windows:
                windows.append(snippet)
            start = index + len(keyword)
    return windows[:3]


def _numeric(snippet: str) -> str | None:
    match = NUMERIC_PATTERN.search(snippet)
    return match.group(0) if match else None


def _unit(snippet: str) -> str | None:
    if "%" in snippet:
        return "percent_or_fraction_visibility"
    return None
