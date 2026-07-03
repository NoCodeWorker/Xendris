"""
Phygn v1.7 — Model-Agnostic Runtime: Schemas

ModelBackend, ModelResponse, BackendRegistration, BackendPermission.

Core rule: LLM proposes. Phygn verifies.
"""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

ModelType = Literal[
    "FRONTIER_API",
    "OPEN_SOURCE_API",
    "LOCAL_LLM",
    "SMALL_CLASSIFIER",
    "EMBEDDING_MODEL",
    "RULE_BASED",
    "HUMAN_REVIEW",
]

ModelPermissionStatus = Literal[
    "MODEL_FULLY_ALLOWED_FOR_LOW_RISK",
    "MODEL_ALLOWED_WITH_VALIDATION",
    "MODEL_REQUIRES_HUMAN_REVIEW",
    "MODEL_BLOCKED_FOR_HIGH_RISK",
]

TaskCategory = Literal[
    "idea_intake",
    "hypothesis_seed_generation",
    "proxy_suggestion",
    "claim_extraction",
    "source_audit",
    "report_drafting",
    "financial_action",
    "automated_execution",
    "physical_validation",
    "medical_legal_claim",
    "gatekeeping",
]


class ModelResponse(BaseModel):
    """Output from any model backend."""
    backend_id: str
    model_name: str
    model_type: ModelType
    prompt_used: str
    raw_output: str
    structured_output: dict | None = None
    is_validated: bool = False
    validation_notes: list[str] = Field(default_factory=list)
    label: str = "PROPOSED_NOT_VALIDATED"


class BackendRegistration(BaseModel):
    """Registration entry for a model backend."""
    backend_id: str
    model_name: str
    model_type: ModelType
    supports_json_mode: bool = False
    supports_tool_use: bool = False
    context_window_tokens: int | None = None
    is_local: bool = False
    requires_api_key: bool = True
    allowed_tasks: list[TaskCategory] = Field(default_factory=list)
    blocked_tasks: list[TaskCategory] = Field(default_factory=list)
    quality_tier: int = 2  # 1=high, 2=medium, 3=low (affects routing)
    notes: str = ""


class BackendPermission(BaseModel):
    """Result of evaluate_backend_permission for a task."""
    backend_id: str
    model_type: ModelType
    task: TaskCategory
    permission_status: ModelPermissionStatus
    requires_validation: bool
    requires_human_review: bool
    is_blocked: bool
    routing_notes: list[str] = Field(default_factory=list)
