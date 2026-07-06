"""JSON-file based wallet store for tenant wallets and transactions."""
from __future__ import annotations

import json
import uuid
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from xendris.core.wallet.models import TenantWallet, WalletTransaction


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def _parse_record(data: dict[str, Any], cls: type) -> Any:
    for key, val in data.items():
        if isinstance(val, str):
            try:
                data[key] = Decimal(val)
            except Exception:
                pass
            try:
                data[key] = datetime.fromisoformat(val)
            except Exception:
                pass
    return cls(**data)


class WalletStore:
    """File-based wallet store. Each tenant gets a wallet file."""

    def __init__(self, data_dir: str | Path = "data/wallets") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _wallet_path(self, tenant_id: str) -> Path:
        return self.data_dir / f"{tenant_id}.json"

    def _tx_path(self, tenant_id: str) -> Path:
        return self.data_dir / f"{tenant_id}_transactions.jsonl"

    def get_wallet(self, tenant_id: str) -> TenantWallet | None:
        path = self._wallet_path(tenant_id)
        if not path.exists():
            return None
        raw = json.loads(path.read_text("utf-8"))
        return _parse_record(raw, TenantWallet)

    def save_wallet(self, wallet: TenantWallet) -> TenantWallet:
        path = self._wallet_path(wallet.tenant_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(wallet.model_dump(), f, cls=DecimalEncoder, indent=2)
        return wallet

    def create_wallet(self, tenant_id: str, initial_balance: Decimal | None = None) -> TenantWallet:
        wallet = TenantWallet(
            tenant_id=tenant_id,
            balance=initial_balance or Decimal("0.00"),
        )
        return self.save_wallet(wallet)

    def append_transaction(self, tx: WalletTransaction) -> WalletTransaction:
        path = self._tx_path(tx.tenant_id)
        line = json.dumps(tx.model_dump(), cls=DecimalEncoder, default=str)
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return tx

    def charge(self, tenant_id: str, amount: Decimal, description: str = "", run_id: str | None = None) -> tuple[TenantWallet, WalletTransaction]:
        wallet = self.get_wallet(tenant_id)
        if wallet is None:
            raise ValueError(f"Wallet not found: {tenant_id}")
        wallet = wallet.charge(amount)
        self.save_wallet(wallet)
        tx = WalletTransaction(
            transaction_id=f"tx-{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            transaction_type="CHARGE",
            amount=amount,
            description=description,
            run_id=run_id,
        )
        self.append_transaction(tx)
        return wallet, tx

    def credit(self, tenant_id: str, amount: Decimal, description: str = "") -> tuple[TenantWallet, WalletTransaction]:
        wallet = self.get_wallet(tenant_id)
        if wallet is None:
            raise ValueError(f"Wallet not found: {tenant_id}")
        wallet = wallet.credit(amount)
        self.save_wallet(wallet)
        tx = WalletTransaction(
            transaction_id=f"tx-{uuid.uuid4().hex[:12]}",
            tenant_id=tenant_id,
            transaction_type="CREDIT",
            amount=amount,
            description=description,
        )
        self.append_transaction(tx)
        return wallet, tx

    def get_transactions(self, tenant_id: str, limit: int = 100) -> list[WalletTransaction]:
        path = self._tx_path(tenant_id)
        if not path.exists():
            return []
        lines = path.read_text("utf-8").strip().split("\n")
        txs = []
        for line in lines[-limit:]:
            if line.strip():
                data = json.loads(line)
                txs.append(_parse_record(data, WalletTransaction))
        return txs
