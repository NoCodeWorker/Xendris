from pydantic import BaseModel, Field
from typing import Optional, Dict, Literal

class BenchmarkCase(BaseModel):
    id: str
    title: str
    prompt: str
    expected_failure_type: str
    expected_detection: str
    category: str

class ModelResponse(BaseModel):
    case_id: str
    system: Literal["base_model", "xendris"]
    response_text: str
    raw_metadata: Optional[Dict] = Field(default_factory=dict)

class RubricScore(BaseModel):
    conclusion_inflation_detected: float = Field(..., ge=0.0, le=1.0)
    unsupported_premises_detected: float = Field(..., ge=0.0, le=1.0)
    local_to_global_jump_avoided: float = Field(..., ge=0.0, le=1.0)
    corrected_argument_proposed: float = Field(..., ge=0.0, le=1.0)
    total_score: float = Field(..., ge=0.0, le=1.0)
    severe_regression: bool
    notes: str

class BenchmarkResult(BaseModel):
    case_id: str
    failure_type: str
    base_score: RubricScore
    xendris_score: RubricScore
    winner: Literal["base_model", "xendris", "tie"]
    delta: float
    observation: str
    base_latency_ms: Optional[float] = None
    xendris_latency_ms: Optional[float] = None
    base_timeout: Optional[bool] = None
    xendris_timeout: Optional[bool] = None
    base_error: Optional[str] = None
    xendris_error: Optional[str] = None


class BenchmarkSummary(BaseModel):
    total_cases: int
    xendris_wins: int
    base_model_wins: int
    ties: int
    severe_regressions: int
    passed: bool
    conclusion: str
    execution_mode: Literal["mock", "real_provider"]
    provider_name: str
    timestamp: str

