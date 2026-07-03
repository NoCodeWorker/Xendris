"""Campaign wrapper for v4.6 candidate freeze review."""

from __future__ import annotations

from pathlib import Path
from phyng.candidate_decision.campaign import run_candidate_decision_campaign
from phyng.candidate_decision.schemas import CampaignResultv46
from typing import Any

def run_phi_gradient_candidate_freeze_review_campaign(root: str | Path = ".") -> CampaignResultv46 | dict[str, Any]:
    return run_candidate_decision_campaign(root)
