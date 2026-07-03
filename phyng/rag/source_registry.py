import json
from pathlib import Path
from typing import Optional
from phyng.rag.schemas import SourceRecord


def add_source(record: SourceRecord, root_dir: Path) -> None:
    sources_dir = root_dir / "rag" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = sources_dir / f"{record.source_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(record.model_dump_json(indent=2))


def list_sources(root_dir: Path) -> list[SourceRecord]:
    sources_dir = root_dir / "rag" / "sources"
    if not sources_dir.exists():
        return []
    
    records = []
    for file_path in sources_dir.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                records.append(SourceRecord.model_validate(data))
        except Exception:
            # Skip invalid json files silently to be robust
            continue
    return records


def get_source(source_id: str, root_dir: Path) -> Optional[SourceRecord]:
    file_path = root_dir / "rag" / "sources" / f"{source_id}.json"
    if not file_path.exists():
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return SourceRecord.model_validate(data)
    except Exception:
        return None
