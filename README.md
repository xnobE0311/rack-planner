# Rack‑Planner – a 10‑inch Mini‑Rack Simulator

Rack‑Planner is an open‑source project aimed at homelab and maker communities who need a **portable, highly‑customisable 10‑inch rack**.  It combines a flexible data model for defining devices, a 3D modelling pipeline for generating printable rack parts, and an interactive web interface that allows you to plan your rack layout before you buy or print any parts.

## Why a 10‑inch rack?

Most IT and networking equipment is designed around the 19‑inch rack standard, but there is a growing interest in compact **10‑inch or half‑rack** form factors for home and small‑office environments.  Unlike 19‑inch racks there is **no official 10‑inch standard** – it’s more of a community consensus.  Nevertheless, most manufacturers follow the same vertical *rack unit* (U) spacing (1U = **44.45 mm** or 1.75 inches) and keep the mounting holes **236.525 mm (≈ 9.312 inches)** apart【979178008495651†L51-L67】.  That translates to roughly **210 mm (8.45 inches) of usable horizontal space** inside the rack【979178008495651†L51-L67】.

Commercial mini racks tend to fix the depth at around **310 mm** and are available in heights from **4U to 15U**【230981583912271†L207-L233】.  Some 3D‑printed systems such as *Lab Rax* adopt similar dimensions, using the standard 44.45 mm rack unit spacing, hole spacing of 236.525 mm and a usable width of **about 222 mm**【789130421047180†L129-L140】.  Rack‑Planner allows you to vary these dimensions so that you can accommodate off‑the‑shelf gear or custom printed hardware.

### Ventilation and cable management

Good airflow and cable routing are critical for any rack.  Industry guidance for 19‑inch racks applies equally well to mini racks – leave **at least 150 mm (6 inches) of extra depth** behind your equipment to accommodate cables and prevent hot air recirculation【145473922566177†L274-L277】.  Use **blanking panels** to cover empty U spaces and prevent hot air from flowing through unused areas【345713078156390†L198-L205】.  Keep power and data cables separated, label them clearly and secure them to cable managers to reduce strain【509432572594291†L62-L100】.  These practices improve cooling efficiency, simplify maintenance and extend the life of your equipment.

## Project goals

Rack‑Planner’s primary goal is to provide a **full suite of tools** for designing and building a customised 10‑inch rack:

- **Interactive planner** – A browser‑based interface (React + Three.js) will let you pick the rack height (up to 10U by default), choose the width/depth, and place devices on virtual rack rails.  Drag‑and‑drop devices, view available U slots and verify clearances for ventilation and cable routing.
- **Parametric 3D models** – Scripts built with [OpenSCAD](https://openscad.org) or [CadQuery](https://cadquery.readthedocs.io) will generate printable STL files for rack frames, shelves and accessories.  Parameters include height (in U), width (in mm), depth, hole spacing and vent patterns.
- **Device library** – JSON files in `data/devices/` contain measurements and metadata for common mini‑rack devices (switches, patch panels, mini servers, SBC clusters, UPS modules).  You can also create your own devices by specifying U height, width, depth, weight, power consumption and port types.
- **Validation engine** – A backend (Python + FastAPI) will accept device lists and rack parameters, check whether everything fits (width & depth constraints, U spacing, required ventilation clearance), and produce a summary or exportable plan.  It will flag conflicts like insufficient depth or blocked vents.
- **Sustainability and openness** – Everything in this repository is licensed under the **MIT Licence**, contributions follow an open‑governance model, and the project encourages reuse of existing gear and 3D‑printed parts to reduce waste.

## Quick start

1. **Clone this repository** and install the dependencies (Python ≥ 3.10 and Node ≥ 18).  Detailed instructions will be added once the backend and frontend prototypes are ready.
2. **Run the backend API**: `uvicorn src/api.main:app --reload`
3. **Run the frontend**: `npm install && npm run dev`
4. **Experiment with devices**: explore `data/devices/example_devices.json`, then add your own entries.  Use the planner UI to drag devices into your rack and see whether they fit.

This repo is currently a design document and data library.  The software itself will be developed in phases.  See `docs/architecture.md` for the system design and `CONTRIBUTING.md` for how to get involved.

## Default mini‑rack dimensions

The table below summarises commonly used dimensions for 10‑inch racks.  These values are used as defaults in the planner but can be overridden when designing your own rack.

| Parameter | Value | Source |
| --- | --- | --- |
| Rack unit height (1U) | **44.45 mm (1.75 inches)** | EIA‑310 standard【145473922566177†L127-L143】 |
| Hole spacing between posts | **236.525 mm (9.312 inches)** | Project Mini Rack【979178008495651†L51-L67】 |
| Maximum usable width | **≈210 mm (8.45 inches)** | Project Mini Rack【979178008495651†L51-L67】 |
| Typical external width | **10 inches (distance between profiles)** | ServerRack24 knowledge base【230981583912271†L207-L233】 |
| Typical depth | **310 mm** | ServerRack24 knowledge base【230981583912271†L207-L233】 |
| Recommended rear clearance | **≥150 mm (6 inches)** | Server rack airflow guidelines【145473922566177†L274-L277】 |
| Preferred hole spacing in printable racks | **236.525 mm, 44.45 mm U spacing, usable width 222 mm** | Lab Rax article【789130421047180†L129-L140】 |

## Documentation

- **System architecture** – See [`docs/architecture.md`](docs/architecture.md) for detailed design of the backend, frontend and data models.
- **Contributing guide** – See [`CONTRIBUTING.md`](CONTRIBUTING.md) for instructions on how to contribute, report issues or request new features.
- **License** – The project is licensed under the [MIT Licence](LICENSE).

## Citation and research

This repository was assembled using information from a variety of sources.  Key references include Jeff Geerling’s [Project Mini Rack](https://github.com/geerlingguy/mini-rack) for unofficial 10‑inch standards【979178008495651†L51-L67】, the ServerRack24 knowledge base for commercial rack dimensions【230981583912271†L207-L233】, the Lab Rax 3D‑printable rack system for printable design cues【789130421047180†L129-L140】, Pelonis Technologies and Medium articles for airflow and cable management best practices【345713078156390†L198-L205】【509432572594291†L62-L100】, and ACDCFAN’s server rack dimension guide for standard rack unit definitions【145473922566177†L127-L143】【145473922566177†L274-L277】.
