import json
from pathlib import Path
from typing import Optional
from phyng.rag.schemas import ClaimRecord


def add_claim(record: ClaimRecord, root_dir: Path) -> None:
    claims_dir = root_dir / "rag" / "claims"
    claims_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = claims_dir / f"{record.claim_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(record.model_dump_json(indent=2))


def list_claims(root_dir: Path) -> list[ClaimRecord]:
    claims_dir = root_dir / "rag" / "claims"
    if not claims_dir.exists():
        return []
    
    records = []
    for file_path in claims_dir.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                records.append(ClaimRecord.model_validate(data))
        except Exception:
            continue
    return records


def get_claim(claim_id: str, root_dir: Path) -> Optional[ClaimRecord]:
    file_path = root_dir / "rag" / "claims" / f"{claim_id}.json"
    if not file_path.exists():
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return ClaimRecord.model_validate(data)
    except Exception:
        return None
