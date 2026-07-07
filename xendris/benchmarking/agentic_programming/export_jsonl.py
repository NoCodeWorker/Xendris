from __future__ import annotations

import json


def export_to_jsonl(
    results: list,
    output_path: str,
) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r.to_dict(), ensure_ascii=False) + "\n")
