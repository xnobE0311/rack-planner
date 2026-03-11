from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .module_manager import active_devices, active_module, activate_module, list_modules, load_modules
from .schemas import Device, ValidationRequest, ValidationResponse

REPO_ROOT = Path(__file__).resolve().parents[2]
DEVICES_DIR = REPO_ROOT / "data" / "devices"


def _split_csv(value: str) -> List[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def _bool_env(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "y", "on"}


def resolve_device_library_paths() -> List[Path]:
    explicit_path = os.getenv("RACK_PLANNER_DEVICES_PATH", "").strip()
    explicit_dir = os.getenv("RACK_PLANNER_DEVICES_DIR", "").strip()
    candidates: List[Path] = []

    if explicit_path:
        p = Path(explicit_path)
        if not p.is_absolute():
            p = (REPO_ROOT / p).resolve()
        candidates = [p]
    elif explicit_dir:
        d = Path(explicit_dir)
        if not d.is_absolute():
            d = (REPO_ROOT / d).resolve()
        if not d.exists() or not d.is_dir():
            raise HTTPException(status_code=500, detail=f"Devices dir not found: {d}")
        candidates = sorted([p for p in d.glob("*.json") if p.is_file()])
    else:
        candidates = [
            DEVICES_DIR / "default_devices.json",
            DEVICES_DIR / "example_devices.json",
        ]

    existing = [p for p in candidates if p.exists()]
    if not existing:
        raise HTTPException(
            status_code=500,
            detail=f"No device library files found. Checked: {[str(p) for p in candidates]}",
        )
    return existing


def load_device_library() -> List[Device]:
    """Load base device definitions and merge any devices from the active module."""
    devices_by_id: Dict[str, Device] = {}
    for path in resolve_device_library_paths():
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Failed to read JSON: {path}: {exc}")

        if not isinstance(raw, list):
            raise HTTPException(status_code=500, detail=f"Device file must be a JSON array: {path}")

        for entry in raw:
            try:
                device = Device(**entry)
            except Exception as exc:
                raise HTTPException(status_code=500, detail=f"Invalid device entry in {path}: {exc}")
            devices_by_id[device.id] = device

    for device in active_devices():
        devices_by_id[device.id] = device

    return sorted(devices_by_id.values(), key=lambda d: (d.category or "", d.name))


def create_app() -> FastAPI:
    app = FastAPI(
        title="Rack-Planner API",
        description="Backend API for the 10-inch mini rack planner with Patchbox-style modules",
        version="0.2.0",
    )

    allowed_origins = _split_csv(
        os.getenv("RACK_PLANNER_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    )
    allow_credentials = _bool_env("RACK_PLANNER_CORS_ALLOW_CREDENTIALS", default="false")

    if not allowed_origins:
        allowed_origins = ["*"]
    if allow_credentials and "*" in allowed_origins:
        allowed_origins = [o for o in allowed_origins if o != "*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    load_modules()

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/v1/devices", response_model=List[Device])
    def list_devices_v1() -> List[Device]:
        return load_device_library()

    @app.get("/api/v1/modules")
    def list_modules_v1() -> dict:
        return {
            "active": active_module(),
            "modules": list_modules(),
        }

    @app.post("/api/v1/modules/activate")
    def activate_module_v1(payload: dict) -> dict:
        module_id = payload.get("module_id")
        try:
            activate_module(module_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Module not found")
        return {"active": active_module()}

    @app.post("/api/v1/validate", response_model=ValidationResponse)
    def validate_v1(payload: ValidationRequest) -> ValidationResponse:
        devices = {d.id: d for d in load_device_library()}
        rack = payload.rack
        warnings: List[str] = []
        occupied_u: Dict[int, str] = {}

        for placement in payload.placements:
            device = devices.get(placement.device_id)
            if device is None:
                warnings.append(f"Unknown device_id: {placement.device_id}")
                continue

            u_height = placement.u_height or device.u_height
            if placement.u_start + u_height > rack.height_u:
                warnings.append(
                    f"{device.id}: occupies U{placement.u_start + 1}..U{placement.u_start + u_height}, exceeds rack height {rack.height_u}U."
                )

            for u in range(placement.u_start, placement.u_start + u_height):
                if u < 0 or u >= rack.height_u:
                    continue
                if u in occupied_u:
                    warnings.append(f"Overlap: {device.id} conflicts with {occupied_u[u]} at U{u + 1}.")
                else:
                    occupied_u[u] = device.id

            if device.width_mm > rack.width_mm:
                warnings.append(f"{device.id}: width_mm {device.width_mm} > rack width_mm {rack.width_mm}.")

            required_rear_clearance = max(rack.rear_clearance_mm, device.cable_clearance_mm or 0.0)
            usable_depth = rack.depth_mm - required_rear_clearance
            if usable_depth < 0:
                warnings.append(
                    f"{device.id}: rear clearance {required_rear_clearance} leaves negative usable depth (rack depth {rack.depth_mm})."
                )
            elif device.depth_mm > usable_depth:
                warnings.append(
                    f"{device.id}: depth_mm {device.depth_mm} > usable depth {usable_depth} (rack depth {rack.depth_mm} - rear clearance {required_rear_clearance})."
                )

        return ValidationResponse(ok=(len(warnings) == 0), warnings=warnings)

    @app.get("/devices", include_in_schema=False, response_model=List[Device])
    def legacy_devices() -> List[Device]:
        return list_devices_v1()

    @app.post("/validate", include_in_schema=False, response_model=ValidationResponse)
    def legacy_validate(payload: ValidationRequest) -> ValidationResponse:
        return validate_v1(payload)

    return app


app = create_app()
