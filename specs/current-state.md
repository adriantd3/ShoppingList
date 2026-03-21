# Current State

## Snapshot
Date: 2026-03-21
Method: Spec-Driven Development through phase-3 planning for UI feature
Context: Brownfield repository with existing frontend and backend codebases, with new target architecture decisions

## What Exists
- Agent customizations in `.github/`.
- `spec-workflow` installed via `npx skills` in project scope (`.agents/skills/`).
- Initial requirements elicitation agent and skill available.
- Existing implementation structure under `frontend/` and `backend/`.
- Updated MVP feature specs with requirement IDs and acceptance criteria:
	- `001-auth.md`
	- `002-dashboard.md`
	- `003-shared-realtime-list.md`
	- `004-template-and-reset.md`
	- `005-platform-and-stack.md`
	- `006-ui-screen-map.md`
	- `007-backend-core.md`
- Phase-2 technical design drafted for feature `006`:
	- `006-ui-screen-map-design.md`
- Phase-3 task breakdown drafted for feature `006`:
	- `006-ui-screen-map-tasks.md`
- Phase-2 technical design drafted for feature `007`:
	- `007-backend-core-design.md`
- Phase-3 task breakdown drafted for feature `007`:
	- `007-backend-core-tasks.md`
- Confirmed MVP stack direction:
	- Frontend: React Native + Expo
	- UI Library: Tamagui (primary for new MVP screens)
	- Frontend Runtime Policy: full rebuild from scratch for MVP
	- Dependency Policy: start from current stable dependency versions
	- Backend: FastAPI (Python)
	- Database: PostgreSQL
	- Realtime: WebSocket + PostgreSQL LISTEN/NOTIFY
	- Auth: FastAPI Users + JWT + OAuth (Google/Apple)
	- Push Permission UX: request during first-run onboarding

## Open Gaps
- No implementation tasks executed yet for the new MVP specs.
- Traceability entries still point to planned code/test paths (placeholders) until implementation begins.
- No migration execution yet from Java modules to Python runtime path.
- No frontend migration execution yet from existing UI components to Tamagui.
- UI screen-map, technical design, and implementation task breakdown are defined for feature 006.
- Backend planning feature 007 requirements, technical design, and task breakdown are drafted.
- No explicit performance/load validation runs yet for NFR targets.

## Next Actions
1. Create implementation plan per feature with impact labels:
	- `001-auth`: full-stack
	- `002-dashboard`: full-stack
	- `003-shared-realtime-list`: full-stack
	- `004-template-and-reset`: full-stack
	- `005-platform-and-stack`: backend + frontend + devops
2. Define initial FastAPI project skeleton and local compose services.
3. Define Tamagui design tokens and base component layer for React Native screens.
4. Begin phase-4 execution for `006-ui-screen-map` following `006-ui-screen-map-tasks.md`.
5. Implement auth and list domains first (`001`, `002`) to unlock MVP usage.
6. Implement collaboration and reset workflows (`003`, `004`) with integration tests.
7. Produce phase-2 technical design for `007-backend-core` (ER model, architecture, endpoint/event contracts).
8. Begin phase-4 execution for `007-backend-core` following `007-backend-core-tasks.md`.
9. Keep this file updated with requirement-to-code-to-test traceability as implementation progresses.
