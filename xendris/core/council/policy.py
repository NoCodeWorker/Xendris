"""AdaptiveCouncilPolicy — decides when to escalate from single-model to multi-model council."""
from __future__ import annotations

from decimal import Decimal
from xendris.core.council.models import (
    GuardResult, EscalationReason, GuardOutput, CouncilDecision,
)
from xendris.core.council.sycophancy import SycophancyGuard
from xendris.core.council.contrarian import ContrarianGuard
from xendris.core.council.principles import FirstPrinciplesGuard
from xendris.core.council.evidence import EvidenceGuard


class AdaptiveCouncilPolicy:
    """No council by default. Only escalates when there is evidence of need."""

    def __init__(
        self,
        sycophancy_guard: SycophancyGuard | None = None,
        contrarian_guard: ContrarianGuard | None = None,
        principles_guard: FirstPrinciplesGuard | None = None,
        evidence_guard: EvidenceGuard | None = None,
    ) -> None:
        self.sycophancy_guard = sycophancy_guard or SycophancyGuard()
        self.contrarian_guard = contrarian_guard or ContrarianGuard()
        self.principles_guard = principles_guard or FirstPrinciplesGuard()
        self.evidence_guard = evidence_guard or EvidenceGuard()

    def evaluate(
        self,
        user_input: str,
        model_output: str,
        risk_level: str = "LOW",
        claim_type: str = "FACTUAL",
    ) -> CouncilDecision:
        guards: list[GuardOutput] = []
        sycophancy_flagged = False

        # F-01: SycophancyGuard
        sg = self.sycophancy_guard.evaluate(user_input, model_output)
        guards.append(sg)
        if sg.result == GuardResult.FLAG:
            sycophancy_flagged = True

        # F-03: ContrarianGuard (only if sycophancy flagged)
        cg = self.contrarian_guard.evaluate(user_input, model_output, sycophancy_flagged)
        guards.append(cg)

        # F-04: FirstPrinciplesGuard
        pg = self.principles_guard.evaluate(user_input, model_output)
        guards.append(pg)

        # F-05: EvidenceGuard
        eg = self.evidence_guard.evaluate(user_input, model_output)
        guards.append(eg)

        # Determine escalation
        risk_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
        risk_val = risk_map.get(risk_level.upper(), 0)

        reasons_for_escalation = self._check_escalation_reasons(sg, cg, pg, eg, risk_val, claim_type)

        if reasons_for_escalation:
            reason = reasons_for_escalation[0]
            is_high_impact = risk_val >= 2 or claim_type.upper() == "FACTUAL"
            budget_allows = True  # simplified: always allows for MVP

            esc = EscalationReason.HIGH_IMPACT_SYCOPHANCY if sycophancy_flagged and is_high_impact else reason
            selected = ["gpt-4", "claude-3-haiku"]  # council models

            return CouncilDecision(
                requires_council=True,
                escalation_reason=esc,
                guard_results=guards,
                selected_models=selected,
                marginal_certainty_gain=Decimal("0.05"),
                tokens_used=1500,
                cost=Decimal("0.03"),
                tokens_avoided=3000,
                cost_saved=Decimal("0.06"),
                verdict="ESCALATED_TO_COUNCIL",
            )

        return CouncilDecision(
            requires_council=False,
            guard_results=guards,
            marginal_certainty_gain=Decimal("0.00"),
            verdict="SINGLE_MODEL_OK",
        )

    def _check_escalation_reasons(
        self,
        sg: GuardOutput,
        cg: GuardOutput,
        pg: GuardOutput,
        eg: GuardOutput,
        risk_val: int,
        claim_type: str,
    ) -> list[EscalationReason]:
        reasons: list[EscalationReason] = []

        if sg.result == GuardResult.FLAG and cg.result == GuardResult.FLAG:
            reasons.append(EscalationReason.SYCOPHANCY_DETECTED)

        if pg.result == GuardResult.FLAG:
            reasons.append(EscalationReason.STRONG_CONTRADICTION)

        if risk_val >= 2:
            reasons.append(EscalationReason.HIGH_RISK_CLAIM)

        if eg.result == GuardResult.FLAG and risk_val >= 1:
            reasons.append(EscalationReason.INSUFFICIENT_EVIDENCE_HIGH_IMPACT)

        return reasons
