"""Patchbox-style module manager for Rack Planner.

Each module lives under ``backend/rack_planner/modules/<module_id>/`` and
contains at minimum a ``module.json`` metadata file. A module may optionally
provide a ``devices.json`` file with additional device definitions.

Only one module can be active at a time. When active, its devices are merged
with the base device library served by the API. This mirrors the Patchbox OS
concept of switching the system into a different role by activating a module.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from .schemas import Device

MODULES_DIR = Path(__file__).resolve().parent / "modules"

_modules: Dict[str, dict] = {}
_active_module: Optional[str] = None


def load_modules() -> Dict[str, dict]:
    """Load all modules from disk into memory."""
    global _modules
    _modules = {}

    if not MODULES_DIR.exists():
        return _modules

    for folder in MODULES_DIR.iterdir():
        if not folder.is_dir():
            continue

        metadata_file = folder / "module.json"
        if not metadata_file.exists():
            continue

        try:
            metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        module_id = metadata.get("id")
        if not module_id:
            continue

        devices: List[Device] = []
        devices_file = folder / "devices.json"
        if devices_file.exists():
            try:
                raw = json.loads(devices_file.read_text(encoding="utf-8"))
                for entry in raw:
                    try:
                        devices.append(Device(**entry))
                    except Exception:
                        continue
            except Exception:
                pass

        _modules[module_id] = {
            "metadata": metadata,
            "devices": devices,
        }

    return _modules


def list_modules() -> List[dict]:
    """Return metadata for all loaded modules."""
    if not _modules:
        load_modules()
    return [m["metadata"] for m in _modules.values()]


def activate_module(module_id: Optional[str]) -> None:
    """Activate a module, or clear the active module when falsy."""
    global _active_module

    if not _modules:
        load_modules()

    if not module_id:
        _active_module = None
        return

    if module_id not in _modules:
        raise KeyError(f"Module '{module_id}' not found")

    _active_module = module_id


def active_module() -> Optional[str]:
    """Return the active module id, if any."""
    return _active_module


def active_devices() -> List[Device]:
    """Return device definitions from the currently active module."""
    if not _modules:
        load_modules()

    if _active_module and _active_module in _modules:
        return _modules[_active_module]["devices"]

    return []
