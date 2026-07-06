"""Launch the Xendris Runtime API server."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    os.chdir(PROJECT_ROOT)
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)

    uvicorn.run(
        "xendris.runtime_api:app",
        host="127.0.0.1",
        port=8001,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
