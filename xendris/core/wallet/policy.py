"""Budget policy engine and balance check gate for the runtime."""
from __future__ import annotations

from decimal import Decimal
from datetime import datetime, timedelta

from xendris.core.wallet.models import TenantWallet
from xendris.core.wallet.store import WalletStore


class BudgetPolicy:
    """Evaluates pre-request budget constraints."""

    def __init__(self, store: WalletStore) -> None:
        self.store = store

    def check_limits(self, tenant_id: str, estimated_cost: Decimal) -> str | None:
        wallet = self.store.get_wallet(tenant_id)
        if wallet is None:
            return f"WALLET_NOT_FOUND:{tenant_id}"

        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        txs = self.store.get_transactions(tenant_id, limit=10000)

        daily_total = sum(
            tx.amount for tx in txs
            if tx.transaction_type == "CHARGE" and tx.timestamp >= today_start
        )
        monthly_total = sum(
            tx.amount for tx in txs
            if tx.transaction_type == "CHARGE" and tx.timestamp >= month_start
        )

        total_after = wallet.balance - estimated_cost

        if total_after < 0:
            return f"INSUFFICIENT_BALANCE:balance={wallet.balance},estimated={estimated_cost}"
        if wallet.hard_cap > 0 and wallet.balance + estimated_cost > wallet.hard_cap:
            return f"HARD_CAP_EXCEEDED:cap={wallet.hard_cap}"
        if wallet.daily_limit > 0 and daily_total + estimated_cost > wallet.daily_limit:
            return f"DAILY_LIMIT_EXCEEDED:limit={wallet.daily_limit},used={daily_total},estimated={estimated_cost}"
        if wallet.monthly_limit > 0 and monthly_total + estimated_cost > wallet.monthly_limit:
            return f"MONTHLY_LIMIT_EXCEEDED:limit={wallet.monthly_limit},used={monthly_total},estimated={estimated_cost}"

        return None


class BalanceCheckGate:
    """Gate that blocks execution if wallet balance < estimated cost."""

    def __init__(self, store: WalletStore) -> None:
        self.store = store

    def check(self, tenant_id: str, estimated_cost: Decimal) -> str | None:
        wallet = self.store.get_wallet(tenant_id)
        if wallet is None:
            return f"WALLET_NOT_FOUND:{tenant_id}"
        if not wallet.can_charge(estimated_cost):
            return f"BALANCE_INSUFFICIENT:balance={wallet.balance},required={estimated_cost}"
        return None
