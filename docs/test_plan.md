# Test Plan for Rack‑Planner

This document defines a structured approach to testing **Rack‑Planner**, covering
unit tests, integration tests and end‑to‑end scenarios.  The goal is to
ensure reliability for both human users and automated agents, verify that
requirements are met and catch regressions as new features are added.

## 1 Objectives

1. Verify that the **data model** for devices and racks is correctly
   implemented and that the JSON device library adheres to the schema defined
   in the architecture document【579544912602913†L27-L48】.
2. Validate the **API endpoints** exposed by the FastAPI backend:
   - `/devices` returns the complete list of devices with correct types.
   - `/validate` detects invalid placements (e.g. devices exceeding rack height).
3. Ensure the **frontend** correctly communicates with the backend, renders
   devices and rack views and updates state in response to user actions.
4. Provide a foundation for **end‑to‑end tests** that simulate user
   interaction via a browser, including future features like drag‑and‑drop and
   3D visualisation.
5. Define guidelines for integrating tests into a **continuous integration**
   (CI) pipeline on GitHub.

## 2 Unit tests

### 2.1 Data model and JSON validation (Python)

* Use `pytest` to create test functions in `backend/tests/test_schemas.py`.
* Load example devices from `data/devices/example_devices.json` and check:
  - Each entry can be parsed into a `Device` object from `backend/app/schemas.py`.
  - Required fields (`id`, `name`, `u_height`, `width_mm`, `depth_mm`, `weight_kg`, `power_w`) are present.
  - Numeric fields are positive and within reasonable bounds (e.g. `u_height` ≥ 1).
* Test `RackSpec` and `DevicePlacement` models accept valid input and reject
  invalid data (e.g. negative heights).

### 2.2 Backend endpoints

* Create a test client using FastAPI’s `TestClient`:

  ```python
  from fastapi.testclient import TestClient
  from backend.app.main import app

  client = TestClient(app)
  ```

* **/devices** – Perform a GET request and assert that the response has
  status code 200 and returns a JSON array of devices.  Verify that the first
  device matches the content of `example_devices.json`.
* **/validate** – Submit valid and invalid plans:
  - A plan where all devices fit within the rack should return `ok: true` and
    an empty `warnings` list.
  - A plan with a device starting at a negative U or exceeding the rack height
    should return `ok: false` and include the appropriate warning message.

### 2.3 Frontend components (JavaScript)

* Use `Jest` with `@testing-library/react` to test React components in
  `frontend/src`:
  - **DeviceLibrary** renders a list of devices and calls the `onAdd` handler when
    an item is clicked.
  - **RackDesigner** updates the rack specification state when inputs are
    changed.
  - **RackView** displays the correct number of U slots and spans devices
    across multiple rows.
* Mock API calls using `axios-mock-adapter` or similar so that frontend tests
  do not require a running backend.

## 3 Integration tests

Integration tests verify that multiple components work together.

* **Backend–frontend integration** – Use `vite-node` or a minimal express
  server to serve the built frontend, then start the FastAPI backend in a
  separate thread within the test environment.  Simulate HTTP requests
  via the browser (or `axios`) to ensure that the frontend fetches the
  device library and updates the UI accordingly.
* Verify that adding a device through the UI results in the correct
  placement state and that updating rack parameters re-renders the rack view.

## 4 End‑to‑end (E2E) tests

End‑to‑end tests simulate real user interactions in a browser and are
especially useful for verifying complex features such as drag‑and‑drop or
Three.js visualisation.  Use a framework like **Playwright** or **Cypress**.

Example scenarios:

1. **Load the planner** – Navigate to `http://localhost:5173` and verify
   that the device library and rack configuration form render correctly.
2. **Add a device** – Click on a device in the library and ensure it appears
   in the rack view at the expected U position.  Check that the warning
   notification appears if the rack is full.
3. **Change rack height** – Modify the height from 10U to 8U and ensure that
   existing devices are validated and warnings are displayed if necessary.
4. **Fetch new devices** – Edit `example_devices.json` to add a new device,
   reload the frontend and verify that the new device appears in the library.
5. **Pending features** – Once drag‑and‑drop or 3D viewing is implemented,
   simulate dragging a device into place and rotating the rack.

These tests can be run against a deployed preview of the application in CI.

## 5 Continuous integration

To maintain quality as the project evolves, set up a GitHub Actions workflow
that performs the following steps on each pull request:

1. **Install dependencies** for both backend and frontend.
2. **Run Python unit tests** using `pytest`.
3. **Run JavaScript unit tests** using `npm test`.
4. **Build the frontend** with `npm run build` to ensure there are no
   compilation errors.
5. (Future) **Run E2E tests** with Playwright or Cypress on the built site.

This workflow will provide immediate feedback to contributors and AI agents
about regressions or breaking changes.

## 6 Manual testing guidelines

Not all tests can be automated, especially in the early stages of development.
Manual testers should:

1. Verify that the backend starts without errors using the commands in the
   quick‑start guide.
2. Use the frontend to add and remove devices, change rack dimensions and
   observe how the UI responds.  Compare the behaviour with the requirements
   outlined in `docs/architecture.md` and the milestones in the README.
3. Confirm that ventilation and cable management recommendations are followed
   when placing devices (once implemented)【345713078156390†L198-L205】.

Document any issues found in GitHub issues with clear reproduction steps.

## 7 Future extensions

As the project grows to include thermal modelling, electrical load analysis
and AI‑assisted layout suggestions, the test plan should be extended to cover
those areas.  For example, tests could compare predicted temperatures
against known good baselines or verify that the AI suggestions respect all
clearance rules.