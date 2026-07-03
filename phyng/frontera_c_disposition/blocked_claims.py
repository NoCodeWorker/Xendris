"""Blocked and allowed claim boundaries for v5.6."""

from __future__ import annotations

from phyng.frontera_c_disposition.schemas import BlockedClaims


BLOCKED_CLAIMS = [
    "LOG_BOUNDARY is validated.",
    "LOG_BOUNDARY validates Frontera C.",
    "LOG_BOUNDARY supports the invariant.",
    "LOG_BOUNDARY has robust PredictiveGain.",
    "Negative-control failure can be bypassed by more architecture.",
    "Frontera C is validated.",
    "The invariant is empirically confirmed.",
]

ALLOWED_CLAIMS = [
    "LOG_BOUNDARY produced a positive single-source smoke test.",
    "LOG_BOUNDARY failed negative controls because the gain was explained by simple controls.",
    "LOG_BOUNDARY was archived as a Frontera C validation candidate.",
    "LOG_BOUNDARY may be retained as a benchmark/control fixture.",
]


def build_blocked_claims(candidate_family: str = "LOG_BOUNDARY") -> BlockedClaims:
    return BlockedClaims(
        candidate_family=candidate_family,
        blocked_claims=BLOCKED_CLAIMS,
        allowed_claims=ALLOWED_CLAIMS,
        claim_permission="CLAIM_BLOCKED",
        physical_claim_created=False,
        frontera_c_validated=False,
        invariant_confirmed=False,
    )
