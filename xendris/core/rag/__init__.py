"""
xendris.core.rag — Retrieval-Augmented Generation helpers.

Consolidates three scattered phyng sub-systems under one namespace:

    phyng.rag                   → source registry, claim registry, audit
    phyng.ytrue_extraction      → y_true candidate builders and QC
    phyng.real_source_acquisition → download queue management

Usage:
    from xendris.core.rag import add_source, list_sources, add_claim, audit_claim_support
"""

# --- Source & Claim registry (phyng.rag is the canonical location) ---
from phyng.rag import (  # noqa: F401
    SourceRecord,
    ClaimRecord,
    ClaimSourceLink,
    add_source,
    list_sources,
    add_claim,
    list_claims,
    link_claim_to_source,
    audit_claim_support,
)

__all__ = [
    "SourceRecord",
    "ClaimRecord",
    "ClaimSourceLink",
    "add_source",
    "list_sources",
    "add_claim",
    "list_claims",
    "link_claim_to_source",
    "audit_claim_support",
]
