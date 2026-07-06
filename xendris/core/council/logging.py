"""Council escalation logging — records every escalation in the trust ledger."""
from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any
from xendris.core.council.models import CouncilDecision


class CouncilLedgerRecord:
    """A single council escalation record matching the trust ledger format."""

    def __init__(
        self,
        run_id: str,
        decision: CouncilDecision,
        user_input: str = "",
        model_output: str = "",
    ) -> None:
        self.record_id = f"council-{uuid.uuid4().hex[:12]}"
        self.run_id = run_id
        self.timestamp = datetime.utcnow()
        self.requires_council = decision.requires_council
        self.escalation_reason = decision.escalation_reason.value if decision.escalation_reason else None
        self.verdict = decision.verdict
        self.selected_models = decision.selected_models
        self.tokens_used = decision.tokens_used
        self.cost = decision.cost
        self.tokens_avoided = decision.tokens_avoided
        self.cost_saved = decision.cost_saved
        self.marginal_certainty_gain = decision.marginal_certainty_gain
        self.guard_results = [
            {"guard": g.guard_name, "result": g.result.value, "reason": g.reason}
            for g in decision.guard_results
        ]
        self.user_input_preview = user_input[:200]
        self.model_output_preview = model_output[:200]

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "run_id": self.run_id,
            "timestamp": self.timestamp.isoformat(),
            "requires_council": self.requires_council,
            "escalation_reason": self.escalation_reason,
            "verdict": self.verdict,
            "selected_models": self.selected_models,
            "tokens_used": self.tokens_used,
            "cost": str(self.cost),
            "tokens_avoided": self.tokens_avoided,
            "cost_saved": str(self.cost_saved),
            "marginal_certainty_gain": str(self.marginal_certainty_gain),
            "guard_results": self.guard_results,
        }


class CouncilLogger:
    """Maintains in-memory council escalation log for a runtime session."""

    def __init__(self) -> None:
        self.records: list[CouncilLedgerRecord] = []

    def log_decision(self, run_id: str, decision: CouncilDecision, user_input: str = "", model_output: str = "") -> CouncilLedgerRecord:
        record = CouncilLedgerRecord(run_id, decision, user_input, model_output)
        self.records.append(record)
        return record

    def get_records(self, run_id: str | None = None) -> list[CouncilLedgerRecord]:
        if run_id:
            return [r for r in self.records if r.run_id == run_id]
        return self.records

    def clear(self) -> None:
        self.records.clear()
