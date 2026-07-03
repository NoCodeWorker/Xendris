from pydantic import BaseModel, Field


class CampaignInput(BaseModel):
    campaign_id: str
    system_id: str
    m_kg: float = Field(gt=0)
    L_value_m: float = Field(gt=0)
    L_type: str
    physical_role: str
    observer_channel: str
    justification: str
    allowed_range_m: tuple[float, float]
    arbitrariness_risk: str


class CampaignResult(BaseModel):
    campaign_id: str
    system_id: str
    signature: dict = Field(default_factory=dict)
    atlas_region: str
    trace_type: str
    scale_status: str
    scale_reason: str
    non_triviality_status: str
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    required_sources: list[str] = Field(default_factory=list)
    required_models: list[str] = Field(default_factory=list)
    required_tests: list[str] = Field(default_factory=list)
    benchmark_status: str
    next_tasks: list[str] = Field(default_factory=list)
