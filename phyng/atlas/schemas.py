from pydantic import BaseModel, Field


class PhysicalSystemSpec(BaseModel):
    system_id: str
    label: str
    description: str
    m_kg: float = Field(gt=0)
    L_value_m: float = Field(gt=0)
    L_type: str
    physical_role: str
    observer_channel: str
    justification: str
    allowed_range_m: tuple[float, float]
    arbitrariness_risk: str
    source_ids: list[str] = Field(default_factory=list)


class BoundaryAtlasPoint(BaseModel):
    system_id: str
    label: str
    m_kg: float
    L_value_m: float
    L_type: str
    lambda_c_m: float
    r_g_m: float
    schwarzschild_radius_m: float
    Q: float
    B: float
    QB: float
    planck_ratio_squared: float
    delta_QB: float
    logQ: float
    logB: float
    u: float
    w: float
    scale_status: str
    region: str
    trace_type: str
    claim_status: str
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    test_ids: list[str] = Field(default_factory=list)


class AtlasThresholds(BaseModel):
    near_boundary_threshold: float = 1e-1
    small_threshold: float = 1e-20


class BoundaryAtlas(BaseModel):
    atlas_id: str
    version: str
    points: list[BoundaryAtlasPoint] = Field(default_factory=list)
    summary: dict = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    required_sources: list[str] = Field(default_factory=list)
    generated_at: str
