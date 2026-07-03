"""
Phygn v1.7 — UX Report Generator
"""

from __future__ import annotations

from pathlib import Path
from phyng.ux.idea_intake import HypothesisSeedCard, MathTranslatorOutput


def write_ux_reports(
    reports_dir: str | Path,
    seed_card: HypothesisSeedCard,
    translator_output: MathTranslatorOutput,
) -> dict[str, str]:
    """
    Write the two UX reports:
    - reports/ux/idea_to_hypothesis_flow_v1_7.md
    - reports/ux/hypothesis_seed_cards_v1_7.md
    """
    base_path = Path(reports_dir) / "ux"
    base_path.mkdir(parents=True, exist_ok=True)

    flow_path = base_path / "idea_to_hypothesis_flow_v1_7.md"
    cards_path = base_path / "hypothesis_seed_cards_v1_7.md"

    # Flow report
    flow_content = f"""# Idea-to-Hypothesis Flow Report — Phygn v1.7

## Process Overview
This report demonstrates the transition of a raw natural language intuition into a structured, testable hypothesis seed.

### Step 1: Raw Intake
- **Idea ID**: `{seed_card.idea_id}`
- **Raw Intuition**: *"{seed_card.raw_intuition}"*

### Step 2: Cleaned Hypothesis
- **Cleaned Statement**: {seed_card.cleaned_hypothesis}

### Step 3: Math Translation ({translator_output.label})
- **Possible X Variables**: {", ".join([f"`{x}`" for x in translator_output.possible_x_variables])}
- **Possible Y Observables**: {", ".join([f"`{y}`" for y in translator_output.possible_y_observables])}
- **Proxy Candidates**: {", ".join([f"`{p}`" for p in translator_output.proxy_candidates])}
- **Baseline Candidates**: {", ".join([f"`{b}`" for b in translator_output.baseline_candidates])}
- **Failure Conditions**: {", ".join([f"`{f}`" for f in translator_output.failure_condition_candidates])}

## UX Permitted and Blocked Actions
- **Allowed Uses**:
{chr(10).join([f"  - {use}" for use in seed_card.allowed_uses])}
- **Blocked Uses**:
{chr(10).join([f"  - {use}" for use in seed_card.blocked_uses])}
"""

    # Seed card report
    card_content = f"""# Hypothesis Seed Card — {seed_card.seed_id}

## Metadata
- **Seed ID**: `{seed_card.seed_id}`
- **Idea ID**: `{seed_card.idea_id}`
- **Title**: **{seed_card.title}**
- **Current Ladder Level**: `{seed_card.current_ladder_level}`
- **UX Status**: `{seed_card.ux_status}`
- **Proposal Label**: `{seed_card.proposal_label}`

## Cleaned Hypothesis
{seed_card.cleaned_hypothesis}

## Candidate Variables & Observables
- **Candidate Variables**:
{chr(10).join([f"  - {v}" for v in seed_card.candidate_variables])}
- **Candidate Observables**:
{chr(10).join([f"  - {o}" for o in seed_card.candidate_observables])}
- **Candidate Proxies**:
{chr(10).join([f"  - {p}" for p in seed_card.candidate_proxies])}

## Formalization Gap Analysis
- **Missing Information**:
{chr(10).join([f"  - {m}" for m in seed_card.missing_information])}

## Next Best Questions for User Review
{chr(10).join([f"- {q}" for q in seed_card.next_best_questions])}

## Minimum Test Plan
{chr(10).join([f"- {t}" for t in seed_card.minimum_test_plan])}
"""

    flow_path.write_text(flow_content, encoding="utf-8")
    cards_path.write_text(card_content, encoding="utf-8")

    return {
        "flow": str(flow_path),
        "cards": str(cards_path),
    }
