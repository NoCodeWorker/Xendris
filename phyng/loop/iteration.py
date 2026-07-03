import datetime
from pathlib import Path
from phyng.loop.schemas import IterationRecord, BacklogTask
from phyng.loop.state_scan import scan_project_state
from phyng.loop.gap_detection import run_all_gap_detections
from phyng.loop.backlog import load_backlog, save_backlog, update_backlog_md_report
from phyng.rag.source_registry import list_sources
from phyng.rag.claim_registry import list_claims, get_claim
from phyng.rag.claim_linker import audit_claim_support
from phyng.rag.research_planner import plan_research_for_claim, list_research_tasks
from phyng.rag.rag_report import (
    generate_rag_status_report, generate_claim_source_matrix_report,
    generate_research_backlog_report, generate_benchmark_status_report, generate_core_backlog_report
)


def run_iteration_once(project_root: Path) -> IterationRecord:
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    
    # Ensure directory structure and initialize empty JSON arrays if missing
    (project_root / "rag" / "sources").mkdir(parents=True, exist_ok=True)
    (project_root / "rag" / "chunks").mkdir(parents=True, exist_ok=True)
    (project_root / "rag" / "claims").mkdir(parents=True, exist_ok=True)
    (project_root / "rag" / "citations").mkdir(parents=True, exist_ok=True)
    (project_root / "rag" / "research_tasks").mkdir(parents=True, exist_ok=True)
    (project_root / "backlog").mkdir(parents=True, exist_ok=True)
    (project_root / "reports").mkdir(parents=True, exist_ok=True)

    manifests = [
        "rag/source_manifest.json",
        "rag/claims/claim_registry.json",
        "rag/claims/claim_source_links.json",
        "rag/research_tasks/research_backlog.json",
        "rag/citations/citation_audit.json",
        "backlog/phygn_core_backlog.json"
    ]
    for rel in manifests:
        p = project_root / rel
        if not p.exists() or p.stat().st_size == 0:
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write("[]")

    # 1. State Scan
    state = scan_project_state(project_root)
    
    # Load all sources and claims
    sources = list_sources(project_root)
    claims = list_claims(project_root)
    
    # Audit claim support states first to make sure statuses are in sync before gap detection
    for c in claims:
        audit_claim_support(c.claim_id, project_root)
    
    # Reload claims after audit updates
    claims = list_claims(project_root)
    
    # 2. Gap Detection
    gaps = run_all_gap_detections(sources, claims, project_root)
    
    # Rank Gaps based on severity: CRITICAL > HIGH > MEDIUM > LOW
    severity_ranking = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    sorted_gaps = sorted(gaps, key=lambda g: severity_ranking.get(g.severity, 1), reverse=True)
    
    target_gap = None
    target_mode = "Refactor Mode"
    if sorted_gaps:
        target_gap = sorted_gaps[0]
        mode_mapping = {
            "MISSING_SOURCE": "Research Mode",
            "MISSING_CLAIM_LINK": "RAG Link Mode",
            "MISSING_TEST": "Test Implementation Mode",
            "MISSING_BENCHMARK": "Benchmark Mode",
            "CLAIM_OVERREACH": "Gatekeeper Mode",
            "MISSING_MODEL": "Model Formalization Mode",
            "REPORT_GAP": "Reporting Mode",
            "API_SCHEMA_GAP": "API Implementation Mode",
            "RAG_GAP": "RAG Link Mode",
            "CLAIM_RISK": "Gatekeeper Mode"
        }
        target_mode = mode_mapping.get(target_gap.gap_type, "Refactor Mode")
    
    # 3. Update Backlog
    existing_backlog = load_backlog(project_root)
    existing_task_ids = {t.task_id for t in existing_backlog}
    
    new_backlog_tasks = []
    research_tasks_created = []
    
    for gap in gaps:
        task_id = f"TASK_{gap.gap_id}"
        if task_id not in existing_task_ids:
            prio_map = {"CRITICAL": "P0", "HIGH": "P1", "MEDIUM": "P2", "LOW": "P3"}
            prio = prio_map.get(gap.severity, "P2")
            
            task = BacklogTask(
                task_id=task_id,
                title=f"Resolve gap: {gap.gap_id}",
                task_type=gap.gap_type,
                priority=prio,
                status="TODO",
                blocked_by=[],
                acceptance_criteria=[gap.recommended_action],
                linked_gap_id=gap.gap_id
            )
            existing_backlog.append(task)
            new_backlog_tasks.append(task)
            
        if gap.gap_type == "MISSING_SOURCE":
            # Extract claim_id from gap_id (format is GAP_SRC_<claim_id> or similar)
            claim_id = gap.gap_id.replace("GAP_SRC_", "").replace("GAP_LOW_TRUST_", "")
            claim = get_claim(claim_id, project_root)
            if claim:
                r_task = plan_research_for_claim(claim, gap.gap_id, project_root)
                if r_task:
                    research_tasks_created.append(r_task.task_id)
                    
    save_backlog(existing_backlog, project_root)
    
    # 4. Generate Reports
    reports_written = []
    
    # Update backlog markdown report
    backlog_md_path = update_backlog_md_report(existing_backlog, project_root)
    reports_written.append(str(backlog_md_path))
    
    # Generate RAG status and claim source matrix reports
    rag_status_path = generate_rag_status_report(project_root)
    reports_written.append(str(rag_status_path))
    
    matrix_path = generate_claim_source_matrix_report(project_root)
    reports_written.append(str(matrix_path))
    
    # Generate research backlog, benchmark status, and core backlog reports
    res_backlog_path = generate_research_backlog_report(project_root)
    reports_written.append(str(res_backlog_path))
    
    bench_status_path = generate_benchmark_status_report(project_root)
    reports_written.append(str(bench_status_path))
    
    core_backlog_report_path = generate_core_backlog_report(project_root)
    reports_written.append(str(core_backlog_report_path))
    
    # Generate iteration log using v0.4 format
    log_path = project_root / "reports" / "iteration_log.md"
    
    target_gap_id = target_gap.gap_id if target_gap else "None"
    target_priority = target_gap.severity if target_gap else "None"
    target_action = target_gap.recommended_action if target_gap else "No outstanding gaps. Maintain and refactor."
    
    log_content = [
        "# Phygn Iteration Log",
        "",
        f"## ITERATION {timestamp}",
        "",
        "### Selected Gap",
        f"{target_gap_id}",
        "",
        "### Priority",
        f"{target_priority}",
        "",
        "### Mode",
        f"{target_mode}",
        "",
        "### Expected Output",
        f"{target_action}",
        "",
        "### Acceptance Criteria",
        f"- {target_action}",
        "",
        "---",
        "",
        "## Gaps Found Detail",
        ""
    ]
    if not gaps:
        log_content.append("- No gaps found in this iteration.")
    else:
        log_content.append("| Gap ID | Type | Severity | Description |")
        log_content.append("|---|---|---|---|")
        for g in gaps:
            log_content.append(f"| {g.gap_id} | {g.gap_type} | {g.severity} | {g.description} |")
            
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_content))
    reports_written.append(str(log_path))
    
    record = IterationRecord(
        iteration_id=f"ITER_{timestamp.replace(':', '-').replace('.', '-')}",
        timestamp=timestamp,
        gaps_found=gaps,
        backlog_tasks_created=new_backlog_tasks,
        research_tasks_created=research_tasks_created,
        reports_written=reports_written,
        status="SUCCESS"
    )
    
    # Save the iteration log record
    iteration_log_file = project_root / "reports" / "iteration_records.jsonl"
    with open(iteration_log_file, "a", encoding="utf-8") as f:
        f.write(record.model_dump_json() + "\n")
        
    return record

