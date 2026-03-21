# AGENTS

Repository agent guidance is centralized in `.github/AGENTS.md`.

For feature work, agents should follow Spec-Driven Development using:
- `specs/project.md`
- `specs/conventions.md`
- `specs/current-state.md`
- `specs/features/*.md`

Brownfield constraint:
- This repository already has `frontend/` and `backend/` code.
- Specs and implementation plans must explicitly state affected side (`frontend`, `backend`, or both).

Cross-provider defaults (apply regardless of agent provider):
- For non-trivial tasks, plan first (3+ steps or architectural decisions).
- Update specs before implementation and keep requirement-to-code-to-test traceability explicit.
- Verify before done: tests/logs/diffs when relevant.
- For bug reports, reproduce and fix directly with minimal user context switching.
- Prefer simple, minimal, root-cause fixes over temporary patches.

Task flow:
1. Read `specs/project.md`, `specs/conventions.md`, `specs/current-state.md`, and target `specs/features/*.md`.
2. Confirm impact scope: `frontend`, `backend`, or both.
3. Implement incrementally and validate.
4. Update `specs/current-state.md` with status and traceability notes.

Detailed registry, subagents, and project-specific execution policy remain in `.github/AGENTS.md`.

