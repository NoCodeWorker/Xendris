"""SandboxAudit dataclass definition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SandboxAudit:
    """Audit log record for provider request executions within the Sandbox."""

    endpoint: str
    status_code: int
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    network_allowed: bool
    blocked_by_sandbox: bool
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the sandbox audit record."""
        return {
            "endpoint": self.endpoint,
            "status_code": self.status_code,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "estimated_cost": self.estimated_cost,
            "network_allowed": self.network_allowed,
            "blocked_by_sandbox": self.blocked_by_sandbox,
            "reason": self.reason,
            "metadata": dict(self.metadata),
        }
