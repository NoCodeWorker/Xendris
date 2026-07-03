"""Risk-ranked refactor recommendation generation."""

from __future__ import annotations

from phyng.repository_audit.schemas import (
    RefactorRecommendation,
    RepositoryAuditResult,
)


def generate_refactor_map(audit_result: RepositoryAuditResult) -> list[RefactorRecommendation]:
    recommendations: list[RefactorRecommendation] = [
        RefactorRecommendation(
            title="Document current architecture before moving modules",
            description="Keep v2.0 as a discovery phase and preserve behavior while recording module boundaries and campaign/report/test contracts.",
            affected_modules=["docs", "reports/audit"],
            risk_level="DOCUMENT_ONLY",
            expected_benefit="Creates an explicit baseline for future canonicalization and rollback.",
            behavior_change_expected=False,
            requires_human_review=False,
            suggested_order=1,
        )
    ]

    if audit_result.status_strings:
        recommendations.append(
            RefactorRecommendation(
                title="Add canonical status mapping tables",
                description="Map discovered domain status strings to common permission, evidence, blocked-reason and risk concepts without replacing existing public literals.",
                affected_modules=["phyng/*/schemas.py", "reports/audit"],
                risk_level="LOW_RISK_EXTRACT_CONSTANTS",
                expected_benefit="Reduces semantic drift while keeping existing gate outputs stable.",
                behavior_change_expected=False,
                requires_human_review=False,
                suggested_order=2,
            )
        )

    if audit_result.enums:
        recommendations.append(
            RefactorRecommendation(
                title="Extract shared enum aliases only after duplicate proof",
                description="Where multiple domains define equivalent state families, introduce compatibility aliases before changing imports.",
                affected_modules=["phyng/epistemic_modes", "phyng/business_validation", "phyng/candidates"],
                risk_level="LOW_RISK_EXTRACT_ENUM",
                expected_benefit="Improves common grammar for gates without breaking report history.",
                behavior_change_expected=False,
                requires_human_review=False,
                suggested_order=3,
            )
        )

    recommendations.extend(
        [
            RefactorRecommendation(
                title="Unify report contract progressively",
                description="Introduce a shared report section checklist, then update report writers one domain at a time with snapshot tests.",
                affected_modules=["phyng/*/report.py", "reports/*"],
                risk_level="MEDIUM_RISK_REPORT_CONTRACT_UNIFICATION",
                expected_benefit="Makes campaign outputs comparable and easier to audit.",
                behavior_change_expected=False,
                requires_human_review=False,
                suggested_order=4,
            ),
            RefactorRecommendation(
                title="Defer module moves until contract tests exist",
                description="Do not move domain modules into a new core/domains topology until import boundaries and public API compatibility are covered.",
                affected_modules=["phyng"],
                risk_level="HIGH_RISK_MODULE_MOVE",
                expected_benefit="Avoids churn and broken historical imports while preserving a future migration path.",
                behavior_change_expected=True,
                requires_human_review=True,
                suggested_order=7,
            ),
            RefactorRecommendation(
                title="Block public API renames without migration ADR",
                description="Any rename of public schemas, statuses, campaign entrypoints or reports requires explicit human review and compatibility aliases.",
                affected_modules=["phyng", "frontend", "docs"],
                risk_level="HIGH_RISK_PUBLIC_API_CHANGE",
                expected_benefit="Protects downstream callers, reports and tests from silent behavior drift.",
                behavior_change_expected=True,
                requires_human_review=True,
                suggested_order=8,
            ),
        ]
    )
    return sorted(recommendations, key=lambda item: item.suggested_order)
