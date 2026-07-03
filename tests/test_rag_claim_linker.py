import tempfile
from pathlib import Path
from phyng.rag.schemas import ClaimRecord, SourceRecord, ClaimSourceLink
from phyng.rag.claim_registry import add_claim
from phyng.rag.source_registry import add_source
from phyng.rag.claim_linker import link_claim_to_source, audit_claim_support


def test_linker_claim_without_source():
    claim = ClaimRecord(
        claim_id="CLAIM-1",
        text="Planck length boundary",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=[]
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        add_claim(claim, tmp_path)
        
        audited = audit_claim_support("CLAIM-1", tmp_path)
        assert audited.status == "REQUIRES_SOURCE"


def test_linker_low_trust_source_blocks_hard_claim():
    claim = ClaimRecord(
        claim_id="CLAIM-HARD",
        text="A hard physical hypothesis",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=[]
    )
    source = SourceRecord(
        source_id="SRC-LOW-TRUST",
        title="Unverified blog post",
        source_type="WEB_ARTICLE",
        trust_level="LOW",
        relevance="MEDIUM",
        topics=["Relativity"]
    )
    link = ClaimSourceLink(
        claim_id="CLAIM-HARD",
        source_id="SRC-LOW-TRUST",
        support_level="DIRECT_SUPPORT",
        quote_or_note="This is true"
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        add_claim(claim, tmp_path)
        add_source(source, tmp_path)
        
        link_claim_to_source(link, tmp_path)
        audited = audit_claim_support("CLAIM-HARD", tmp_path)
        assert audited.status == "REQUIRES_HIGHER_TRUST_SOURCE"


def test_linker_direct_support_allows():
    claim = ClaimRecord(
        claim_id="CLAIM-ALLOWED",
        text="Planck length is the minimum length.",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="REQUIRES_SOURCE",
        source_ids=[]
    )
    source = SourceRecord(
        source_id="SRC-HIGH-TRUST",
        title="High trust physics paper",
        source_type="PAPER",
        trust_level="HIGH",
        relevance="HIGH",
        topics=["Quantum Mechanics"]
    )
    link = ClaimSourceLink(
        claim_id="CLAIM-ALLOWED",
        source_id="SRC-HIGH-TRUST",
        support_level="DIRECT_SUPPORT",
        quote_or_note="Planck length is the minimum limit"
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        add_claim(claim, tmp_path)
        add_source(source, tmp_path)
        
        # Mock test file to satisfy tests requirement check
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        with open(tests_dir / "test_verification.py", "w") as f:
            f.write("# Verification for CLAIM-ALLOWED")
        
        link_claim_to_source(link, tmp_path)
        audited = audit_claim_support("CLAIM-ALLOWED", tmp_path)
        assert audited.status == "ALLOWED"



def test_linker_contradicting_blocks_claim():
    claim = ClaimRecord(
        claim_id="CLAIM-CONTRADICTED",
        text="Planck length is 10 meters.",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=[]
    )
    source = SourceRecord(
        source_id="SRC-REFUTING",
        title="Refuting paper",
        source_type="PAPER",
        trust_level="PRIMARY",
        relevance="HIGH",
        topics=["Physics"]
    )
    link = ClaimSourceLink(
        claim_id="CLAIM-CONTRADICTED",
        source_id="SRC-REFUTING",
        support_level="CONTRADICTS",
        quote_or_note="This is false. Planck length is much smaller."
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        add_claim(claim, tmp_path)
        add_source(source, tmp_path)
        
        link_claim_to_source(link, tmp_path)
        audited = audit_claim_support("CLAIM-CONTRADICTED", tmp_path)
        assert audited.status == "BLOCKED"


def test_linker_background_only_requires_source():
    claim = ClaimRecord(
        claim_id="CLAIM-BG-ONLY",
        text="A normal claim",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=[]
    )
    source = SourceRecord(
        source_id="SRC-BG",
        title="Background paper",
        source_type="PAPER",
        trust_level="HIGH",
        relevance="LOW",
        topics=["Physics"]
    )
    link = ClaimSourceLink(
        claim_id="CLAIM-BG-ONLY",
        source_id="SRC-BG",
        support_level="BACKGROUND",
        quote_or_note="This is general background."
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        add_claim(claim, tmp_path)
        add_source(source, tmp_path)
        link_claim_to_source(link, tmp_path)
        
        audited = audit_claim_support("CLAIM-BG-ONLY", tmp_path)
        assert audited.status == "REQUIRES_SOURCE"


def test_linker_hard_claim_requires_higher_trust_source():
    claim = ClaimRecord(
        claim_id="CLAIM-HARD-TEXT",
        text="This predicts new physics cancelations.",
        claim_type="STRUCTURAL_LEMMA",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=[]
    )
    source = SourceRecord(
        source_id="SRC-LOW-TRUST",
        title="Casual forum post",
        source_type="WEB_ARTICLE",
        trust_level="LOW",
        relevance="HIGH",
        topics=["Physics"]
    )
    link = ClaimSourceLink(
        claim_id="CLAIM-HARD-TEXT",
        source_id="SRC-LOW-TRUST",
        support_level="DIRECT_SUPPORT",
        quote_or_note="Prediction here."
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        add_claim(claim, tmp_path)
        add_source(source, tmp_path)
        link_claim_to_source(link, tmp_path)
        
        audited = audit_claim_support("CLAIM-HARD-TEXT", tmp_path)
        assert audited.status == "REQUIRES_HIGHER_TRUST_SOURCE"


def test_linker_no_test_requires_test_status():
    claim = ClaimRecord(
        claim_id="CLAIM-NO-TESTS",
        text="Planck length check",
        claim_type="HYPOTHESIS",
        layer="PHYSICAL_CORE",
        status="ALLOWED",
        source_ids=[]
    )
    source = SourceRecord(
        source_id="SRC-HIGH",
        title="Good paper",
        source_type="PAPER",
        trust_level="HIGH",
        relevance="HIGH",
        topics=["Physics"]
    )
    link = ClaimSourceLink(
        claim_id="CLAIM-NO-TESTS",
        source_id="SRC-HIGH",
        support_level="DIRECT_SUPPORT",
        quote_or_note="Verified limits."
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        add_claim(claim, tmp_path)
        add_source(source, tmp_path)
        link_claim_to_source(link, tmp_path)
        
        # Note: we do not create a mock test file, so tests req check fails
        audited = audit_claim_support("CLAIM-NO-TESTS", tmp_path)
        assert audited.status == "REQUIRES_TEST"

