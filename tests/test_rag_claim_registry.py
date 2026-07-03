import tempfile
from pathlib import Path
from phyng.rag.schemas import ClaimRecord
from phyng.rag.claim_registry import add_claim, list_claims, get_claim


def test_claim_record_validation_and_persistence():
    claim = ClaimRecord(
        claim_id="CLAIM-LEMMA-1",
        text="Planck length is the absolute minimum boundary.",
        claim_type="STRUCTURAL_LEMMA",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=["SRC-PLANCK"]
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Save claim
        add_claim(claim, tmp_path)
        
        # List claims
        all_claims = list_claims(tmp_path)
        assert len(all_claims) == 1
        assert all_claims[0].claim_id == "CLAIM-LEMMA-1"
        assert all_claims[0].claim_type == "STRUCTURAL_LEMMA"
        
        # Get claim
        retrieved = get_claim("CLAIM-LEMMA-1", tmp_path)
        assert retrieved is not None
        assert retrieved.text == claim.text
        
        # Non-existent
        assert get_claim("NON-EXISTENT", tmp_path) is None
