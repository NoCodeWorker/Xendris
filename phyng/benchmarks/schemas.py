from pydantic import BaseModel, Field, model_validator


BENCHMARK_PROVENANCE_TYPES = {
    "PLACEHOLDER",
    "SYNTHETIC",
    "SIMULATED",
    "LITERATURE_EXTRACTED",
    "EXPERIMENTAL",
}


class BenchmarkDataset(BaseModel):
    dataset_id: str
    name: str
    observable: str
    t: list[float]
    y_true: list[float]
    provenance_type: str
    source_ids: list[str] = Field(default_factory=list)
    generation_method: str | None = None
    parameters: dict[str, float] = Field(default_factory=dict)
    uncertainty: list[float] | None = None
    epsilon_exp: float | None = None
    allowed_uses: list[str] = Field(default_factory=list)
    forbidden_uses: list[str] = Field(default_factory=list)
    extraction_notes: str | None = None
    units: str | None = None

    @model_validator(mode="after")
    def validate_dataset_shape(self):
        if self.provenance_type not in BENCHMARK_PROVENANCE_TYPES:
            raise ValueError(f"Unsupported provenance_type: {self.provenance_type}")
        if len(self.t) != len(self.y_true):
            raise ValueError("t and y_true must have the same length")
        if not self.t:
            raise ValueError("benchmark dataset must not be empty")
        if self.uncertainty is not None and len(self.uncertainty) != len(self.y_true):
            raise ValueError("uncertainty must match y_true length")
        return self


class BenchmarkReadinessResult(BaseModel):
    dataset_id: str
    readiness_status: str
    can_compute_gain: bool
    gain_label: str | None = None
    allowed_claim_level: int
    blocked_reason: str | None = None
    required_actions: list[str] = Field(default_factory=list)
