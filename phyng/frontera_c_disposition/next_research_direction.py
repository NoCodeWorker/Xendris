"""Next research direction after v5.6 disposition."""

from __future__ import annotations

from phyng.frontera_c_disposition.schemas import BlockedClaims, FronteraCRoadmapUpdate, NextResearchDirection


def build_next_research_direction(roadmap: FronteraCRoadmapUpdate, claims: BlockedClaims) -> NextResearchDirection:
    return NextResearchDirection(
        final_status="LOG_BOUNDARY_ARCHIVED_AS_VALIDATION_CANDIDATE",
        selected_next_direction=roadmap.recommended_path,
        allowed_next_phase="v5.7 - Visibility/Decoherence Dataset Expansion",
        blocked_next_phases=[
            "v5.6 - C-Structure Ablation Gate for LOG_BOUNDARY",
            "Frontera C validation from LOG_BOUNDARY",
            "Physical claim generation",
        ],
        required_inputs=[
            "Additional independent visibility/decoherence sources",
            "At least 10 accepted y_true records before LOG_BOUNDARY reconsideration",
            "Out-of-sample or leave-one-source-out evaluation design",
            "Negative controls that simple controls do not explain",
        ],
        rationale=roadmap.rationale,
        blocked_claims=claims.blocked_claims,
        allowed_claims=claims.allowed_claims,
        notes=[
            "v5.7 may expand the dataset but must not rescue LOG_BOUNDARY as an active validation candidate.",
            "No validation is permitted from v5.6.",
        ],
    )
