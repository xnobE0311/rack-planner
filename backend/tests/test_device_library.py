from __future__ import annotations

import json
from pathlib import Path

from rack_planner.schemas import Device


def test_default_devices_json_parses() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    device_file = repo_root / "data" / "devices" / "default_devices.json"

    assert device_file.exists(), "default_devices.json must exist for a stable demo + CI baseline"

    raw = json.loads(device_file.read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    assert len(raw) >= 5

    for entry in raw:
        d = Device(**entry)
        assert d.id
        assert d.name
        assert d.u_height >= 1
        assert d.width_mm > 0
        assert d.depth_mm > 0
        assert d.weight_kg >= 0
        assert d.power_w >= 0
