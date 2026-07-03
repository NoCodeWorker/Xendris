import json
from pathlib import Path
from phyng.evidence.source_candidates import SourceCandidate, evaluate_candidate_status


def scan_local_sources(project_root: Path) -> list[SourceCandidate]:
    """
    Scans sources/baseline/ directory in project_root.
    Reads source_manifest.json if present, registering entries as candidates.
    If no manifest exists, registers any file found as a SourceCandidate.
    """
    baseline_dir = project_root / "sources" / "baseline"
    if not baseline_dir.exists() or not baseline_dir.is_dir():
        return []
        
    candidates = []
    manifest_path = baseline_dir / "source_manifest.json"
    
    # 1. Load from manifest if present
    if manifest_path.exists() and manifest_path.is_file():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for idx, entry in enumerate(data):
                    cand_id = entry.get("source_candidate_id", f"CAND-BASE-{idx+1:03d}")
                    req_id = entry.get("requirement_id", "BSR-001")
                    title = entry.get("title")
                    authors = entry.get("authors", [])
                    year = entry.get("year")
                    source_type = entry.get("source_type", "PAPER")
                    local_path = entry.get("local_path")
                    url = entry.get("url")
                    trust = entry.get("trust_level", "HIGH")
                    notes = entry.get("notes")
                    
                    # Form Candidate
                    cand = SourceCandidate(
                        source_candidate_id=cand_id,
                        requirement_id=req_id,
                        title=title,
                        authors=authors,
                        year=year,
                        source_type=source_type,
                        local_path=local_path,
                        url=url,
                        trust_level=trust,
                        notes=notes
                    )
                    # Evaluate status dynamically using actual file existence
                    # Statically local_path in manifest might be relative to project_root
                    if cand.local_path:
                        resolved_path = project_root / cand.local_path
                        # Temp change to let evaluate_candidate_status use resolved path check
                        actual_path = cand.local_path
                        cand.local_path = str(resolved_path)
                        cand.candidate_status = evaluate_candidate_status(cand)
                        cand.local_path = actual_path
                    else:
                        cand.candidate_status = evaluate_candidate_status(cand)
                        
                    candidates.append(cand)
            return candidates
        except Exception:
            pass
            
    # 2. No manifest or error loading manifest, fallback to scanning files
    files = list(baseline_dir.glob("*"))
    source_files = [f for f in files if f.is_file() and f.name != "source_manifest.json" and f.name != ".gitkeep"]
    
    for idx, sfile in enumerate(source_files):
        rel_path = sfile.relative_to(project_root)
        name_lower = sfile.name.lower()
        
        # Extrapolate requirement based on filename
        if "formula" in name_lower or "decay" in name_lower:
            req_id = "BSR-001"
            title = "Exponential Decay Reference"
        elif "environmental" in name_lower or "noise" in name_lower or "gamma" in name_lower:
            req_id = "BSR-002"
            title = "Decoherence Noise Reference"
        elif "threshold" in name_lower or "uncertainty" in name_lower or "epsilon" in name_lower:
            req_id = "BSR-003"
            title = "Experimental Visibility Reference"
        else:
            req_id = "BSR-004"
            title = "General Context Reference"
            
        cand = SourceCandidate(
            source_candidate_id=f"CAND-SCAN-{idx+1:03d}",
            requirement_id=req_id,
            title=title,
            authors=["System Scanned"],
            year="2026",
            source_type="PAPER",
            local_path=str(rel_path),
            url=None,
            trust_level="HIGH",
            notes="Dynamically registered via directory scanner."
        )
        # Verify status
        cand.local_path = str(sfile)
        cand.candidate_status = evaluate_candidate_status(cand)
        cand.local_path = str(rel_path)
        candidates.append(cand)
        
    return candidates
