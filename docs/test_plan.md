# Test plan

This test plan is meant to be executable, not only descriptive.

## Backend

### Schema and device-library tests

Purpose:

- verify `default_devices.json` exists
- verify each entry parses into the backend `Device` schema
- catch data-shape drift early

Run:

```bash
cd backend
pip install -e ".[dev]"
pytest
```

### API smoke tests

Purpose:

- verify `/health` works
- verify `/api/v1/devices` returns a list
- verify `/api/v1/validate` handles valid and invalid plans

Run:

```bash
cd backend
pip install -e ".[dev]"
pytest
```

## Frontend

Current minimum CI gate:

- dependency install succeeds
- production build succeeds

Run:

```bash
cd frontend
npm install
npm run build
```

## CI

GitHub Actions should run:

1. backend install and pytest
2. frontend install and build
3. upload built frontend artifact for debugging

## Planned future tests

- frontend unit tests with Vitest + Testing Library
- e2e tests with Playwright
- visual regression tests for rack layouts
- validation tests for venting and cable rules
