---
task_id: T001
title: Extend backend validation to cover venting and cable rules
status: todo
priority: P1
effort: M
area: [backend]
depends_on: []
assignee: unassigned
created_at: "2026-03-11"
updated_at: "2026-03-11"

acceptance_criteria:
  - "Validation flags devices whose venting requirements are blocked by rack boundaries or adjacent placements."
  - "Validation returns structured warnings with stable wording suitable for tests."
  - "New pytest cases cover at least one venting failure and one cable-clearance failure."

tests:
  - "cd backend && pytest -q"
---

## Background
The current validator checks height, overlap, width, and depth clearance. Venting and cable-routing rules are still planned.

## Implementation notes
Update `backend/rack_planner/app.py` and extend tests in `backend/tests/test_api.py`.
