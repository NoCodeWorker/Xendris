"""ClaimExtractor parses text deterministically using markers or fallbacks."""

from __future__ import annotations

from typing import Any


class ClaimExtractor:
    """Parses text deterministically to extract claims using explicit text markers or conservative fallbacks."""

    @staticmethod
    def extract_claims(content: str, prefix: str = "EXT", default_context: str = "USER") -> list[dict[str, Any]]:
        """Parse structured text using CLAIM: and other markers, or create fallback claim."""
        claims: list[dict[str, Any]] = []
        current_claim: dict[str, Any] | None = None

        for line in content.splitlines():
            line_str = line.strip()
            if not line_str:
                continue

            if line_str.startswith("CLAIM:"):
                if current_claim is not None:
                    claims.append(current_claim)
                current_claim = {
                    "content": line_str[6:].strip(),
                    "claim_type": "FACTUAL",
                    "epistemic_sector": "FACTUAL",
                    "local_context": "PRODUCTION",
                    "evidence_refs": [],
                    "limitations": [],
                    "risk_level": "LOW",
                }
            elif current_claim is not None:
                if line_str.startswith("CLAIM_TYPE:"):
                    current_claim["claim_type"] = line_str[11:].strip()
                elif line_str.startswith("SECTOR:"):
                    current_claim["epistemic_sector"] = line_str[7:].strip()
                elif line_str.startswith("CONTEXT:"):
                    current_claim["local_context"] = line_str[8:].strip()
                elif line_str.startswith("EVIDENCE:"):
                    current_claim["evidence_refs"].append(line_str[9:].strip())
                elif line_str.startswith("LIMITATION:"):
                    current_claim["limitations"].append(line_str[11:].strip())
                elif line_str.startswith("RISK:"):
                    current_claim["risk_level"] = line_str[5:].strip()

        if current_claim is not None:
            claims.append(current_claim)

        # Fallback if no explicit markers found
        if not claims:
            claims.append({
                "content": content,
                "claim_type": "INFERRED",
                "epistemic_sector": "HYPOTHESIS",
                "local_context": default_context,
                "evidence_refs": [],
                "limitations": ["Conservative fallback claim, unverified output"],
                "risk_level": "LOW",
            })

        # Apply deterministic IDs and build finalized dictionaries
        final_claims: list[dict[str, Any]] = []
        for idx, c in enumerate(claims):
            final_claims.append({
                "claim_id": f"{prefix}-{idx+1}",
                "content": c["content"],
                "claim_type": c["claim_type"],
                "epistemic_sector": c["epistemic_sector"],
                "local_context": c["local_context"],
                "evidence_refs": tuple(c["evidence_refs"]),
                "limitations": tuple(c["limitations"]),
                "risk_level": c["risk_level"],
            })

        return final_claims
