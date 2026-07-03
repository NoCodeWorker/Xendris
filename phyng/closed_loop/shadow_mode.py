"""Shadow mode for meta-change proposals."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.closed_loop.schemas import MetaChangeProposal, ShadowModeResult


def run_shadow_mode(proposal: MetaChangeProposal, sample_cases: list[dict]) -> ShadowModeResult:
    current_outputs = [dict(case.get("current_output", case)) for case in sample_cases]
    shadow_outputs = [dict(case.get("shadow_output", case.get("current_output", case))) for case in sample_cases]
    differences: list[dict] = []
    permission_differences: list[dict] = []
    blocked_reason_differences: list[dict] = []

    for index, (current, shadow) in enumerate(zip(current_outputs, shadow_outputs)):
        if current != shadow:
            differences.append({"index": index, "current": current, "shadow": shadow})
        if current.get("canonical_permission") != shadow.get("canonical_permission"):
            permission_differences.append({"index": index, "current": current.get("canonical_permission"), "shadow": shadow.get("canonical_permission")})
        if current.get("blocked_reasons") != shadow.get("blocked_reasons"):
            blocked_reason_differences.append({"index": index, "current": current.get("blocked_reasons"), "shadow": shadow.get("blocked_reasons")})

    warnings: list[str] = []
    recommendation = "SHADOW_APPROVED_NO_MUTATION"
    status = "META_CHANGE_APPROVED_LOW_RISK"
    if permission_differences:
        warnings.append("Permission differences detected in shadow mode.")
        recommendation = "BLOCK_OR_REVIEW"
        status = "META_CHANGE_BLOCKED_REGRESSION"

    return ShadowModeResult(
        proposal_id=proposal.proposal_id,
        current_outputs=current_outputs,
        shadow_outputs=shadow_outputs,
        differences=differences,
        permission_differences=permission_differences,
        blocked_reason_differences=blocked_reason_differences,
        regression_warnings=warnings,
        recommendation=recommendation,
        canonical_status=normalize_status(status, domain="closed_loop"),
    )
