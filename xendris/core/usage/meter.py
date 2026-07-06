"""Usage meter — records per-request usage and provider costs."""
from __future__ import annotations

import json
import uuid
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from xendris.core.usage.models import UsageRecord, ProviderCostRecord, UsageQuery


class UsageMeter:
    """Records and queries usage records for tenant billing."""

    def __init__(self, data_dir: str | Path = "data/usage") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _usage_path(self, tenant_id: str, date_str: str | None = None) -> Path:
        if date_str is None:
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
        return self.data_dir / tenant_id / f"{date_str}.jsonl"

    def record_usage(self, usage: UsageRecord) -> UsageRecord:
        path = self._usage_path(usage.tenant_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(usage.model_dump(), default=str)
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return usage

    def record_provider_cost(self, cost: ProviderCostRecord) -> ProviderCostRecord:
        path = self.data_dir / "_provider_costs" / f"{cost.run_id}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cost.model_dump(), f, default=str, indent=2)
        return cost

    def query_usage(self, query: UsageQuery) -> list[UsageRecord]:
        records: list[UsageRecord] = []
        tenant_dir = self.data_dir / query.tenant_id
        if not tenant_dir.exists():
            return records

        for fpath in sorted(tenant_dir.glob("*.jsonl")):
            for line in fpath.read_text("utf-8").strip().split("\n"):
                if not line.strip():
                    continue
                data = json.loads(line)
                record = UsageRecord(**data)
                if query.model_id and record.model_id != query.model_id:
                    continue
                if query.project_id and record.project_id != query.project_id:
                    continue
                if query.start_date and record.timestamp < query.start_date:
                    continue
                if query.end_date and record.timestamp > query.end_date:
                    continue
                records.append(record)

        return records

    def get_tenant_daily_total(self, tenant_id: str) -> Decimal:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        path = self._usage_path(tenant_id, today)
        if not path.exists():
            return Decimal("0.00")
        total = Decimal("0.00")
        for line in path.read_text("utf-8").strip().split("\n"):
            if line.strip():
                data = json.loads(line)
                total += Decimal(str(data.get("xendris_cost", "0")))
        return total
