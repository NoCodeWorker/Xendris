"""Unit and numeric normalization for v5.7.3."""

from __future__ import annotations

import re


def normalize_visibility_value(text: str | None, snippet: str = "") -> tuple[float | None, str | None, str | None, list[str]]:
    if not text and not snippet:
        return None, None, None, []
    chosen = _choose_value(text or "", snippet)
    if chosen is None:
        return None, None, None, []
    value = chosen / 100.0
    return value, f"{chosen:g}%", "dimensionless_fraction", [f"Converted {chosen:g}% to {value:g} dimensionless fraction."]


def extract_conditions(condition_axis: str | None, snippet: str) -> tuple[dict, list[str]]:
    lower = snippet.lower()
    if condition_axis == "velocity_m_s":
        match = re.search(r"central velocity of\s*([0-9]+(?:\.[0-9]+)?)\s*m\s*/\s*s", lower)
        if match:
            return {"velocity_m_s": float(match.group(1))}, ["Mapped central velocity text to velocity_m_s condition."]
        return {}, []
    if condition_axis == "mass_amu":
        power = re.search(r"laser power of\s*p\s*[∼~=]*\s*([0-9]+(?:\.[0-9]+)?)\s*w", lower)
        if power:
            return {"laser_power_W": float(power.group(1))}, ["Mapped laser power text to laser_power_W condition."]
        return {"condition_axis": "mass_amu"}, ["Preserved mass_amu condition axis; exact mass requires source-level review."]
    if condition_axis == "molecule":
        conditions = {}
        if "c60f48" in lower:
            conditions["molecule"] = "C60F48"
        selected = re.search(r"taking only those\s*([0-9]+(?:\.[0-9]+)?)\s*%", lower)
        if selected:
            conditions["selected_scan_fraction"] = float(selected.group(1)) / 100.0
        if conditions:
            return conditions, ["Mapped molecule/selection text to experimental conditions."]
        return {}, []
    return {}, []


def _choose_value(text: str, snippet: str) -> float | None:
    lower = snippet.lower()
    if "interference contrast of" in snippet.lower():
        match = re.search(r"interference contrast of\s*([0-9]+(?:\.[0-9]+)?)\s*%", snippet, re.IGNORECASE)
        if match:
            return float(match.group(1))
    if "statistical error" in lower or "±" in snippet:
        return None
    match = re.search(r"V\s*=\s*([0-9]+(?:\.[0-9]+)?)", snippet)
    if match:
        return float(match.group(1))
    match = re.search(r"visibility\s*(?:of)?\s*([0-9]+(?:\.[0-9]+)?)\s*%", text + " " + snippet, re.IGNORECASE)
    if match:
        return float(match.group(1))
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*%", text or snippet)
    if match:
        return float(match.group(1))
    return None
