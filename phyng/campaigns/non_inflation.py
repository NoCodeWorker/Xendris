from pydantic import BaseModel


CLAIM_LEVELS = {
    0: "calculation exists",
    1: "structural identity validated",
    2: "negative bound produced",
    3: "toy model delta produced",
    4: "toy benchmark gain produced",
    5: "source-backed physical model comparison",
    6: "detectable candidate prediction",
    7: "empirically actionable proposal",
}


class ClaimLevelDecision(BaseModel):
    evidence_level: int
    requested_claim_level: int
    decision: str
    reason: str
    safe_rewrite: str | None = None


def evaluate_claim_level(
    evidence_level: int,
    requested_claim_level: int,
) -> ClaimLevelDecision:
    if evidence_level not in CLAIM_LEVELS:
        raise ValueError(f"Unknown evidence level: {evidence_level}")
    if requested_claim_level not in CLAIM_LEVELS:
        raise ValueError(f"Unknown requested claim level: {requested_claim_level}")

    if requested_claim_level > evidence_level:
        return ClaimLevelDecision(
            evidence_level=evidence_level,
            requested_claim_level=requested_claim_level,
            decision="BLOCKED_OVERCLAIM",
            reason=(
                f"Requested claim level {requested_claim_level} exceeds "
                f"available evidence level {evidence_level}."
            ),
            safe_rewrite=(
                "Phygn computes a toy model delta under explicit assumptions. "
                "No physical decoherence prediction is claimed."
            ),
        )

    return ClaimLevelDecision(
        evidence_level=evidence_level,
        requested_claim_level=requested_claim_level,
        decision="ALLOWED_WITHIN_EVIDENCE_LEVEL",
        reason="Requested claim level is supported by available evidence level.",
    )
