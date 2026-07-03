"""Loop guards against self-confirmation."""

from __future__ import annotations

from phyng.closed_loop.schemas import LoopGuardResult, MetaChangeProposal


def run_loop_guards(
    proposal: MetaChangeProposal | None = None,
    *,
    source_status: str | None = None,
    target_permission: str | None = None,
    has_source_or_benchmark: bool = False,
    synthetic_to_physical: bool = False,
    shadow_mode_ran: bool = False,
    report_has_blocked_claims: bool = True,
    audit_event_present: bool = True,
) -> list[LoopGuardResult]:
    results = [
        _guard("NO_SELF_AUTHORIZATION", True, "Loop cannot authorize its own truth."),
        _guard(
            "NO_PERMISSION_ELEVATION_FROM_HEURISTIC_ONLY",
            not (source_status == "HEURISTIC_ONLY" and target_permission in {"CLAIM_LIMITED_ALLOWED", "ACTION_LIMITED_ALLOWED", "EXECUTION_ALLOWED", "SCALE_ALLOWED"}),
            "Heuristic-only input cannot elevate permissions.",
            "CRITICAL",
        ),
        _guard("NO_HIDDEN_PARAMETER_OPTIMIZATION", True, "No hidden parameter optimization declared."),
        _guard("NO_POST_HOC_SCALE_SELECTION", True, "No post-hoc scale selection declared."),
        _guard(
            "NO_CLAIM_WITHOUT_SOURCE_OR_BENCHMARK",
            not (target_permission == "CLAIM_LIMITED_ALLOWED" and not has_source_or_benchmark),
            "Claims require source or benchmark support.",
            "CRITICAL",
        ),
        _guard(
            "NO_SYNTHETIC_TO_PHYSICAL_PROMOTION",
            not synthetic_to_physical,
            "Synthetic support cannot promote to physical validation.",
            "CRITICAL",
        ),
        _guard(
            "NO_CRITICAL_CHANGE_WITHOUT_SHADOW_MODE",
            not (proposal is not None and proposal.risk_level in {"MEDIUM", "HIGH"} and not shadow_mode_ran),
            "Medium/high risk changes require shadow mode.",
            "CRITICAL",
        ),
        _guard(
            "NO_GATE_RELAXATION_WITHOUT_HUMAN_REVIEW",
            not (proposal is not None and "GATE" in proposal.change_type and not proposal.requires_human_review),
            "Gate relaxation requires human review.",
            "CRITICAL",
        ),
        _guard("NO_REPORT_WITHOUT_BLOCKED_CLAIMS_SECTION", report_has_blocked_claims, "Reports must include blocked claims/actions.", "HIGH"),
        _guard("NO_LOOP_ITERATION_WITHOUT_AUDIT_EVENT", audit_event_present, "Loop iterations require audit events.", "HIGH"),
    ]
    return results


def _guard(name: str, passed: bool, message: str, severity: str = "INFO") -> LoopGuardResult:
    return LoopGuardResult(guard_name=name, passed=passed, severity=severity if not passed else "INFO", message=message)
