from pydantic import BaseModel, Field
from pathlib import Path


class SourceCandidate(BaseModel):
    source_candidate_id: str
    requirement_id: str
    title: str | None = None
    authors: list[str] = Field(default_factory=list)
    year: str | None = None
    source_type: str = "PAPER"
    local_path: str | None = None
    url: str | None = None
    trust_level: str = "MEDIUM"
    # CANDIDATE_ONLY | CANDIDATE_REGISTERED | LOCAL_FILE_AVAILABLE | METADATA_INCOMPLETE | READY_FOR_AUDIT | REJECTED
    candidate_status: str = "CANDIDATE_REGISTERED"
    notes: str | None = None


def evaluate_candidate_status(candidate: SourceCandidate) -> str:
    """
    Evaluates candidate status based on rules:
    - URL-only candidate -> CANDIDATE_ONLY, not ingested.
    - Missing local file -> CANDIDATE_REGISTERED, not ingested.
    - Local file available -> LOCAL_FILE_AVAILABLE.
    - Metadata incomplete -> METADATA_INCOMPLETE (if title, authors, or year is missing).
    - Ready source -> READY_FOR_AUDIT.
    """
    # 1. Check metadata completeness
    metadata_complete = (
        candidate.title is not None and len(candidate.title.strip()) > 0 and
        len(candidate.authors) > 0 and
        candidate.year is not None and len(candidate.year.strip()) > 0
    )
    
    # 2. Check local file vs URL
    if candidate.local_path:
        local_file = Path(candidate.local_path)
        if local_file.exists() and local_file.is_file():
            if not metadata_complete:
                return "METADATA_INCOMPLETE"
            return "READY_FOR_AUDIT"
        else:
            return "CANDIDATE_REGISTERED"
    else:
        if candidate.url:
            return "CANDIDATE_ONLY"
        return "CANDIDATE_REGISTERED"
