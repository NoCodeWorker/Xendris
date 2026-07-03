from phyng.evidence import default_source_requirements, plan_source_ingestion
from phyng.rag.research_planner import list_research_tasks


def test_no_fake_metadata_allowed(tmp_path):
    requirement = default_source_requirements()[0]

    result = plan_source_ingestion(requirement, tmp_path, source_id="SRC-DOES-NOT-EXIST")

    assert result.source_id is None
    assert result.status == "SOURCE_NOT_FOUND"
    assert result.action == "BLOCK_FAKE_SOURCE_RECORD"
    assert requirement.linked_claim_ids == result.blocked_claims


def test_missing_source_creates_research_task(tmp_path):
    requirement = default_source_requirements()[0]

    result = plan_source_ingestion(requirement, tmp_path)
    tasks = list_research_tasks(tmp_path)

    assert result.status == "REQUIRES_SOURCE"
    assert len(tasks) == 1
    assert tasks[0].linked_gap_id == "REQ-SRC-001"
