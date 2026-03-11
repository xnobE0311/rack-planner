from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class NetworkPort(BaseModel):
    """A network port definition for a device."""

    type: str = Field(..., description='Physical connector type, e.g. "RJ45", "SFP", "SFP+"')
    count: int = Field(..., ge=0)
    speed_gbps: Optional[float] = Field(default=None, ge=0)
    poe: Optional[bool] = Field(default=None, description="Whether ports provide PoE")
    poe_standard: Optional[str] = Field(default=None, description='e.g. "802.3af", "802.3at", "802.3bt"')
    poe_budget_w: Optional[float] = Field(default=None, ge=0, description="Total PoE budget (W)")


class PowerPort(BaseModel):
    """Power connector(s) used by a device."""

    type: str = Field(..., description='e.g. "IEC C14", "IEC C8", "DC barrel", "USB-C PD"')
    count: int = Field(..., ge=0)
    location: str = Field(default="rear", description='e.g. "front", "rear", "side", "internal"')


class Venting(BaseModel):
    """Ventilation requirements for a device."""

    front: bool = False
    rear: bool = False
    sides: bool = False
    top: bool = False
    bottom: bool = False


class Mounting(BaseModel):
    """How a device mounts to the rack rails."""

    face: str = Field(default="front", description='Mounting face, typically "front"')
    hole_span_mm: Optional[float] = Field(default=None, gt=0)
    holes_per_u: int = Field(default=3, ge=1)
    hole_diameter_mm: Optional[float] = Field(default=None, gt=0)
    screw_type: Optional[str] = Field(default=None, description='e.g. "M6", "#10-32"')


class Device(BaseModel):
    """A rack-mountable device definition."""

    id: str
    name: str
    category: Optional[str] = None
    u_height: int = Field(..., ge=1)
    width_mm: float = Field(..., gt=0)
    depth_mm: float = Field(..., gt=0)
    height_mm: Optional[float] = Field(default=None, gt=0)
    weight_kg: float = Field(..., ge=0)
    power_w: float = Field(..., ge=0)
    power_w_max: Optional[float] = Field(default=None, ge=0)
    network_ports: Optional[List[NetworkPort]] = None
    power_ports: Optional[List[PowerPort]] = None
    mount_type: Optional[str] = Field(default="front")
    mount: Optional[Mounting] = None
    venting: Optional[Venting] = None
    cable_clearance_mm: Optional[float] = Field(default=None, ge=0)
    notes: Optional[str] = None


class RackSpec(BaseModel):
    """Specifications describing a rack frame."""

    height_u: int = Field(..., ge=1)
    width_mm: float = Field(..., gt=0)
    depth_mm: float = Field(..., gt=0)
    rear_clearance_mm: float = Field(default=150, ge=0)


class DevicePlacement(BaseModel):
    """A planned placement of a device in the rack."""

    device_id: str
    u_start: int = Field(..., ge=0)
    u_height: Optional[int] = Field(default=None, ge=1)
    offset_mm: float = Field(default=0.0)


class ValidationRequest(BaseModel):
    rack: RackSpec
    placements: List[DevicePlacement] = Field(default_factory=list)


class ValidationResponse(BaseModel):
    ok: bool
    warnings: List[str] = Field(default_factory=list)
