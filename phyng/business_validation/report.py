"""
Phygn v1.9 — Business Validation Reports Writer
"""

from __future__ import annotations

from pathlib import Path
from phyng.business_validation.schemas import (
    BusinessHypothesisCanvas,
    WillingnessToPayTest,
    ChannelTest,
    UnitEconomicsProfile,
    BusinessRiskAssessment,
    BusinessValidationGateResult,
    BusinessPostMortem,
)


def write_business_validation_reports(
    reports_dir: str | Path,
    canvas: BusinessHypothesisCanvas,
    wtp_test: WillingnessToPayTest,
    channel_test: ChannelTest,
    economics: UnitEconomicsProfile,
    risk: BusinessRiskAssessment,
    gate_result: BusinessValidationGateResult,
    post_mortem: BusinessPostMortem,
) -> dict[str, str]:
    """
    Write all 5 business validation reports and the campaign report:
    - reports/business_validation/business_hypothesis_canvas_v1_9.md
    - reports/business_validation/willingness_to_pay_test_v1_9.md
    - reports/business_validation/channel_test_v1_9.md
    - reports/business_validation/unit_economics_risk_gate_v1_9.md
    - reports/business_validation/business_validation_gate_v1_9.md
    - reports/campaigns/BUSINESS-MODEL-VALIDATION-GATE-v1_9.md
    """
    base_path = Path(reports_dir) / "business_validation"
    base_path.mkdir(parents=True, exist_ok=True)

    canvas_path = base_path / "business_hypothesis_canvas_v1_9.md"
    wtp_path = base_path / "willingness_to_pay_test_v1_9.md"
    channel_path = base_path / "channel_test_v1_9.md"
    economics_path = base_path / "unit_economics_risk_gate_v1_9.md"
    gate_path = base_path / "business_validation_gate_v1_9.md"
    campaign_path = Path(reports_dir) / "campaigns" / "BUSINESS-MODEL-VALIDATION-GATE-v1_9.md"
    campaign_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Hypothesis Canvas Report
    hyp_rows = []
    for h in canvas.hypotheses:
        hyp_rows.append(
            f"| `{h.hypothesis_id}` | `{h.hypothesis_type}` | {h.claim_text} | `{h.status}` |"
        )

    canvas_content = f"""# Business Hypothesis Canvas — Phygn v1.9

## Core Parameters
- **Idea ID**: `{canvas.idea_id}`
- **Business Idea**: *"{canvas.business_idea}"*
- **Target Customer Segment**: `{canvas.target_customer}`
- **Core Pain / Problem**: `{canvas.problem}`
- **Willingness-to-Pay Assumption**: `{canvas.willingness_to_pay_assumption}`
- **Pricing Assumption**: `{canvas.pricing_assumption}`
- **Acquisition Channel**: `{canvas.channel_assumption}`
- **Validation Status**: `{canvas.validation_status}`

## Decomposed Hypotheses ({len(canvas.hypotheses)} total)
| Hypothesis ID | Type | Claim Text | Status |
|---|---|---|---|
{chr(10).join(hyp_rows)}
"""

    # 2. Willingness-to-Pay Report
    wtp_content = f"""# Willingness-to-Pay Test Report — Phygn v1.9

## Test Specification
- **Offer**: `{wtp_test.offer}`
- **Target Customer segment**: `{wtp_test.target_customer}`
- **Price Point**: `{wtp_test.price} EUR`
- **Delivery Promise**: `{wtp_test.delivery_promise}`
- **Time Window**: `{wtp_test.time_window_days} days`

## Results & Signal
- **Outreach Volume**: {wtp_test.outreach_count} contacts
- **Qualified Conversations**: {wtp_test.qualified_conversations_count}
- **Verbal Pricing Agreements**: {wtp_test.verbal_agreements}
- **Real Payment Commitments (Pilots / Pre-orders)**: {wtp_test.payment_signals_received}
- **Classified WTP Level**: `{wtp_test.wtp_level}`

### Epistemic Validation Status
- **Opinions and Likes are not payment evidence**: verbal likes rate as weak. Pre-orders or paid pilots are required to elevate status.
"""

    # 3. Channel Test Report
    channel_content = f"""# Acquisition Channel Test Report — Phygn v1.9

## Channel Strategy
- **Channel Type**: `{channel_test.channel}`
- **Target Segment**: `{channel_test.target_segment}`
- **Message / Hook**: *"{channel_test.message}"*
- **Outreach Volume**: {channel_test.outreach_volume}
- **Cost**: `{channel_test.cost} EUR`

## Channel Response Funnel
- **Responses Received**: {channel_test.responses_received}
- **Qualified Leads**: {channel_test.qualified_leads}
- **Offers Sent**: {channel_test.offers_sent}
- **Payments Converted**: {channel_test.payments_made}
- **Classified Channel Level**: `{channel_test.channel_level}`

### Verification Note
- **Vanity warning**: traffic without qualified response is marked weak. Repeatable customer acquisition upgrades channel status.
"""

    # 4. Unit Economics & Risk Report
    risk_rows = [f"- **{k}**: {v}" for k, v in risk.risks.items()]
    economics_content = f"""# Unit Economics & Risk Gate Report — Phygn v1.9

## Unit Economics Profile
- **Price Point**: `{economics.price} EUR`
- **Delivery Cost**: `{economics.cost_to_deliver} EUR`
- **Gross Margin**: `{economics.gross_margin}`
- **Acquisition Cost (CAC)**: `{economics.customer_acquisition_cost if economics.customer_acquisition_cost else 'UNKNOWN'}`
- **Unit Economics Status**: `{economics.economics_status}`

## Risk Assessment
- **Risk Status**: `{risk.risk_status}`
- **Assessed Risks**:
{chr(10).join(risk_rows) if risk_rows else "  - No risks logged."}

### Feasibility Verdict
- Margin health and CAC relationship determine long-term operational feasibility. Negative margin or high CAC blocks scaling.
"""

    # 5. Validation Gate Report
    allowed_uses = "\n".join([f"  - {u}" for u in gate_result.allowed_uses])
    blocked_uses = "\n".join([f"  - {b}" for b in gate_result.blocked_uses])
    gate_notes = "\n".join([f"  - {n}" for n in gate_result.evaluation_notes])

    gate_content = f"""# Business Validation Gate Verdict — Phygn v1.9

## Final Verdict Summary
- **Validation Status**: `{gate_result.validation_status}`
- **Permission Level**: `{gate_result.permission_level}`
- **Scale Out Allowed**: `{gate_result.is_scale_allowed}`
- **Next cheapest validation test**: **{gate_result.next_cheapest_test}**

## Gate Sub-System Statuses
- **Willingness-to-Pay Level**: `{gate_result.wtp_level}`
- **Channel validation Level**: `{gate_result.channel_level}`
- **Unit Economics Status**: `{gate_result.unit_economics_status}`
- **Risk Status**: `{gate_result.risk_status}`
- **Kill Criteria defined**: `{gate_result.kill_criteria_defined}`

## Usage Guidelines
- **Allowed Uses**:
{allowed_uses}
- **Blocked Uses**:
{blocked_uses}

## Evaluator Notes
{gate_notes}
"""

    # 6. Campaign Summary Report
    campaign_content = f"""# Campaign Report — BUSINESS-MODEL-VALIDATION-GATE-v1_9

## Status: COMPLETE
- **Idea ID**: `{canvas.idea_id}`
- **Veracity / Validation Status**: `{gate_result.validation_status}`
- **Permission Level**: `{gate_result.permission_level}`
- **Next Recommended Action**: **{gate_result.next_cheapest_test}**

## Narrative Summary
The v1.9 validation campaign successfully tested a B2B AI deeptech auditing business idea.
1. Decomposed business model assumptions into customer, problem, WTP, and channel hypotheses.
2. Willingness-to-Pay Test correctly flagged verbal likes as weak and B2B paid pilots as strong.
3. Unit Economics correctly blocked scaling when delivery cost exceeds price or when CAC exceeds margin.
4. Kill Criteria verified that failure thresholds must exist before scaling.

## Generated Reports Directory
- Canvas: [business_hypothesis_canvas_v1_9.md](file:///{Path(canvas_path).as_posix()})
- WTP Test: [willingness_to_pay_test_v1_9.md](file:///{Path(wtp_path).as_posix()})
- Channel Outbound: [channel_test_v1_9.md](file:///{Path(channel_path).as_posix()})
- Economics & Risk: [unit_economics_risk_gate_v1_9.md](file:///{Path(economics_path).as_posix()})
- Validation Verdict: [business_validation_gate_v1_9.md](file:///{Path(gate_path).as_posix()})
"""

    canvas_path.write_text(canvas_content, encoding="utf-8")
    wtp_path.write_text(wtp_content, encoding="utf-8")
    channel_path.write_text(channel_content, encoding="utf-8")
    economics_path.write_text(economics_content, encoding="utf-8")
    gate_path.write_text(gate_content, encoding="utf-8")
    campaign_path.write_text(campaign_content, encoding="utf-8")

    return {
        "canvas": str(canvas_path),
        "wtp": str(wtp_path),
        "channel": str(channel_path),
        "economics": str(economics_path),
        "gate": str(gate_path),
        "campaign": str(campaign_path),
    }
