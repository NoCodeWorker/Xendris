from pathlib import Path

from phyng.evidence.schemas import SourceIngestionResult, SourceRequirement
from phyng.evidence.source_requirements import create_research_tasks_for_requirements
from phyng.rag.source_registry import get_source


def plan_source_ingestion(
    requirement: SourceRequirement,
    root_dir: Path,
    source_id: str | None = None,
) -> SourceIngestionResult:
    if source_id is None:
        create_research_tasks_for_requirements([requirement], root_dir)
        return SourceIngestionResult(
            requirement_id=requirement.requirement_id,
            source_id=None,
            status="REQUIRES_SOURCE",
            action="CREATE_REQUIREMENT_AND_RESEARCH_TASK",
            reason="No concrete source was provided; source ingestion is not asserted.",
            blocked_claims=requirement.linked_claim_ids,
            next_steps=[
                "Find a real source file or bibliographic record.",
                "Create SourceRecord only from actual metadata.",
                "Link direct support before unlocking hard claims.",
            ],
        )

    source = get_source(source_id, root_dir)
    if source is None:
        create_research_tasks_for_requirements([requirement], root_dir)
        return SourceIngestionResult(
            requirement_id=requirement.requirement_id,
            source_id=None,
            status="SOURCE_NOT_FOUND",
            action="BLOCK_FAKE_SOURCE_RECORD",
            reason=f"Source ID {source_id} does not exist in the registry.",
            blocked_claims=requirement.linked_claim_ids,
            next_steps=["Register a real source before claiming ingestion."],
        )

    return SourceIngestionResult(
        requirement_id=requirement.requirement_id,
        source_id=source.source_id,
        status="CANDIDATE_FOUND",
        action="AUDIT_SOURCE_BEFORE_UNLOCK",
        reason="A source record exists, but claim links and support audit are still required.",
        created_claim_links=[],
        blocked_claims=requirement.linked_claim_ids,
        next_steps=["Create ClaimSourceLink records.", "Run evidence audit."],
    )
