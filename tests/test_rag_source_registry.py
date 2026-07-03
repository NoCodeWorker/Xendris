import tempfile
from pathlib import Path
from phyng.rag.schemas import SourceRecord
from phyng.rag.source_registry import add_source, list_sources, get_source


def test_source_record_validation_and_persistence():
    source = SourceRecord(
        source_id="SRC-PLANCK-1900",
        title="Ueber eine Verbesserung der Wien'schen Spectralgleichung",
        authors=["Max Planck"],
        year="1900",
        source_type="PAPER",
        trust_level="PRIMARY",
        relevance="HIGH",
        topics=["Quantum", "Blackbody Radiation"],
        used_for=["Planck constant definition"]
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Save source
        add_source(source, tmp_path)
        
        # List sources
        all_sources = list_sources(tmp_path)
        assert len(all_sources) == 1
        assert all_sources[0].source_id == "SRC-PLANCK-1900"
        assert all_sources[0].authors == ["Max Planck"]
        
        # Get source
        retrieved = get_source("SRC-PLANCK-1900", tmp_path)
        assert retrieved is not None
        assert retrieved.title == source.title
        
        # Non-existent
        assert get_source("NON-EXISTENT", tmp_path) is None
