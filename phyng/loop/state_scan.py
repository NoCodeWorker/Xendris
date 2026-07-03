from pathlib import Path
from typing import Dict, Any


def scan_project_state(root_dir: Path) -> Dict[str, Any]:
    state = {
        "tests_count": 0,
        "test_files": [],
        "core_modules": [],
        "missing_modules": [],
        "reports_count": 0,
        "backlog_present": False,
        "api_present": False
    }
    
    # Scan tests
    tests_dir = root_dir / "tests"
    if tests_dir.exists():
        test_files = list(tests_dir.glob("test_*.py"))
        state["tests_count"] = len(test_files)
        state["test_files"] = [f.name for f in test_files]
        
    # Check core modules in phyng/
    phyng_dir = root_dir / "phyng"
    required_modules = [
        "constants.py",
        "frontier_lengths.py",
        "enums.py",
        "errors.py",
        "operational_scale.py",
        "signature.py",
        "epistemic_trace.py",
        "predictive_gain.py",
        "claim_gatekeeper.py",
        "api.py"
    ]
    
    if phyng_dir.exists():
        for mod in required_modules:
            if (phyng_dir / mod).exists():
                state["core_modules"].append(mod)
            else:
                state["missing_modules"].append(mod)
                
    # Check reports
    reports_dir = root_dir / "reports"
    if reports_dir.exists():
        reports = list(reports_dir.glob("*.md"))
        state["reports_count"] = len(reports)
        
    # Check backlog files
    backlog_json = root_dir / "backlog" / "phygn_core_backlog.json"
    state["backlog_present"] = backlog_json.exists()
    
    # Check API file specifically
    state["api_present"] = "api.py" in state["core_modules"]
    
    return state
