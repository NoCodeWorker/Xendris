"""TrustLedgerExporter for exporting records in JSON, JSONL, and Markdown."""

from __future__ import annotations

import json
from xendris.core.ledger.record import TrustLedgerRecord
from xendris.core.ledger.event_type import TrustEventType


class TrustLedgerExporter:
    """Exports ledger records to multiple persistent formats."""

    @staticmethod
    def export_jsonl(records: list[TrustLedgerRecord], path: str) -> None:
        """Export records to a JSONL file."""
        with open(path, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r.to_dict()) + "\n")

    @staticmethod
    def export_json(records: list[TrustLedgerRecord], path: str) -> None:
        """Export records to a single formatted JSON file."""
        serializable = [r.to_dict() for r in records]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2, sort_keys=True)

    @staticmethod
    def export_markdown_summary(records: list[TrustLedgerRecord], path: str) -> None:
        """Compile and write a Markdown summary of the ledger records."""
        total = len(records)
        event_counts: dict[str, int] = {}
        blocked = 0
        human_review = 0
        selected: set[str] = set()
        rejected: set[str] = set()
        limitations: set[str] = set()

        for r in records:
            name = r.event_type.name
            event_counts[name] = event_counts.get(name, 0) + 1
            if r.decision == "BLOCK" or r.decision == "BLOCKED" or r.event_type == TrustEventType.CLAIM_BLOCKED:
                blocked += 1
            elif r.decision == "HUMAN_REVIEW" or r.decision == "HUMAN_REVIEW_REQUIRED" or r.event_type == TrustEventType.HUMAN_REVIEW_ROUTED:
                human_review += 1

            if r.model_id:
                if r.event_type == TrustEventType.MODEL_SELECTED:
                    selected.add(r.model_id)
                elif r.event_type == TrustEventType.MODEL_REJECTED:
                    rejected.add(r.model_id)

            for limit in r.limitations:
                limitations.add(limit)

        md = [
            "# Xendris Trust Ledger Run Summary",
            "",
            f"**Total Records**: {total}",
            "",
            "## Records by Event Type",
            "",
        ]
        
        for name, count in sorted(event_counts.items()):
            md.append(f"* **{name}**: {count}")
            
        md.extend([
            "",
            f"**Blocked Claims**: {blocked}",
            f"**Human Review Count**: {human_review}",
            "",
            "## Selected Models",
            "",
        ])
        
        for m in sorted(selected):
            md.append(f"* {m}")
        if not selected:
            md.append("*No models selected.*")
            
        md.extend([
            "",
            "## Rejected Models",
            "",
        ])
        
        for m in sorted(rejected):
            md.append(f"* {m}")
        if not rejected:
            md.append("*No models rejected.*")

        md.extend([
            "",
            "## Limitations Summary",
            "",
        ])
        
        for limit in sorted(limitations):
            md.append(f"* {limit}")
        if not limitations:
            md.append("*No limitations recorded.*")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")
