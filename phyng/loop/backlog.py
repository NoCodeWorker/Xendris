import json
from pathlib import Path
from phyng.loop.schemas import BacklogTask


def load_backlog(root_dir: Path) -> list[BacklogTask]:
    file_path = root_dir / "backlog" / "phygn_core_backlog.json"
    if not file_path.exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [BacklogTask.model_validate(item) for item in data]
    except Exception:
        return []


def save_backlog(backlog: list[BacklogTask], root_dir: Path) -> None:
    backlog_dir = root_dir / "backlog"
    backlog_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = backlog_dir / "phygn_core_backlog.json"
    
    # Dump list of dicts
    data = [task.model_dump() for task in backlog]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def update_backlog_md_report(backlog: list[BacklogTask], root_dir: Path) -> Path:
    report_path = root_dir / "backlog" / "phygn_core_backlog.md"
    
    md_content = []
    md_content.append("# Phygn Core Development Backlog")
    md_content.append("")
    md_content.append("## Task Board")
    md_content.append("")
    md_content.append("| Task ID | Title | Priority | Status | Blocked By |")
    md_content.append("|---|---|---|---|---|")
    
    if not backlog:
        md_content.append("| - | - | - | - | - |")
    else:
        for t in backlog:
            blocked = ", ".join(t.blocked_by) if t.blocked_by else "None"
            md_content.append(f"| {t.task_id} | {t.title} | {t.priority} | {t.status} | {blocked} |")
            
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
        
    return report_path
