import re
from pathlib import Path
from phyng.loop.schemas import GapRecord
from phyng.rag.schemas import ClaimRecord, SourceRecord


def detect_claims_without_sources(claims: list[ClaimRecord]) -> list[GapRecord]:
    gaps = []
    for c in claims:
        if not c.source_ids or c.status in ["REQUIRES_SOURCE", "REQUIRES_HIGHER_TRUST_SOURCE"]:
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_SRC_{c.claim_id}",
                    gap_type="MISSING_SOURCE",
                    severity="HIGH",
                    description=f"Claim '{c.claim_id}' has no linked valid source or requires higher trust sources.",
                    recommended_action=f"Link claim '{c.claim_id}' to a PRIMARY or HIGH trust physical bibliography source."
                )
            )
    return gaps


def detect_claims_without_tests(claims: list[ClaimRecord], root_dir: Path) -> list[GapRecord]:
    gaps = []
    tests_dir = root_dir / "tests"
    if not tests_dir.exists():
        for c in claims:
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_TEST_{c.claim_id}",
                    gap_type="MISSING_TEST",
                    severity="CRITICAL",
                    description=f"Tests directory does not exist. Claim '{c.claim_id}' has no test validation.",
                    recommended_action="Create tests directory and add unit tests."
                )
            )
        return gaps
        
    # Read all test files contents
    test_contents = ""
    for file_path in tests_dir.glob("test_*.py"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                test_contents += f.read()
        except Exception:
            continue
            
    for c in claims:
        # Check if the claim ID is mentioned in the test code
        if c.claim_id not in test_contents:
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_TEST_{c.claim_id}",
                    gap_type="MISSING_TEST",
                    severity="HIGH",
                    description=f"Claim '{c.claim_id}' is not referenced or tested in the test suite.",
                    recommended_action=f"Add a test case in tests/ checking gatekeeper or physical review of '{c.claim_id}'."
                )
            )
    return gaps


def detect_sources_without_claims(sources: list[SourceRecord], claims: list[ClaimRecord]) -> list[GapRecord]:
    gaps = []
    used_source_ids = set()
    for c in claims:
        for sid in c.source_ids:
            used_source_ids.add(sid)
            
    for s in sources:
        if s.source_id not in used_source_ids:
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_UNUSED_SRC_{s.source_id}",
                    gap_type="RAG_GAP",
                    severity="LOW",
                    description=f"Registered source '{s.source_id}' is not linked to any active claim.",
                    recommended_action=f"Link source '{s.source_id}' to a corresponding physical claim or remove it."
                )
            )
    return gaps


def detect_blocked_claims_without_safe_rewrite(claims: list[ClaimRecord]) -> list[GapRecord]:
    gaps = []
    for c in claims:
        if c.status == "BLOCKED" and not c.safe_rewrite:
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_REWRITE_{c.claim_id}",
                    gap_type="CLAIM_RISK",
                    severity="MEDIUM",
                    description=f"Blocked claim '{c.claim_id}' does not have a safe scientific rewrite defined.",
                    recommended_action=f"Define a safe rewrite for claim '{c.claim_id}' to propose a rigorous alternative."
                )
            )
    return gaps


def detect_claims_with_low_trust_only(claims: list[ClaimRecord], sources: list[SourceRecord]) -> list[GapRecord]:
    gaps = []
    source_map = {s.source_id: s for s in sources}
    for c in claims:
        if not c.source_ids:
            continue
        all_low = True
        for sid in c.source_ids:
            src = source_map.get(sid)
            if src and src.trust_level != "LOW":
                all_low = False
                break
        if all_low:
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_LOW_TRUST_{c.claim_id}",
                    gap_type="CLAIM_RISK",
                    severity="HIGH",
                    description=f"Claim '{c.claim_id}' depends only on low trust sources.",
                    recommended_action=f"Link claim '{c.claim_id}' to a HIGH or PRIMARY trust source."
                )
            )
    return gaps


def detect_research_tasks_pending(root_dir: Path) -> list[GapRecord]:
    from phyng.rag.research_planner import list_research_tasks
    gaps = []
    tasks = list_research_tasks(root_dir)
    for t in tasks:
        if t.status in ["TODO", "IN_PROGRESS", "AWAITING_SOURCE_INGESTION"]:
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_RSC_PENDING_{t.task_id}",
                    gap_type="MISSING_SOURCE",
                    severity="MEDIUM",
                    description=f"Research task '{t.task_id}' is pending ingestion: {t.question}",
                    recommended_action=f"Resolve research task '{t.task_id}' by ingesting the required physical sources."
                )
            )
    return gaps


def detect_missing_reports(root_dir: Path) -> list[GapRecord]:
    gaps = []
    required_reports = [
        "iteration_log.md",
        "rag_status.md",
        "claim_source_matrix.md",
        "research_backlog.md",
        "core_backlog.md",
        "benchmark_status.md"
    ]
    reports_dir = root_dir / "reports"
    for r in required_reports:
        path = reports_dir / r
        if not path.exists():
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_REPORT_MISSING_{r.replace('.', '_')}",
                    gap_type="REPORT_GAP",
                    severity="LOW",
                    description=f"Required report '{r}' is missing from reports/ directory.",
                    recommended_action=f"Run iteration loop to regenerate the missing report '{r}'."
                )
            )
    return gaps


def detect_missing_registries(root_dir: Path) -> list[GapRecord]:
    gaps = []
    required_registries = [
        ("rag/source_manifest.json", "RAG_GAP"),
        ("rag/claims/claim_registry.json", "RAG_GAP"),
        ("rag/claims/claim_source_links.json", "RAG_GAP"),
        ("rag/research_tasks/research_backlog.json", "RAG_GAP"),
        ("rag/citations/citation_audit.json", "RAG_GAP"),
        ("backlog/phygn_core_backlog.json", "RAG_GAP")
    ]
    for rel_path, gap_type in required_registries:
        path = root_dir / rel_path
        if not path.exists():
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_REGISTRY_MISSING_{path.name.replace('.', '_')}",
                    gap_type=gap_type,
                    severity="HIGH",
                    description=f"Required registry database file '{rel_path}' is missing.",
                    recommended_action=f"Create/initialize empty registry file at '{rel_path}'."
                )
            )
    return gaps


def detect_api_endpoints_without_tests(root_dir: Path) -> list[GapRecord]:
    gaps = []
    api_file = root_dir / "phyng" / "api.py"
    if not api_file.exists():
        return gaps
        
    try:
        with open(api_file, "r", encoding="utf-8") as f:
            api_content = f.read()
    except Exception:
        return gaps
        
    routes = re.findall(r'@app\.(?:get|post|put|delete)\("([^"]+)"\)', api_content)
    
    tests_dir = root_dir / "tests"
    if not tests_dir.exists():
        for r in routes:
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_API_TEST_{r.replace('/', '_').strip('_')}",
                    gap_type="API_SCHEMA_GAP",
                    severity="HIGH",
                    description=f"API route '{r}' has no corresponding test suite.",
                    recommended_action="Create tests directory and add endpoint verification tests."
                )
            )
        return gaps
        
    test_contents = ""
    for file_path in tests_dir.glob("test_*.py"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                test_contents += f.read()
        except Exception:
            continue
            
    for r in routes:
        if r not in test_contents:
            gaps.append(
                GapRecord(
                    gap_id=f"GAP_API_TEST_{r.replace('/', '_').strip('_')}",
                    gap_type="API_SCHEMA_GAP",
                    severity="MEDIUM",
                    description=f"API endpoint '{r}' is not verified/invoked in tests.",
                    recommended_action=f"Add a client test case in tests/ invoking endpoint '{r}'."
                )
            )
    return gaps


def run_all_gap_detections(sources: list[SourceRecord], claims: list[ClaimRecord], root_dir: Path) -> list[GapRecord]:
    gaps = []
    gaps.extend(detect_claims_without_sources(claims))
    gaps.extend(detect_claims_with_low_trust_only(claims, sources))
    gaps.extend(detect_claims_without_tests(claims, root_dir))
    gaps.extend(detect_sources_without_claims(sources, claims))
    gaps.extend(detect_blocked_claims_without_safe_rewrite(claims))
    gaps.extend(detect_research_tasks_pending(root_dir))
    gaps.extend(detect_missing_reports(root_dir))
    gaps.extend(detect_missing_registries(root_dir))
    gaps.extend(detect_api_endpoints_without_tests(root_dir))
    return gaps

