# CONTRIBUTING_AI.md

This project is intentionally structured for **AI-continuable development**.

## Operating rules for AI agents

1. Work from small, atomic tasks.
2. Prefer modifying the minimum number of files required.
3. Keep behavior deterministic and configurable through environment variables.
4. Do not introduce hidden services, background daemons, or undocumented state.
5. Update tests and documentation in the same change whenever behavior changes.
6. Preserve backwards compatibility unless a task explicitly allows breaking changes.
7. Use versioned API routes for new backend behavior.
8. Do not hardcode local machine paths, ports, or credentials.
9. Treat `data/devices/default_devices.json` as CI-stable seed data.
10. When adding a new task, create a file from `docs/tasks/TEMPLATE.md`.

## Required validation before proposing a commit

Run the smallest applicable validation set:

```bash
make backend-test
make frontend-build
```

If Docker-related files changed, also validate:

```bash
docker compose config
```

## Commit style

Prefer conventional commits:

- `feat:` new capability
- `fix:` bug fix
- `docs:` documentation only
- `test:` tests only
- `chore:` maintenance / infra
- `refactor:` structural change without behavior change

## Definition of done

A change is considered done when:

- acceptance criteria in the task are satisfied
- documentation is updated if needed
- tests pass or test gaps are explicitly documented
- the change can be reviewed independently
