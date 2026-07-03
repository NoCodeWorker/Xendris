"""Campaign orchestration audit."""

from __future__ import annotations

from pathlib import Path

from phyng.repository_audit.schemas import CampaignAuditRecord


def audit_campaigns(root: Path) -> list[CampaignAuditRecord]:
    root = Path(root)
    campaign_dir = root / "phyng" / "campaigns"
    records: list[CampaignAuditRecord] = []
    if not campaign_dir.exists():
        return records

    test_texts = {
        str(p.relative_to(root)).replace("\\", "/"): p.read_text(encoding="utf-8", errors="ignore")
        for p in (root / "tests").glob("test_*.py")
    }
    reports = sorted(str(p.relative_to(root)).replace("\\", "/") for p in (root / "reports" / "campaigns").glob("*.md"))

    for path in sorted(campaign_dir.glob("*.py")):
        if path.name == "__init__.py":
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        text = path.read_text(encoding="utf-8", errors="ignore")
        stem = path.stem
        campaign_id = _campaign_id(stem, text)
        module_hint = f"phyng.campaigns.{stem}"
        matched_tests = sorted(
            test_rel for test_rel, body in test_texts.items()
            if module_hint in body or stem in test_rel or stem in body
        )
        matched_reports = [report for report in reports if _report_matches(report, stem, campaign_id)]
        gatekeepers = sorted(
            line.strip()
            for line in text.splitlines()
            if "gate" in line.lower() and ("import" in line or "=" in line or "(" in line)
        )[:20]
        warnings: list[str] = []
        if not matched_tests:
            warnings.append("No direct campaign tests detected.")
        if not matched_reports:
            warnings.append("No existing campaign report mapped by heuristic.")
        records.append(
            CampaignAuditRecord(
                campaign_id=campaign_id,
                entrypoint=rel,
                reports=matched_reports,
                gatekeepers=gatekeepers,
                tests=matched_tests,
                warnings=warnings,
            )
        )
    return records


def _campaign_id(stem: str, text: str) -> str:
    for line in text.splitlines():
        if "CAMPAIGN" in line and ("=" in line or "campaign_id" in line):
            tokens = [token.strip("\"',`() ") for token in line.replace("=", " ").split()]
            for token in tokens:
                if "CAMPAIGN" in token and len(token) > 8:
                    return token
    return stem.replace("_", "-").upper()


def _report_matches(report: str, stem: str, campaign_id: str) -> bool:
    normalized_report = report.lower().replace("-", "_")
    normalized_stem = stem.lower()
    normalized_id = campaign_id.lower().replace("-", "_")
    return normalized_stem in normalized_report or normalized_id in normalized_report
