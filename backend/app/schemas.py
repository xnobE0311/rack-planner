"""Pydantic schemas for the Rack‑Planner backend.

These models define the structure of devices, rack specifications and placement
records used by the FastAPI backend. They mirror the JSON schema outlined in
the project architecture document.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class NetworkPort(BaseModel):
    """A network port definition for a device.

    Attributes:
        type: The physical connector type (e.g. "RJ45", "SFP").
        count: The number of ports of this type.
        speed_gbps: Optional speed in gigabits per second for each port.
    """

    type: str
    count: int
    speed_gbps: Optional[float] = None


class Venting(BaseModel):
    """Ventilation openings on a device.

    A boolean flag for each side indicates whether that side must remain
    unobstructed for airflow. If a flag is ``True``, the validation logic
    will ensure there is free space on that side when the device is placed in
    the rack.
    """

    front: bool = False
    rear: bool = False
    sides: bool = False
    top: bool = False


class Device(BaseModel):
    """A piece of equipment that can be mounted in the rack.

    Attributes correspond closely to the JSON examples in ``data/devices``.
    Additional optional fields may be extended as needed.
    """

    id: str
    name: str
    u_height: int = Field(..., alias="u_height")
    width_mm: float
    depth_mm: float
    weight_kg: float
    power_w: float
    network_ports: Optional[List[NetworkPort]] = None
    mount_type: Optional[str] = "front"
    venting: Optional[Venting] = None
    notes: Optional[str] = None


class RackSpec(BaseModel):
    """Specifications describing a rack frame."""

    height_u: int
    width_mm: float
    depth_mm: float
    rear_clearance_mm: float


class DevicePlacement(BaseModel):
    """A planned placement of a device in the rack."""

    device_id: str
    u_start: int
    u_height: int
    offset_mm: Optional[float] = 0.0


class ValidationResponse(BaseModel):
    """Response returned by the validation endpoint.

    The ``ok`` field indicates whether the plan has no violations. ``warnings``
    contains human‑readable strings describing any issues detected.
    """

    ok: bool
    warnings: List[str]