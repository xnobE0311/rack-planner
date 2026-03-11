# Architecture

Rack-Planner is a web app for planning 10-inch mini rack layouts.

Core capabilities:

- device metric library
- rack U-position planning
- validation of fit and clearance
- future 3D viewer
- future parametric printable parts

## Design principles

- API-first so agents can work headlessly
- deterministic environments via Docker and CI
- stable contracts via `/api/v1`
- metrics stored in millimetres as canonical units
- small, archivable task slices

## Backend

Location:

- `backend/rack_planner/app.py`
- `backend/rack_planner/schemas.py`

Key endpoints:

- `GET /health`
- `GET /api/v1/devices`
- `POST /api/v1/validate`

Legacy endpoints are temporarily kept for early compatibility.

### Validation v1

Current scope:

- rack height overflow
- overlap detection
- width check
- depth check with rear/cable clearance

Planned scope:

- venting constraints
- cable routing constraints
- thermal estimation
- power budget validation
- save/load plans

## Frontend

Location:

- `frontend/src/App.jsx`
- `frontend/src/components/*`

Current scope:

- fetch device library from backend
- configure rack dimensions
- place devices using first-fit U allocation
- display a simple 2D rack layout

Planned scope:

- drag-and-drop placement
- richer validation feedback
- 3D viewer with Three.js
- import/export plans

## Data

Device files live under `data/devices/`.

Recommended baseline:

- `default_devices.json` for CI/demo stability
- `example_devices.json` for experimentation

The backend can override device sources using:

- `RACK_PLANNER_DEVICES_PATH`
- `RACK_PLANNER_DEVICES_DIR`

## Package structure

```text
backend/
  rack_planner/
    __init__.py
    app.py
    schemas.py
  tests/
frontend/
  src/
data/
  devices/
docs/
  tasks/
```

## Why this structure is AI-friendly

- backend can be installed with `pip install -e .[dev]`
- frontend can be built deterministically
- CI can check both layers separately
- tasks can be written as atomic markdown files
- the device library is machine-readable JSON
