from phyng.campaigns.campaign_002_decoherence import (
    create_campaign_002_research_tasks,
    generate_foundational_source_ingestion_reports,
)
from phyng.rag.research_planner import list_research_tasks


def test_missing_sources_create_research_tasks(tmp_path):
    task_ids = create_campaign_002_research_tasks(tmp_path)
    tasks = list_research_tasks(tmp_path)

    assert "RT-CAMPAIGN-002-SRC-DECOH-001" in task_ids
    assert len(tasks) == 4
    assert all(task.status == "AWAITING_SOURCE_INGESTION" for task in tasks)


def test_source_ingestion_reports_do_not_claim_ingestion(tmp_path):
    task_ids = create_campaign_002_research_tasks(tmp_path)

    path = generate_foundational_source_ingestion_reports(tmp_path, task_ids)

    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "AWAITING_SOURCE_INGESTION" in text
    assert "No invented citations" in text
