import tempfile
from pathlib import Path
from phyng.rag.schemas import ClaimRecord, SourceRecord, ClaimSourceLink
from phyng.rag.claim_registry import add_claim
from phyng.rag.source_registry import add_source
from phyng.rag.claim_linker import link_claim_to_source
from phyng.rag.rag_report import generate_rag_status_report, generate_claim_source_matrix_report


def test_rag_reports_generation():
    claim = ClaimRecord(
        claim_id="CLAIM-1",
        text="Planck length is the minimum limit.",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=["SRC-1"]
    )
    source = SourceRecord(
        source_id="SRC-1",
        title="High trust physics paper",
        source_type="PAPER",
        trust_level="HIGH",
        relevance="HIGH",
        topics=["Quantum Mechanics"]
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        add_claim(claim, tmp_path)
        add_source(source, tmp_path)
        
        link = ClaimSourceLink(
            claim_id="CLAIM-1",
            source_id="SRC-1",
            support_level="DIRECT_SUPPORT",
            quote_or_note="This is true"
        )
        link_claim_to_source(link, tmp_path)

        
        status_path = generate_rag_status_report(tmp_path)
        assert status_path.exists()
        assert status_path.name == "rag_status.md"
        with open(status_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Total Registered Sources**: 1" in content
            assert "Total Registered Claims**: 1" in content
            
        matrix_path = generate_claim_source_matrix_report(tmp_path)
        assert matrix_path.exists()
        assert matrix_path.name == "claim_source_matrix.md"
        with open(matrix_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "CLAIM-1" in content
            assert "SRC-1" in content
            assert "ALLOWED" in content
