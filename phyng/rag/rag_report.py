from pathlib import Path
from phyng.rag.source_registry import list_sources
from phyng.rag.claim_registry import list_claims
from phyng.rag.claim_linker import list_links_for_claim
from phyng.rag.research_planner import list_research_tasks


def generate_rag_status_report(root_dir: Path) -> Path:
    sources = list_sources(root_dir)
    claims = list_claims(root_dir)
    tasks = list_research_tasks(root_dir)
    
    # Calculate stats
    total_sources = len(sources)
    total_claims = len(claims)
    
    status_counts = {}
    for c in claims:
        status_counts[c.status] = status_counts.get(c.status, 0) + 1
        
    report_path = root_dir / "reports" / "rag_status.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    md_content = []
    md_content.append("# RAG Status Report")
    md_content.append("")
    md_content.append("## Metrics Summary")
    md_content.append(f"- **Total Registered Sources**: {total_sources}")
    md_content.append(f"- **Total Registered Claims**: {total_claims}")
    md_content.append("")
    md_content.append("### Claims Status Breakdown")
    if not status_counts:
        md_content.append("- No claims registered yet.")
    for status, count in status_counts.items():
        md_content.append(f"- **{status}**: {count}")
    md_content.append("")
    md_content.append("## Research Backlog status")
    if not tasks:
        md_content.append("- No active research tasks.")
    else:
        md_content.append("| Task ID | Question | Priority | Status |")
        md_content.append("|---|---|---|---|")
        for t in tasks:
            md_content.append(f"| {t.task_id} | {t.question} | {t.priority} | {t.status} |")
            
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
        
    return report_path


def generate_claim_source_matrix_report(root_dir: Path) -> Path:
    claims = list_claims(root_dir)
    
    report_path = root_dir / "reports" / "claim_source_matrix.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    md_content = []
    md_content.append("# Claim-Source Mapping Matrix")
    md_content.append("")
    md_content.append("| Claim ID | Claim Text | Layer | Status | Linked Sources & Support Level |")
    md_content.append("|---|---|---|---|---|")
    
    if not claims:
        md_content.append("| - | - | - | - | - |")
    else:
        for c in claims:
            links = list_links_for_claim(c.claim_id, root_dir)
            if not links:
                link_desc = "*No sources linked*"
            else:
                link_desc = ", ".join([f"{l.source_id} ({l.support_level})" for l in links])
            md_content.append(f"| {c.claim_id} | {c.text} | {c.layer} | {c.status} | {link_desc} |")
            
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
        
    return report_path


def generate_research_backlog_report(root_dir: Path) -> Path:
    tasks = list_research_tasks(root_dir)
    report_path = root_dir / "reports" / "research_backlog.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    md_content = [
        "# Research Backlog",
        "",
        "| Task ID | Question | Priority | Status | Linked Gap ID |",
        "|---|---|---|---|---|",
    ]
    if not tasks:
        md_content.append("| - | - | - | - | - |")
    else:
        for t in tasks:
            md_content.append(f"| {t.task_id} | {t.question} | {t.priority} | {t.status} | {t.linked_gap_id} |")
            
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    return report_path


def generate_benchmark_status_report(root_dir: Path) -> Path:
    claims = list_claims(root_dir)
    report_path = root_dir / "reports" / "benchmark_status.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    md_content = [
        "# Benchmark Status",
        "",
        "| Claim ID | Text | Layer | Benchmarks | Status |",
        "|---|---|---|---|---|",
    ]
    if not claims:
        md_content.append("| - | - | - | - | - |")
    else:
        for c in claims:
            benchmarks = ", ".join(c.benchmark_ids) if c.benchmark_ids else "None"
            md_content.append(f"| {c.claim_id} | {c.text} | {c.layer} | {benchmarks} | {c.status} |")
            
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    return report_path


def generate_core_backlog_report(root_dir: Path) -> Path:
    from phyng.loop.backlog import load_backlog
    backlog = load_backlog(root_dir)
    report_path = root_dir / "reports" / "core_backlog.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    md_content = [
        "# Core Development Backlog",
        "",
        "| Task ID | Title | Priority | Status | Linked Gap ID |",
        "|---|---|---|---|---|",
    ]
    if not backlog:
        md_content.append("| - | - | - | - | - |")
    else:
        for t in backlog:
            linked_gap = t.linked_gap_id if t.linked_gap_id else "None"
            md_content.append(f"| {t.task_id} | {t.title} | {t.priority} | {t.status} | {linked_gap} |")
            
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    return report_path

