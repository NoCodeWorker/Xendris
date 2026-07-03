from pydantic import BaseModel
from typing import Literal, Optional
from phyng.enums import ClaimType, TraceType, Layer


class SourceRecord(BaseModel):
    source_id: str
    title: str
    authors: list[str] = []
    year: Optional[str] = None
    url: Optional[str] = None
    local_path: Optional[str] = None
    source_type: Literal[
        "PAPER",
        "BOOK",
        "LECTURE_NOTES",
        "OFFICIAL_DOC",
        "ENCYCLOPEDIC",
        "WEB_ARTICLE",
        "OTHER"
    ]
    trust_level: Literal["PRIMARY", "HIGH", "MEDIUM", "LOW"]
    relevance: Literal["HIGH", "MEDIUM", "LOW"]
    topics: list[str] = []
    used_for: list[str] = []
    notes: Optional[str] = None


class ClaimRecord(BaseModel):
    claim_id: str
    text: str
    claim_type: ClaimType
    layer: Layer
    trace_type: Optional[TraceType] = None
    status: Literal[
        "DRAFT",
        "REQUIRES_SOURCE",
        "REQUIRES_HIGHER_TRUST_SOURCE",
        "REQUIRES_MODEL",
        "REQUIRES_TRACE",
        "REQUIRES_SCALE_JUSTIFICATION",
        "REQUIRES_TEST",
        "ALLOWED_LIMITED",
        "ALLOWED",
        "BLOCKED",
        "CONTRADICTED"
    ]
    source_ids: list[str] = []
    test_ids: list[str] = []
    benchmark_ids: list[str] = []
    safe_rewrite: Optional[str] = None
    forbidden_interpretations: list[str] = []


class ClaimSourceLink(BaseModel):
    claim_id: str
    source_id: str
    support_level: Literal[
        "DIRECT_SUPPORT",
        "INDIRECT_SUPPORT",
        "BACKGROUND",
        "CONTRADICTS",
        "INSUFFICIENT"
    ]
    quote_or_note: str
    page_or_section: Optional[str] = None


class ResearchTask(BaseModel):
    task_id: str
    question: str
    reason: str
    linked_gap_id: str
    required_source_types: list[str] = []
    priority: Literal["P0", "P1", "P2", "P3"]
    expected_output: Literal[
        "SOURCE_RECORDS",
        "CLAIM_AUDIT",
        "LITERATURE_MAP",
        "BENCHMARK_BASELINE",
        "MODEL_COMPARISON"
    ]
    status: Literal[
        "TODO",
        "IN_PROGRESS",
        "DONE",
        "BLOCKED",
        "NO_TASK",
        "RESEARCH_TASK_CREATED",
        "AWAITING_SOURCE_INGESTION",
        "SOURCE_INGESTED",
        "CHUNKED",
        "CLAIM_LINKED",
        "CLAIM_AUDITED",
        "BACKLOG_UPDATED"
    ]

