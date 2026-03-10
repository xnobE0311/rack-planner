# Architecture and Design

This document outlines the proposed architecture for **Rack‑Planner**, a 10‑inch mini‑rack simulator and planning tool.  The system is designed to be modular, extensible and sustainable.  It brings together a **web‑based planner**, a **parametric 3D modelling engine**, a **validation backend** and a **device library**.

## 1 Functional requirements

1. **Rack configuration** – The user can specify the rack’s height (in U), width and depth.  Default values follow the widely accepted mini‑rack dimensions: a rack unit is **44.45 mm** high, the distance between vertical posts is **236.525 mm** and usable width is approximately **210–222 mm**【979178008495651†L51-L67】【789130421047180†L129-L140】.  Depth defaults to **310 mm**【230981583912271†L207-L233】 but can be customised.
2. **Device management** – The user can import devices from JSON files or create new devices by providing measurements and metadata: U height, width, depth, weight, power consumption, network ports, front/back orientation and venting requirements.  Devices can be placed, rearranged or removed within the rack via a drag‑and‑drop interface.
3. **Validation** – The backend checks whether each device fits within the rack: width must be ≤ usable width, depth ≤ rack depth minus clearance, and U height must not exceed available slots.  It also verifies that devices requiring front or rear ventilation are not blocked and suggests inserting blanking panels or leaving gaps for airflow【345713078156390†L198-L205】.  It warns if cable management clearance (≥ 150 mm) is insufficient【145473922566177†L274-L277】.
4. **3D visualisation** – The planner renders a 3D representation of the rack and its contents in the browser using **Three.js**.  Users can rotate, zoom and examine the layout, as well as export STL files for 3D printing.
5. **Parametric 3D models** – A set of OpenSCAD/CadQuery scripts generate the rack frame, shelves, blanking panels and cable management accessories based on the chosen dimensions.  Printables use the standard rack unit spacing and hole pattern and provide options for ventilation grills and fan cut‑outs.
6. **Export & share** – Plans can be exported as JSON or YAML, including rack parameters and device positions.  Future versions may allow sharing with other users via GitHub or a cloud service.
7. **Sustainability** – All code, models and data are open source (MIT Licence).  The project encourages reuse of existing hardware and 3D‑printed parts to minimise waste.  Documentation emphasises best practices for airflow and cable management to prolong equipment life.

## 2 Non‑functional requirements

- **Open source** – Source code, documentation and models are licensed under MIT to encourage community contributions.
- **Modularity** – The frontend, backend and modelling components are loosely coupled.  Each can be replaced (e.g., backend could be written in Python or Node) without changing the overall system.
- **Performance** – The planner should maintain interactive frame rates (> 30 fps) when rendering up to 10U of devices.  JSON file operations and validation must be responsive.
- **Portability** – Code should run on Windows, macOS and Linux.  The only build dependencies are Python ≥ 3.10, Node ≥ 18 and a C++ compiler for OpenSCAD.
- **Internationalisation** – Measurements are stored in SI units (millimetres).  The UI offers toggles between metric and imperial units; conversions are handled in the frontend.
- **Accessibility** – Use semantic HTML and ARIA labels.  Provide keyboard navigation and high‑contrast themes.

## 3 System components

### 3.1 Data model

- **Device** – Represented as a JSON object:

  ```json
  {
    "id": "unique-device-id",
    "name": "16‑Port PoE Switch",
    "u_height": 1,
    "width_mm": 195,
    "depth_mm": 180,
    "weight_kg": 1.8,
    "power_w": 60,
    "network_ports": [
      { "type": "RJ45", "count": 16, "speed_gbps": 1 },
      { "type": "SFP",  "count": 2,  "speed_gbps": 10 }
    ],
    "mount_type": "front",
    "venting": {
      "front": true,
      "rear": false,
      "sides": false,
      "top": false
    },
    "notes": "Ports are on the front; allow 50 mm clearance in front for cables."
  }
  ```

  Additional optional fields include `color`, `manufacturer`, `model`, `power_connectors` and `cable_clearance_mm`.

- **Rack** – Defined by:
  - `height_u` – total number of U (default 10).
  - `width_mm` – distance between posts (default 236.525 mm).  `usable_width_mm` is derived (≈210–222 mm).
  - `depth_mm` – maximum depth of equipment (default 310 mm).
  - `rear_clearance_mm` – extra space behind devices for cables and airflow (default 150 mm)【145473922566177†L274-L277】.
  - `rail_pattern` – specification of hole spacing (standard: 15.9 mm top gap + 15.9 mm middle + 15.9 mm bottom for each U).
  - `mounting_hardware` – screw type (M6, #10‑32), cage nuts, etc.

- **Plan** – A list of device placements including `device_id`, `u_start` (bottom U index), `u_height` and optional `offset_mm` for horizontal or depth adjustments.

### 3.2 Backend

The backend will be implemented with **FastAPI** (Python) to leverage Pydantic for data validation.  Key services include:

1. **/validate** – Accepts a rack specification and a list of device placements, checks fit constraints, ventilation and clearance.  Returns warnings and recommended adjustments.
2. **/devices** – Serves the library of devices from `data/devices/`.  Supports CRUD operations so users can add their own devices.
3. **/generate-model** – Calls OpenSCAD/CadQuery scripts to generate STL files for the rack frame or accessories.  Parameters include rack dimensions, vent hole patterns and optional fan cut‑outs.  Files are saved to a temporary directory and returned for download.
4. **/plan** – Stores and retrieves saved plans (future feature).  Integration with GitHub could allow storing plans as gists or repository files.

The backend will unit‑test each service and use continuous integration (GitHub Actions) to ensure correctness.

### 3.3 Frontend

The UI will be a single‑page application built with **React** and **Three.js**.  Core features include:

1. **Rack designer** – A panel where users set the rack height, width and depth.  Presets for common sizes are available.
2. **Device library** – A searchable list of devices loaded from the backend.  Users drag devices onto the rack view.
3. **3D viewer** – Renders the rack and its contents.  Each U slot is highlighted when a device is selected.  Devices can be moved between slots or rotated.  The viewer displays warnings (e.g., depth overflow, blocked vents) as icons or overlays.
4. **Device editor** – Forms to create or edit devices, with fields matching the `Device` schema.  Real‑time validation ensures width/depth are within plausible ranges.
5. **Export & print** – Buttons to export the plan as JSON/YAML and to request STL generation via the `/generate-model` endpoint.

### 3.4 3D modelling

The repository will include **OpenSCAD** and **CadQuery** scripts in `scripts/models/`.  These scripts parameterise all dimensions and generate parts such as:

- **Frame rails** – Vertical posts with mounting holes spaced 236.525 mm apart and standard U spacing.  Options for M6 or #10‑32 holes.
- **Horizontal braces** – Connect the posts; available with solid or vented patterns.  Vented braces improve airflow.
- **Side panels** – Optional; can be 3D printed or laser cut.  Side panels may include mesh or fan cut‑outs for improved cooling.
- **Shelves and blanking panels** – Sized to fit 10‑inch width; blanking panels cover unused U spaces to prevent recirculation【345713078156390†L198-L205】.
- **Cable management rings and bars** – Attach to the rear of the rack to separate data and power cables, reducing electromagnetic interference【509432572594291†L62-L100】.

Users can modify these scripts or pass different parameters via the backend to generate custom parts.  The scripts should be documented and tested to ensure they produce printable geometries for typical FDM printers (250 mm×250 mm bed, 0.4 mm nozzle).

## 4 Development workflow

1. **Planning phase** – Document requirements, gather device measurements, and design the data model (this phase).
2. **Prototype backend** – Implement the FastAPI services, data models and initial validation logic.  Develop unit tests for width/height/depth checks and ventilation clearance.  Use example devices from `data/devices/example_devices.json`.
3. **Prototype frontend** – Create the React app with Three.js integration.  Render a simple rack and allow adding/removing devices.  Integrate with backend for validation and device data.
4. **Iterative refinement** – Add features such as saving plans, exporting to STL, metric/imperial toggle, and accessibility improvements.
5. **Community contributions** – Encourage external contributors to submit devices, bug fixes, new features and translations.  Use issues and pull requests to track work.  Follow the guidelines in `CONTRIBUTING.md`.

## 5 Sustainability considerations

Rack‑Planner emphasises **reuse** and **low‑waste design**:

- **3D printing** allows you to produce only the parts you need, reducing shipping emissions and enabling repairs.  The parametric models are optimised for minimal support material and standard printer sizes.
- **Modular design** means you can upgrade or replace individual components (e.g., swap a 2U shelf for a 4U shelf) without discarding the entire rack.  The planner encourages efficient use of space to reduce the number of parts printed.
- **Cable management** recommendations (separate power and data cables, use labels, secure with clips) improve airflow and reduce the risk of overheating【509432572594291†L62-L100】.
- **Ventilation** guidance (leave spare depth for cables, insert blanking panels to prevent recirculation) prolongs device life and lowers energy consumption【145473922566177†L274-L277】【345713078156390†L198-L205】.

## 6 Future work

This architecture lays the foundation for a comprehensive mini‑rack planning system.  Future enhancements may include:

- **Electrical load calculations** – Summing device power requirements and verifying that a selected PDU or UPS can handle the load.
- **Thermal modelling** – Estimating heat generation and suggesting active cooling (fans, ventilation holes) based on device TDPs.
- **Integration with purchasing APIs** – Linking to vendors or marketplaces for off‑the‑shelf mini‑rack gear, PDUs and accessories.
- **GitHub integration** – Allowing users to store and version‑control plans directly in their GitHub repositories.

By following this architecture and the best practices cited in the documentation, the Rack‑Planner project aims to provide a sustainable, flexible and accessible tool for designing compact network racks.