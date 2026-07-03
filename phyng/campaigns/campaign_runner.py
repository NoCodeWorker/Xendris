from pathlib import Path
from phyng.campaigns.schemas import CampaignInput, CampaignResult
from phyng.campaigns.mesoscopic_boundary_number import run_mesoscopic_boundary_campaign


def run_campaign(
    campaign_id: str, campaign_input: CampaignInput, root_dir: Path
) -> CampaignResult:
    if campaign_id == "CAMPAIGN-001" or campaign_input.campaign_id == "CAMPAIGN-001":
        return run_mesoscopic_boundary_campaign(campaign_input, root_dir)
    else:
        raise ValueError(f"Unknown campaign ID: {campaign_id}")
