"""Failure classification for v5.7.2 source download."""

from __future__ import annotations


def classify_missing_source(requires_paywall_access: bool, requires_supplementary_download: bool, file_exists: bool) -> str:
    if file_exists:
        return "REJECTED_NOT_SOURCE_OBJECT"
    if requires_paywall_access:
        return "PAYWALL"
    if requires_supplementary_download:
        return "SUPPLEMENTARY_REQUIRED"
    return "MISSING_LOCAL_FILE"
