"""Pydantic models for tenant wallet, transactions, and configuration."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from pydantic import BaseModel, Field


class WalletConfig(BaseModel):
    currency: str = "USD"
    hard_cap: Decimal = Field(default=Decimal("1000.00"), ge=0)
    daily_limit: Decimal = Field(default=Decimal("100.00"), ge=0)
    monthly_limit: Decimal = Field(default=Decimal("500.00"), ge=0)
    margin_rate: Decimal = Field(default=Decimal("0.15"), ge=0)  # 15% Xendris markup
    fixed_fee: Decimal = Field(default=Decimal("0.00"), ge=0)
    alert_threshold_pct: Decimal = Field(default=Decimal("80"), ge=0, le=100)


class TenantWallet(BaseModel):
    tenant_id: str
    balance: Decimal = Field(default=Decimal("0.00"))
    currency: str = "USD"
    hard_cap: Decimal = Field(default=Decimal("1000.00"), ge=0)
    daily_limit: Decimal = Field(default=Decimal("100.00"), ge=0)
    monthly_limit: Decimal = Field(default=Decimal("500.00"), ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def can_charge(self, amount: Decimal) -> bool:
        return self.balance >= amount

    def charge(self, amount: Decimal) -> TenantWallet:
        if not self.can_charge(amount):
            raise ValueError(f"Insufficient balance: {self.balance} < {amount}")
        return self.model_copy(update={
            "balance": self.balance - amount,
            "updated_at": datetime.utcnow(),
        })

    def credit(self, amount: Decimal) -> TenantWallet:
        return self.model_copy(update={
            "balance": self.balance + amount,
            "updated_at": datetime.utcnow(),
        })


class WalletTransaction(BaseModel):
    transaction_id: str
    tenant_id: str
    transaction_type: str  # "CHARGE", "CREDIT", "TOPUP"
    amount: Decimal
    currency: str = "USD"
    description: str = ""
    run_id: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)
