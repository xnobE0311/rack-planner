from __future__ import annotations

from fastapi.testclient import TestClient

from rack_planner.app import app

client = TestClient(app)


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_devices_v1() -> None:
    r = client.get("/api/v1/devices")
    assert r.status_code == 200
    devices = r.json()
    assert isinstance(devices, list)
    assert len(devices) >= 1
    assert "id" in devices[0]
    assert "u_height" in devices[0]


def test_validate_v1_ok_empty() -> None:
    payload = {
        "rack": {"height_u": 10, "width_mm": 236.525, "depth_mm": 310, "rear_clearance_mm": 150},
        "placements": [],
    }
    r = client.post("/api/v1/validate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["warnings"] == []


def test_validate_v1_detects_overflow() -> None:
    payload = {
        "rack": {"height_u": 10, "width_mm": 236.525, "depth_mm": 310, "rear_clearance_mm": 150},
        "placements": [{"device_id": "mini-ups-200w", "u_start": 9, "u_height": 2}],
    }
    r = client.post("/api/v1/validate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is False
    assert any("exceeds rack height" in w for w in body["warnings"])
