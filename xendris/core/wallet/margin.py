"""Xendris margin calculator — provider_cost + markup = total."""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from xendris.core.wallet.models import WalletConfig


class MarginCalculator:
    """Calculates Xendris margin over provider cost."""

    def __init__(self, config: WalletConfig | None = None) -> None:
        self.config = config or WalletConfig()

    def calculate(self, provider_cost: Decimal, margin_rate: Decimal | None = None, fixed_fee: Decimal | None = None) -> Decimal:
        rate = margin_rate if margin_rate is not None else self.config.margin_rate
        fee = fixed_fee if fixed_fee is not None else self.config.fixed_fee
        margin = (provider_cost * rate) + fee
        total = provider_cost + margin
        return total.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)

    def margin_only(self, provider_cost: Decimal, margin_rate: Decimal | None = None, fixed_fee: Decimal | None = None) -> Decimal:
        rate = margin_rate if margin_rate is not None else self.config.margin_rate
        fee = fixed_fee if fixed_fee is not None else self.config.fixed_fee
        margin = (provider_cost * rate) + fee
        return margin.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
