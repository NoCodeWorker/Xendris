from pydantic import BaseModel
from typing import Literal, Optional


class GapRecord(BaseModel):
    gap_id: str
    gap_type: Literal[
        "MISSING_TEST",
        "MISSING_SOURCE",
        "MISSING_CLAIM_LINK",
        "MISSING_BENCHMARK",
        "MISSING_MODEL",
        "MISSING_SCALE_JUSTIFICATION",
        "MISSING_TRACE",
        "MISSING_SAFE_REWRITE",
        "CLAIM_OVERREACH",
        "RAG_CONTRADICTION",
        "API_SCHEMA_GAP",
        "REPORT_GAP",
        "RAG_GAP",
        "CLAIM_RISK"
    ]
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    description: str
    recommended_action: str


class BacklogTask(BaseModel):
    task_id: str
    title: str
    task_type: str
    priority: Literal["P0", "P1", "P2", "P3"]
    status: Literal["TODO", "IN_PROGRESS", "DONE", "BLOCKED"]
    blocked_by: list[str] = []
    acceptance_criteria: list[str] = []
    linked_gap_id: Optional[str] = None



class IterationRecord(BaseModel):
    iteration_id: str
    timestamp: str
    gaps_found: list[GapRecord] = []
    backlog_tasks_created: list[BacklogTask] = []
    research_tasks_created: list[str] = []  # IDs of research tasks
    reports_written: list[str] = []        # file paths
    status: Literal["SUCCESS", "FAILED"]
