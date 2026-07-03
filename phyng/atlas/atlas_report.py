import json
from pathlib import Path
from phyng.atlas.schemas import BoundaryAtlas


def generate_atlas_report(atlas: BoundaryAtlas, root_dir: Path) -> Path:
    atlas_dir = root_dir / "reports" / "atlas"
    atlas_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Write invariant_boundary_atlas.md
    md_path = atlas_dir / "invariant_boundary_atlas.md"
    md_lines = [
        "# Invariant Boundary Atlas",
        "",
        f"- **Atlas ID**: {atlas.atlas_id}",
        f"- **Version**: {atlas.version}",
        f"- **Generated At**: {atlas.generated_at}",
        f"- **Total Systems Mapped**: {atlas.summary.get('total_points', 0)}",
        "",
        "## Invariant Core Definition",
        "The atlas is anchored on the fundamental Compton-Schwarzschild invariant:",
        "$$QB = \\left(\\frac{\\ell_P}{L}\\right)^2$$",
        "This implies that at any fixed operational scale $L$, the localization signature $Q$ and gravity signature $B$ are geometrically constrained.",
        "",
        "## Systems Summary Map",
        "",
        "| System ID | Label | Mass (kg) | Scale L (m) | Q | B | QB | Region | Claim Status |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for p in atlas.points:
        md_lines.append(
            f"| {p.system_id} | {p.label} | {p.m_kg:.2e} | {p.L_value_m:.2e} | {p.Q:.2e} | {p.B:.2e} | {p.QB:.2e} | {p.region} | {p.claim_status} |"
        )
        
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    # 2. Write claim_exclusion_matrix.md
    matrix_path = atlas_dir / "claim_exclusion_matrix.md"
    matrix_lines = [
        "# Claim Exclusion Matrix",
        "",
        "| System ID | Region | Allowed Claims | Blocked Claims |",
        "|---|---|---|---|",
    ]
    for p in atlas.points:
        allowed_str = "<br>".join([f"- {c}" for c in p.allowed_claims]) if p.allowed_claims else "None"
        blocked_str = "<br>".join([f"- {c}" for c in p.blocked_claims]) if p.blocked_claims else "None"
        matrix_lines.append(
            f"| {p.system_id} | {p.region} | {allowed_str} | {blocked_str} |"
        )
        
    with open(matrix_path, "w", encoding="utf-8") as f:
        f.write("\n".join(matrix_lines))
        
    # 3. Write atlas_points.json
    json_path = atlas_dir / "atlas_points.json"
    data = [p.model_dump() for p in atlas.points]
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    return md_path
