---
task_id: T003
title: Implement Three.js 3D rack viewer MVP
status: todo
priority: P2
effort: L
area: [frontend]
depends_on: [T002]
assignee: unassigned
created_at: "2026-03-11"
updated_at: "2026-03-11"

acceptance_criteria:
  - "The app renders a simple 3D rack frame and placed devices."
  - "Users can orbit, pan, and zoom."
  - "The viewer uses rack dimensions from current planner state."

tests:
  - "cd frontend && npm run build"
---

## Background
A 3D viewer is one of the core differentiators of Rack-Planner but is not yet implemented.
