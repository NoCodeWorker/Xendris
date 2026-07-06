"""Pydantic models for usage tracking and provider cost records."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from pydantic import BaseModel, Field


class ProviderCostRecord(BaseModel):
    record_id: str
    run_id: str
    model_id: str
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0
    provider_cost: Decimal = Field(default=Decimal("0.00"))
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class UsageRecord(BaseModel):
    usage_id: str
    tenant_id: str
    project_id: str = "default"
    api_key: str = ""
    model_id: str
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0
    provider_cost: Decimal = Field(default=Decimal("0.00"))
    xendris_cost: Decimal = Field(default=Decimal("0.00"))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)


class UsageQuery(BaseModel):
    tenant_id: str
    start_date: datetime | None = None
    end_date: datetime | None = None
    project_id: str | None = None
    model_id: str | None = None
