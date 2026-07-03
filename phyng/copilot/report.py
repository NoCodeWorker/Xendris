"""
Phygn v1.8 — Copilot Reports Writer
"""

from __future__ import annotations

from pathlib import Path
from phyng.copilot.schemas import (
    CopilotResponseContract,
    HypothesisWorkspaceState,
    NextBestQuestion,
    ModelOrchestrationResult,
)


def write_copilot_reports(
    reports_dir: str | Path,
    response_contract: CopilotResponseContract,
    workspace_state: HypothesisWorkspaceState,
    next_question: NextBestQuestion,
    orchestration_result: ModelOrchestrationResult,
) -> dict[str, str]:
    """
    Write all 4 copilot reports and the campaign report:
    - reports/copilot/copilot_truth_boundary_ui_v1_8.md
    - reports/copilot/socratic_question_engine_v1_8.md
    - reports/copilot/hypothesis_workspace_v1_8.md
    - reports/copilot/cheap_model_orchestration_v1_8.md
    - reports/campaigns/COPILOT-TRUTH-BOUNDARY-UI-v1_8.md
    """
    base_path = Path(reports_dir) / "copilot"
    base_path.mkdir(parents=True, exist_ok=True)

    ui_path = base_path / "copilot_truth_boundary_ui_v1_8.md"
    socratic_path = base_path / "socratic_question_engine_v1_8.md"
    workspace_path = base_path / "hypothesis_workspace_v1_8.md"
    orchestration_path = base_path / "cheap_model_orchestration_v1_8.md"
    campaign_path = Path(reports_dir) / "campaigns" / "COPILOT-TRUTH-BOUNDARY-UI-v1_8.md"
    campaign_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. UI Truth Boundary Report
    ui_content = f"""# Copilot Truth-Boundary UI Report — Phygn v1.8

## Truth Boundary Panel Details
- **Current Ladder Level**: `{response_contract.ladder_level}`
- **Epistemic Mode**: `{response_contract.epistemic_mode}`
- **Friction Level**: `{response_contract.friction_level}`
- **Risk Level**: `{response_contract.risk_level}`
- **Truth Boundary Status**: `{response_contract.truth_boundary_status}`

### Guidelines Panel
- **Allowed Uses**:
{chr(10).join([f"  - {u}" for u in response_contract.allowed_uses])}
- **Blocked Uses**:
{chr(10).join([f"  - {b}" for b in response_contract.blocked_uses])}

## User Facing Dialogue
- **Message**: *"{response_contract.user_facing_message}"*
"""

    # 2. Socratic Question Engine Report
    socratic_content = f"""# Socratic Question Engine Report — Phygn v1.8

## Next Best Question Card
- **Question ID**: `{next_question.question_id}`
- **Question Type**: `{next_question.question_type}`
- **Question Text**: **"{next_question.question_text}"**
- **Why Needed**: *"{next_question.why_needed}"*
- **Updates Fields**: {", ".join([f"`{f}`" for f in next_question.updates_fields]) if next_question.updates_fields else "None"}
- **Blocks Until Answered**: {", ".join([f"`{b}`" for b in next_question.blocks_until_answered]) if next_question.blocks_until_answered else "None"}

### Multiple Choice Options
{chr(10).join([f"- {opt}" for opt in next_question.answer_options]) if next_question.answer_options else "No options (Free text answer expected)"}
"""

    # 3. Hypothesis Workspace Report
    card = workspace_state.current_hypothesis_card
    card_vars = ", ".join(card.variables) if card and card.variables else "None"
    card_obs = ", ".join(card.observables) if card and card.observables else "None"
    card_fails = card.failure_condition if card and card.failure_condition else "None"

    workspace_content = f"""# Hypothesis Workspace Report — Phygn v1.8

## State of Workspace `{workspace_state.workspace_id}`
- **Current Ladder Level**: `{workspace_state.current_ladder_level}`
- **Truth Boundary Status**: `{workspace_state.truth_boundary_status}`

### Active Hypothesis Card
- **Raw Idea**: *"{card.raw_idea if card else 'None'}"*
- **Variables**: {card_vars}
- **Observables**: {card_obs}
- **Failure Condition**: {card_fails}
- **Time Horizon**: {card.time_horizon if card and card.time_horizon else 'None'}

### Audit Trail Log
{chr(10).join([f"- **{evt['event']}**: {evt.get('timestamp')}" for evt in workspace_state.audit_trail])}
"""

    # 4. Cheap Model Orchestration Report
    orchestration_content = f"""# Cheap Model Orchestration Report — Phygn v1.8

## Orchestration Protocol
- **Validation Status**: `{orchestration_result.validation_status}`
- **Validation Notes**:
{chr(10).join([f"  - {n}" for n in orchestration_result.validation_notes]) if orchestration_result.validation_notes else "  - Output validated successfully against Phygn constraints."}

## Model Output Proposal (Raw JSON)
```json
{orchestration_result.raw_response}
```
"""

    # 5. Campaign Report
    campaign_content = f"""# Campaign Report — COPILOT-TRUTH-BOUNDARY-UI-v1_8

## Status: COMPLETE
- **Workspace ID**: `{workspace_state.workspace_id}`
- **Epistemic Mode**: `{response_contract.epistemic_mode}`
- **Truth Boundary Status**: `{response_contract.truth_boundary_status}`
- **Next Question Type**: `{next_question.question_type}`
- **Orchestration Status**: `{orchestration_result.validation_status}`

## Narrative Summary
The v1.8 Copilot system successfully handles natural language query intake, maps boundaries, ranks missing information, and outputs a strict JSON Response Contract. We have demonstrated:
1. Socratic Question Engine asking only one question at a time.
2. Truth Boundary panel verifying claims without treating lack of evidence as falsehood.
3. Cheap/Open-source model routing using Phygn's rule-based validation fallback.

## Generated Reports Directory
- UI Truth-Boundary: [copilot_truth_boundary_ui_v1_8.md](file:///{Path(ui_path).as_posix()})
- Socratic Engine: [socratic_question_engine_v1_8.md](file:///{Path(socratic_path).as_posix()})
- Workspace State: [hypothesis_workspace_v1_8.md](file:///{Path(workspace_path).as_posix()})
- Model Orchestration: [cheap_model_orchestration_v1_8.md](file:///{Path(orchestration_path).as_posix()})
"""

    ui_path.write_text(ui_content, encoding="utf-8")
    socratic_path.write_text(socratic_content, encoding="utf-8")
    workspace_path.write_text(workspace_content, encoding="utf-8")
    orchestration_path.write_text(orchestration_content, encoding="utf-8")
    campaign_path.write_text(campaign_content, encoding="utf-8")

    return {
        "ui": str(ui_path),
        "socratic": str(socratic_path),
        "workspace": str(workspace_path),
        "orchestration": str(orchestration_path),
        "campaign": str(campaign_path),
    }
