"""Canonical report contract helpers."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from phyng.core.compatibility import normalize_status
from phyng.core.status_mapping import CanonicalStatusRecord


class CanonicalReportContract(BaseModel):
    title: str
    date: str
    campaign_id: str | None = None
    domain_status: str
    canonical_permission: str
    blocked_reasons: list[str] = Field(default_factory=list)
    evidence_level: str
    support_level: str
    risk_level: str | None = None
    allowed_uses: list[str] = Field(default_factory=list)
    blocked_uses: list[str] = Field(default_factory=list)
    failure_conditions: list[str] = Field(default_factory=list)
    tests_summary: str | None = None
    reports_generated: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    discipline_note: str


def build_report_contract(
    title: str,
    domain_status: str,
    campaign_id: str | None = None,
    domain: str | None = None,
    allowed_uses: list[str] | None = None,
    blocked_uses: list[str] | None = None,
    failure_conditions: list[str] | None = None,
    tests_summary: str | None = None,
    reports_generated: list[str] | None = None,
    next_actions: list[str] | None = None,
    discipline_note: str = "Canonicalization increases clarity without erasing domain meaning.",
    generated_date: str | None = None,
) -> CanonicalReportContract:
    record = normalize_status(domain_status, domain)
    return _contract_from_record(
        title=title,
        record=record,
        campaign_id=campaign_id,
        allowed_uses=allowed_uses,
        blocked_uses=blocked_uses,
        failure_conditions=failure_conditions,
        tests_summary=tests_summary,
        reports_generated=reports_generated,
        next_actions=next_actions,
        discipline_note=discipline_note,
        generated_date=generated_date,
    )


def render_canonical_report_section(contract: CanonicalReportContract) -> str:
    lines = [
        "## Canonical Status",
        "",
        f"- Domain Status: `{contract.domain_status}`",
        f"- Canonical Permission: `{contract.canonical_permission}`",
        f"- Blocked Reasons: `{_csv(contract.blocked_reasons)}`",
        f"- Evidence Level: `{contract.evidence_level}`",
        f"- Support Level: `{contract.support_level}`",
        f"- Risk Level: `{contract.risk_level or 'None'}`",
        "",
        "### Allowed Uses",
        "",
        *_bullets(contract.allowed_uses),
        "",
        "### Blocked Uses",
        "",
        *_bullets(contract.blocked_uses),
        "",
        "### Next Actions",
        "",
        *_bullets(contract.next_actions),
        "",
        "### Discipline Note",
        "",
        contract.discipline_note,
    ]
    return "\n".join(lines) + "\n"


def append_canonical_status_section(markdown: str, contract: CanonicalReportContract) -> str:
    body = markdown.rstrip()
    return body + "\n\n---\n\n" + render_canonical_report_section(contract)


def _contract_from_record(
    title: str,
    record: CanonicalStatusRecord,
    campaign_id: str | None,
    allowed_uses: list[str] | None,
    blocked_uses: list[str] | None,
    failure_conditions: list[str] | None,
    tests_summary: str | None,
    reports_generated: list[str] | None,
    next_actions: list[str] | None,
    discipline_note: str,
    generated_date: str | None,
) -> CanonicalReportContract:
    return CanonicalReportContract(
        title=title,
        date=generated_date or date.today().isoformat(),
        campaign_id=campaign_id,
        domain_status=record.domain_status,
        canonical_permission=record.canonical_permission.value,
        blocked_reasons=[reason.value for reason in record.blocked_reasons],
        evidence_level=record.evidence_level.value,
        support_level=record.support_level.value,
        risk_level=record.risk_level.value if record.risk_level else None,
        allowed_uses=allowed_uses if allowed_uses is not None else list(record.allowed_uses),
        blocked_uses=blocked_uses if blocked_uses is not None else list(record.blocked_uses),
        failure_conditions=failure_conditions or [],
        tests_summary=tests_summary,
        reports_generated=reports_generated or [],
        next_actions=next_actions if next_actions is not None else list(record.next_actions),
        discipline_note=discipline_note,
    )


def _bullets(items: list[str]) -> list[str]:
    if not items:
        return ["- None"]
    return [f"- {item}" for item in items]


def _csv(items: list[str]) -> str:
    return ", ".join(items) if items else "None"
