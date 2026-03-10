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

Follow these steps to get a local instance of Rack‑Planner running.  The project
is split into a **backend** (Python/FastAPI) and **frontend** (React/Vite).  You
will need Python ≥ 3.10 and Node ≥ 18 installed.

1. **Clone this repository** and change into its directory:

   ```bash
   git clone https://github.com/xnobE0311/rack-planner.git
   cd rack-planner
   ```

2. **Install and run the backend API**:

   ```bash
   # install dependencies
   cd backend
   pip install -r requirements.txt

   # start the API server on http://localhost:8000
   uvicorn app.main:app --reload
   ```

   The API exposes endpoints such as `/devices` (list of available devices) and
   `/validate` (basic rack plan validation).  See `docs/architecture.md` for
   details.

3. **Install and run the frontend** in a separate terminal:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   This will start Vite on [http://localhost:5173](http://localhost:5173).  The
   frontend fetches devices from the backend and allows you to configure the rack
   height, width and depth and add devices by clicking on them in the side bar.

4. **Explore and customise devices**: the example device library is located in
   `data/devices/example_devices.json`.  You can extend it with your own
   equipment by following the schema described in `docs/architecture.md`.  Once
   the backend is running the frontend will automatically load any new devices
   you add to that file.

The project is under active development.  To contribute or follow along,
see [`docs/architecture.md`](docs/architecture.md) for the high‑level design
and [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

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

## Development milestones & AI tasks

Rack‑Planner is designed to be built iteratively.  The following table
summarises the major milestones, their current status and links to further
information.  Each item can be adopted by an AI agent or human contributor
as an **archivable task**—complete the work, document what was done, and
open a pull request.

| Status | Milestone | Description |
| --- | --- | --- |
| ✅ | **Design & documentation** | Initial research into 10‑inch rack standards, creation of the architecture document and example devices.  See `docs/architecture.md` and `data/devices/example_devices.json` for details. |
| ✅ | **Backend & frontend scaffolding** | A minimal FastAPI server and React/Vite frontend have been added.  The backend exposes `/devices` and `/validate`.  The frontend displays a rack designer, device library and simple rack view. |
| 🔜 | **Enhanced validation** | Extend the `/validate` endpoint to check width, depth, venting requirements and cable clearance【145473922566177†L274-L277】【345713078156390†L198-L205】.  Also implement error messages for overlapping devices. |
| 🔜 | **Drag‑and‑drop & UI polish** | Replace the current “click to add” mechanic with drag‑and‑drop using a library like `react-dnd`.  Improve visual styling and accessibility (keyboard navigation, high‑contrast theme). |
| 🔜 | **Three.js 3D viewer** | Implement a basic 3D representation of the rack and devices using Three.js.  Allow rotation, zoom and highlighting of selected units. |
| 🔜 | **Parametric 3D models** | Create OpenSCAD or CadQuery scripts to generate the rack frame, shelves, blanking panels and cable management accessories.  Expose a `/generate-model` API and integrate it into the frontend. |
| 🔜 | **Testing & CI** | Develop unit tests for the backend (using `pytest`) and the frontend (using `Jest` or `Playwright`).  Set up GitHub Actions to run the test suite on each commit. |
| 🔜 | **Device library expansion** | Contribute additional devices (switches, mini servers, PDUs, SBC clusters) following the JSON schema.  Ensure accurate measurements and metadata. |
| 🔜 | **Plan export & import** | Add endpoints and UI to save rack plans as JSON/YAML and reload them later.  Consider integration with GitHub Gists for sharing. |
| 🔮 | **AI‑driven design assistance** | Explore using LLMs to suggest optimal layouts based on device thermal/power profiles and to generate new device definitions from datasheets. |

Each milestone can be tracked via GitHub issues.  When working on a task, ensure
that your commits are **atomic** and well‑documented.  Include references to
relevant citations where appropriate to maintain traceability.

## Testing & quality assurance

Quality is essential for both human users and automated agents.  A comprehensive
test plan is provided in [`docs/test_plan.md`](docs/test_plan.md).  It outlines
unit tests for the data models and backend API, integration tests between the
frontend and backend, and end‑to‑end scenarios that exercise the user
interface.  We encourage contributors to expand the test suite as new
features are added.

## Using this project with AI agents

Rack‑Planner is structured to support development by AI agents as well as
humans.  Each task above is discrete and self‑contained—agents can fetch the
repository, locate the relevant files and implement the feature without
needing full context.  The use of open standards (JSON, HTTP) and modular
components makes it easy to reason about and modify the codebase.

When writing code or documentation as an AI agent:

1. **Be explicit and verifiable** – Clearly describe what your code does,
   reference the applicable requirements and include tests where possible.
2. **Preserve citations** – When referencing external standards or guidance
   (e.g. rack unit dimensions or ventilation recommendations), include
   citations in the format used in this README【145473922566177†L274-L277】.
3. **Archive your work** – Summarise your changes in a commit message or
   documentation update so other agents can understand the project history.

By following these conventions, we aim to build an open, traceable and
sustainable tool for the homelab community.
