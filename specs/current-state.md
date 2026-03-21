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
- Milestone A (feature 007 tasks 1-6) implemented in `backend/python-api`:
	- UV-managed FastAPI skeleton and module boundaries (`app/core`, `app/api`, `app/modules`, `app/db`, `tests`).
	- Security baseline with environment-only secret config, production safety checks, and log redaction.
	- Database foundation with SQLAlchemy models and Alembic baseline migration.
	- Auth baseline (JWT issue/verify + login contract) and WebSocket token extraction helper.
	- Authorization policy baseline with deny-by-default list membership/owner checks.
	- Standardized error contract with stable error codes and trace IDs.
	- Validation baseline executed successfully (`ruff`, `mypy`, `pytest`).
- Test layout convention normalized for backend Python API:
	- Removed unused `backend/python-api/app/tests` remnant.
	- Tests organized by layer and module under `backend/python-api/tests/unit/<module>/` and `backend/python-api/tests/integration/<module>/`.
	- Structural guard test added to fail CI if `app/tests` or flat test files under layer roots reappear.

## Open Gaps
- No migration execution yet from Java modules to Python runtime path.
- No frontend migration execution yet from existing UI components to Tamagui.
- UI screen-map, technical design, and implementation task breakdown are defined for feature 006.
- No explicit performance/load validation runs yet for NFR targets.
- Feature 007 tasks 9-20 remain pending (sharing lifecycle, reset/restore, realtime, hardening, full contract/integration/realtime suites).

## Traceability Update (Feature 007 Milestone A-B)
- FR-backend-11, NFR-01, NFR-03
	- Code: `backend/python-api/app/main.py`, `backend/python-api/pyproject.toml`
	- Tests: `backend/python-api/tests/test_health.py`
- FR-backend-10, NFR-02
	- Code: `backend/python-api/app/core/config.py`, `backend/python-api/app/core/logging.py`, `backend/python-api/app/core/errors.py`
	- Tests: `backend/python-api/tests/test_error_contract.py`
- FR-backend-01, FR-backend-02
	- Code: `backend/python-api/app/db/models.py`, `backend/python-api/migrations/env.py`, `backend/python-api/migrations/versions/20260321_0001_backend_core_baseline.py`
	- Tests: validation gate (`uv run mypy app tests`, `uv run ruff check .`)
- FR-backend-03, FR-backend-05
	- Code: `backend/python-api/app/modules/auth/dependencies.py`, `backend/python-api/app/modules/auth/service.py`, `backend/python-api/app/modules/lists/policies.py`, `backend/python-api/app/api/ws/auth.py`
	- Tests: `backend/python-api/tests/test_security.py`, `backend/python-api/tests/test_error_contract.py`
- FR-backend-03, FR-backend-08 (Milestone B - Task 7)
	- Code: `backend/python-api/app/api/rest/v1/endpoints/lists.py`, `backend/python-api/app/modules/lists/schemas.py`, `backend/python-api/app/modules/lists/catalogs.py`, `backend/python-api/app/modules/lists/service.py`, `backend/python-api/app/modules/lists/repository.py`
	- Tests: `backend/python-api/tests/integration/lists/test_contract.py`
- FR-backend-06 (Milestone B - Task 8)
	- Code: `backend/python-api/app/core/idempotency.py`, `backend/python-api/app/api/rest/v1/endpoints/lists.py`, `backend/python-api/app/db/models.py`, `backend/python-api/app/core/config.py`, `backend/python-api/migrations/versions/20260321_0002_task8_idempotency_records.py`
	- Tests: `backend/python-api/tests/unit/core/test_idempotency.py`, `backend/python-api/tests/integration/lists/test_idempotency_contract.py`

## Validation Evidence (Task 8)
- `uv run ruff check .` -> pass
- `uv run mypy app tests` -> pass
- `uv run pytest` -> pass (21 passed, 3 warnings)

## Security Notes (Task 8)
- Risks considered: duplicate replayed mutations, ambiguous idempotency key reuse with altered payloads, and replay-store growth.
- Controls applied: optional `Idempotency-Key` handling on mutating list/item endpoints, request fingerprinting with deterministic scope, persistent response replay with configurable TTL, and stable 409 conflict contract using `IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD`.
- Residual risks: concurrent first-write races can still execute duplicate side effects under high contention before persistence conflict resolution.

## Next Actions
1. Create implementation plan per feature with impact labels:
	- `001-auth`: full-stack
	- `002-dashboard`: full-stack
	- `003-shared-realtime-list`: full-stack
	- `004-template-and-reset`: full-stack
	- `005-platform-and-stack`: backend + frontend + devops
2. Continue Milestone B for feature 007 (tasks 9-10): sharing lifecycle, reset/restore semantics.
3. Define Tamagui design tokens and base component layer for React Native screens.
4. Begin phase-4 execution for `006-ui-screen-map` following `006-ui-screen-map-tasks.md`.
5. Implement auth and list domains first (`001`, `002`) to unlock MVP usage.
6. Implement collaboration and reset workflows (`003`, `004`) with integration tests.
7. Extend backend test suites with integration and contract coverage for new routes.
8. Add security hardening controls (rate limiting, strict body/content limits, CORS policy finalization) in Milestone C.
9. Keep this file updated with requirement-to-code-to-test traceability as implementation progresses.
