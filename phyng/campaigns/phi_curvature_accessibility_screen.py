"""Campaign wrapper for v4.7 PHI_CURVATURE accessibility screen."""

from __future__ import annotations

from pathlib import Path
from phyng.candidate_screening.campaign import run_phi_curvature_accessibility_screen_campaign as run_campaign
from phyng.candidate_screening.schemas import CampaignResultv47
from typing import Any

def run_phi_curvature_accessibility_screen_campaign(root: str | Path = ".") -> CampaignResultv47 | dict[str, Any]:
    return run_campaign(root)
