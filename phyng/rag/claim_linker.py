import json
from pathlib import Path
from typing import Optional
from phyng.rag.schemas import ClaimSourceLink, ClaimRecord
from phyng.rag.claim_registry import get_claim, add_claim
from phyng.rag.source_registry import get_source
from phyng.enums import Layer, ClaimType


def link_claim_to_source(link: ClaimSourceLink, root_dir: Path) -> None:
    links_dir = root_dir / "rag" / "citations"
    links_dir.mkdir(parents=True, exist_ok=True)
    
    # Store link in a file named <claim_id>_<source_id>.json
    file_path = links_dir / f"{link.claim_id}_{link.source_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(link.model_dump_json(indent=2))
        
    # Also update the claim's source_ids list if not already present
    claim = get_claim(link.claim_id, root_dir)
    if claim:
        if link.source_id not in claim.source_ids:
            claim.source_ids.append(link.source_id)
            add_claim(claim, root_dir)


def list_links_for_claim(claim_id: str, root_dir: Path) -> list[ClaimSourceLink]:
    links_dir = root_dir / "rag" / "citations"
    if not links_dir.exists():
        return []
    
    links = []
    for file_path in links_dir.glob(f"{claim_id}_*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                links.append(ClaimSourceLink.model_validate(data))
        except Exception:
            continue
    return links


def audit_claim_support(claim_id: str, root_dir: Path) -> ClaimRecord:
    claim = get_claim(claim_id, root_dir)
    if not claim:
        raise ValueError(f"Claim {claim_id} not found")
        
    links = list_links_for_claim(claim_id, root_dir)
    
    # Update source_ids list to be in sync
    claim.source_ids = [link.source_id for link in links]
    
    if not links:
        claim.status = "REQUIRES_SOURCE"
        add_claim(claim, root_dir)
        return claim
        
    has_contradiction = False
    has_direct_support = False
    has_indirect_support = False
    highest_trust = "LOW"
    
    trust_ranking = {"PRIMARY": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    
    for link in links:
        if link.support_level == "CONTRADICTS":
            has_contradiction = True
        elif link.support_level == "DIRECT_SUPPORT":
            has_direct_support = True
        elif link.support_level == "INDIRECT_SUPPORT":
            has_indirect_support = True
            
        src = get_source(link.source_id, root_dir)
        if src:
            rank = trust_ranking.get(src.trust_level, 1)
            highest_rank = trust_ranking.get(highest_trust, 1)
            if rank > highest_rank:
                highest_trust = src.trust_level
                
    # Check if text contains hard keywords
    text_lower = claim.text.lower()
    hard_keywords = [
        "new physics", "demonstrates", "proves", "predicts", "validates", 
        "empirical evidence", "experimental detection",
        "demuestra", "prueba", "valida", "predice", "evidencia", "descubre", "nueva física"
    ]
    is_hard_text = any(kw in text_lower for kw in hard_keywords)
    is_hard_claim = is_hard_text or claim.claim_type in [ClaimType.AXIOM, ClaimType.HYPOTHESIS, ClaimType.MODEL]
    is_hard_layer = claim.layer in [Layer.PHYSICAL_CORE, Layer.ONTO_EPISTEMIC_CORE]
    
    # Check if tested
    is_speculative = claim.layer == Layer.SPECULATIVE_ONLY
    has_no_test = not claim.test_ids
    
    tests_dir = root_dir / "tests"
    if tests_dir.exists():
        tested_in_files = False
        for file_path in tests_dir.glob("test_*.py"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    if claim.claim_id in f.read():
                        tested_in_files = True
                        break
            except Exception:
                continue
        if tested_in_files:
            has_no_test = False
            
    if has_contradiction:
        claim.status = "BLOCKED"
    else:
        if is_hard_claim and is_hard_layer and highest_trust == "LOW":
            claim.status = "REQUIRES_HIGHER_TRUST_SOURCE"
        elif not has_direct_support and not has_indirect_support:
            # background-only support -> REQUIRES_SOURCE
            claim.status = "REQUIRES_SOURCE"
        elif has_direct_support or has_indirect_support:
            target_status = "ALLOWED_LIMITED" if is_speculative else "ALLOWED"
            
            if not is_speculative and has_no_test:
                claim.status = "REQUIRES_TEST"
            else:
                claim.status = target_status
        else:
            claim.status = "REQUIRES_SOURCE"
            
    add_claim(claim, root_dir)
    return claim

