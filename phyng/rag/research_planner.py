import json
from pathlib import Path
from typing import Optional
from phyng.rag.schemas import ResearchTask, ClaimRecord


def save_research_task(task: ResearchTask, root_dir: Path) -> None:
    tasks_dir = root_dir / "rag" / "research_tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = tasks_dir / f"{task.task_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(task.model_dump_json(indent=2))


def list_research_tasks(root_dir: Path) -> list[ResearchTask]:
    tasks_dir = root_dir / "rag" / "research_tasks"
    if not tasks_dir.exists():
        return []
    
    tasks = []
    for file_path in tasks_dir.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                tasks.append(ResearchTask.model_validate(data))
        except Exception:
            continue
    return tasks


def plan_research_for_claim(claim: ClaimRecord, gap_id: str, root_dir: Path) -> Optional[ResearchTask]:
    if claim.status not in ["REQUIRES_SOURCE", "REQUIRES_HIGHER_TRUST_SOURCE"]:
        return None
        
    task_id = f"RSC_TASK_{claim.claim_id}"
    question = f"What is the physical/literature grounding for: {claim.text}?"
    reason = f"Claim has status {claim.status} and needs verified bibliography."
    
    # Map required source types
    req_types = ["PAPER", "BOOK"]
    if claim.layer == "SPECULATIVE_ONLY":
        req_types.append("WEB_ARTICLE")
        
    priority = "P1"
    if claim.layer == "PHYSICAL_CORE":
        priority = "P0"
        
    task = ResearchTask(
        task_id=task_id,
        question=question,
        reason=reason,
        linked_gap_id=gap_id,
        required_source_types=req_types,
        priority=priority,
        expected_output="SOURCE_RECORDS",
        status="TODO"
    )
    
    save_research_task(task, root_dir)
    return task
