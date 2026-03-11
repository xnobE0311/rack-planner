"""Legacy entrypoint compatibility shim.

Preferred command:
    uvicorn rack_planner.app:app --reload
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from rack_planner.app import app  # noqa: F401
except ImportError:
    backend_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(backend_dir))
    from rack_planner.app import app  # type: ignore # noqa: F401
