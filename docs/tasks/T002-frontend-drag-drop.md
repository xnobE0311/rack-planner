---
task_id: T002
title: Add drag-and-drop placement UI
status: todo
priority: P1
effort: L
area: [frontend]
depends_on: []
assignee: unassigned
created_at: "2026-03-11"
updated_at: "2026-03-11"

acceptance_criteria:
  - "Users can drag a device from the library into a rack U position."
  - "Placement prevents overlap in the UI before submit."
  - "Keyboard-accessible fallback interaction is documented."

tests:
  - "cd frontend && npm run build"
---

## Background
The current UI adds devices by click only. Drag-and-drop is needed for a realistic planner workflow.
