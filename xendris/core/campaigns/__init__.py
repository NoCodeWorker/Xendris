"""
xendris.core.campaigns — Validation campaign runners.

Consolidates phyng campaign orchestration under one namespace:

    phyng.campaigns  → mesoscopic boundary, decoherence model comparison
    phyng.atlas      → boundary atlas builder

Usage:
    from xendris.core.campaigns import run_mesoscopic_boundary_campaign
"""

from phyng.campaigns import (  # noqa: F401
    Campaign002Input,
    CampaignInput,
    run_campaign_002_decoherence_model_comparison,
    run_mesoscopic_boundary_campaign,
)
from phyng.atlas import build_atlas, PhysicalSystemSpec, AtlasThresholds  # noqa: F401

__all__ = [
    "Campaign002Input",
    "CampaignInput",
    "run_campaign_002_decoherence_model_comparison",
    "run_mesoscopic_boundary_campaign",
    "build_atlas",
    "PhysicalSystemSpec",
    "AtlasThresholds",
]
