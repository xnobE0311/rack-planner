"""FastAPI backend for the Rack‑Planner project.

This module exposes a minimal set of endpoints to support early development of
the 10‑inch rack planner. It loads the device library from ``data/devices``,
serves it over HTTP and performs basic rack validation. The intention is to
provide a working API scaffold that can be expanded upon by future
contributors.

Run this module with Uvicorn for local development:

    uvicorn rack_planner.backend.app.main:app --reload

The API will listen on http://localhost:8000 by default. CORS is enabled for
all origins to simplify interaction with the frontend during development.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from .schemas import Device, RackSpec, DevicePlacement, ValidationResponse

app = FastAPI(
    title="Rack Planner API",
    description="Backend API for the 10‑inch rack planner",
    version="0.1.0",
)

# Allow any origin during development; consider restricting in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determine the path to the example devices file relative to this file
DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "devices" / "example_devices.json"


def load_devices() -> List[Device]:
    """Load the device library from disk and return a list of ``Device`` objects.

    If the file cannot be read or parsed, an HTTP 500 error is raised.
    """

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            devices_raw = json.load(f)
        return [Device(**entry) for entry in devices_raw]
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Device file not found at {DATA_PATH}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to load devices: {exc}")


@app.get("/devices", response_model=List[Device])
def get_devices() -> List[Device]:
    """Return the list of available devices from the library."""

    return load_devices()


@app.post("/validate", response_model=ValidationResponse)
def validate_plan(rack: RackSpec, placements: List[DevicePlacement]):
    """Validate a rack plan against basic constraints.

    This initial implementation checks only that devices do not extend beyond
    the rack height. Future versions should consider width, depth,
    ventilation clearance and cable management. See ``docs/architecture.md``
    for guidance on additional validation rules.
    """

    warnings: List[str] = []
    for p in placements:
        if p.u_start < 0:
            warnings.append(f"Device {p.device_id}: start U cannot be negative")
        if p.u_start + p.u_height > rack.height_u:
            warnings.append(
                f"Device {p.device_id}: occupies up to U{p.u_start + p.u_height}, which exceeds rack height {rack.height_u}U"
            )
    ok = len(warnings) == 0
    return ValidationResponse(ok=ok, warnings=warnings)