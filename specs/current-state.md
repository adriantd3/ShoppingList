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
- Feature 007 Milestone D is complete (tasks 15-20 executed: contract/realtime integration suites, security evidence rollup, contract publication, and final traceability sweep).

## Milestone D Execution Status (Feature 007)
- Completed scope:
	- Contract suite expansion for auth and websocket envelope validation.
	- Realtime integration coverage for fan-out, ordering, and membership transition behavior.
	- Endpoint-level security checklist and residual risk register.
	- Published OpenAPI snapshot and WebSocket event catalog.
	- Full traceability/state synchronization.
- Impact scope executed: backend (`backend/python-api`, `backend/openapi`, `docs/`, and specs traceability updates).

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
- FR-backend-03, FR-backend-09 (Milestone B - Task 9)
	- Code: `backend/python-api/app/api/rest/v1/endpoints/sharing.py`, `backend/python-api/app/modules/sharing/schemas.py`, `backend/python-api/app/modules/sharing/repository.py`, `backend/python-api/app/modules/sharing/service.py`, `backend/python-api/app/db/models.py`, `backend/python-api/migrations/versions/20260321_0003_task9_share_links_audit.py`, `backend/python-api/app/api/rest/v1/router.py`
	- Tests: `backend/python-api/tests/integration/sharing/test_sharing_contract.py`, `backend/python-api/tests/unit/sharing/test_service.py`
- FR-backend-03, FR-backend-07 (Milestone B - Task 10)
	- Code: `backend/python-api/app/api/rest/v1/endpoints/lists.py`, `backend/python-api/app/modules/lists/schemas.py`, `backend/python-api/app/modules/lists/service.py`, `backend/python-api/app/modules/lists/repository.py`
	- Tests: `backend/python-api/tests/integration/lists/test_reset_restore_contract.py`, `backend/python-api/tests/unit/lists/test_reset_restore_service.py`

## Traceability Update (Feature 007 Milestone C)
- FR-backend-04, FR-backend-05 (Task 11)
	- Code: `backend/python-api/app/api/ws/router.py`, `backend/python-api/app/modules/realtime/schemas.py`, `backend/python-api/app/modules/realtime/repository.py`, `backend/python-api/app/modules/realtime/service.py`, `backend/python-api/app/modules/realtime/manager.py`, `backend/python-api/app/main.py`
	- Tests: `backend/python-api/tests/integration/core/test_ws_contract.py`, `backend/python-api/tests/unit/realtime/test_realtime_service.py`
- FR-backend-04, FR-backend-07 (Task 12)
	- Code: `backend/python-api/app/modules/realtime/events.py`, `backend/python-api/app/modules/lists/service.py`, `backend/python-api/app/modules/sharing/service.py`
	- Tests: `backend/python-api/tests/unit/lists/test_realtime_emission.py`, `backend/python-api/tests/unit/lists/test_reset_restore_service.py`, `backend/python-api/tests/unit/sharing/test_service.py`
- FR-backend-03 (Task 13)
	- Code: `backend/python-api/app/api/rest/v1/endpoints/profile.py`, `backend/python-api/app/api/rest/v1/router.py`, `backend/python-api/app/modules/notifications/schemas.py`, `backend/python-api/app/modules/notifications/repository.py`, `backend/python-api/app/modules/notifications/service.py`
	- Tests: `backend/python-api/tests/integration/core/test_profile_contract.py`
- FR-backend-05, FR-backend-10, NFR-02 (Task 14)
	- Code: `backend/python-api/app/core/rate_limit.py`, `backend/python-api/app/core/config.py`, `backend/python-api/app/core/errors.py`, `backend/python-api/app/main.py`, `backend/python-api/app/api/rest/v1/endpoints/auth.py`, `backend/python-api/app/api/rest/v1/endpoints/sharing.py`
	- Tests: `backend/python-api/tests/integration/core/test_security_hardening.py`, `backend/python-api/tests/integration/core/test_error_contract.py`

## Traceability Update (Feature 007 Backend Architecture Refinement)
- NFR-03 maintainability (request-scoped context hard cutover)
	- Code: `backend/python-api/app/core/request_context.py`, `backend/python-api/app/modules/auth/context.py`, `backend/python-api/app/api/rest/v1/endpoints/lists.py`, `backend/python-api/app/api/rest/v1/endpoints/sharing.py`, `backend/python-api/app/api/rest/v1/endpoints/profile.py`, `backend/python-api/app/modules/lists/service.py`, `backend/python-api/app/modules/sharing/service.py`, `backend/python-api/app/modules/notifications/service.py`
	- Tests: `backend/python-api/tests/unit/lists/test_realtime_emission.py`, `backend/python-api/tests/unit/lists/test_reset_restore_service.py`, `backend/python-api/tests/unit/sharing/test_service.py`, `backend/python-api/tests/integration/core/test_profile_contract.py`, `backend/python-api/tests/integration/lists/test_contract.py`, `backend/python-api/tests/integration/sharing/test_sharing_contract.py`

## Traceability Update (Feature 007 Milestone D)
- FR-backend-03, FR-backend-10, FR-backend-12 (Task 15)
	- Tests: `backend/python-api/tests/integration/core/test_auth_contract.py`, `backend/python-api/tests/integration/core/test_error_contract.py`
- FR-backend-04, FR-backend-12 (Task 15, Task 17)
	- Tests: `backend/python-api/tests/integration/core/test_ws_contract.py`, `backend/python-api/tests/integration/core/test_ws_realtime_integration.py`
- FR-backend-05, FR-backend-06, FR-backend-07, FR-backend-09, FR-backend-12 (Task 16)
	- Tests: `backend/python-api/tests/integration/lists/test_contract.py`, `backend/python-api/tests/integration/lists/test_idempotency_contract.py`, `backend/python-api/tests/integration/lists/test_reset_restore_contract.py`, `backend/python-api/tests/integration/sharing/test_sharing_contract.py`, `backend/python-api/tests/integration/core/test_profile_contract.py`
- FR-backend-10, NFR-02 (Task 18)
	- Evidence: `docs/backend_milestone_d_security_checklist.md`, `backend/python-api/tests/integration/core/test_security_hardening.py`
- FR-backend-03, FR-backend-04, NFR-03 (Task 19)
	- Contracts: `backend/openapi/python-api.openapi.json`, `backend/openapi/python-api-ws-events.md`, `backend/python-api/README.md`

## Validation Evidence (Task 8-10)
- `uv run ruff check .` -> pass
- `uv run mypy app tests` -> pass
- `uv run pytest` -> pass (33 passed, 3 warnings)

## Validation Evidence (Milestone C: Task 11-14)
- `uv run ruff check .` -> pass
- `uv run mypy app tests` -> pass
- `uv run pytest -q` -> pass (52 passed, 3 warnings)

## Validation Evidence (Architecture Refinement)
- `.venv/Scripts/python.exe -m ruff check .` -> pass
- `.venv/Scripts/python.exe -m mypy app tests` -> pass
- `.venv/Scripts/python.exe -m pytest -q` -> pass (52 passed, 3 warnings)

## Validation Evidence (Milestone D: Task 15-20)
- `.venv/Scripts/python.exe -m ruff check .` -> pass
- `.venv/Scripts/python.exe -m mypy app tests` -> pass
- `.venv/Scripts/python.exe -m pytest -q` -> pass (57 passed, 3 warnings)
- `uv pip check` -> pass

## Session Continuity Notes (2026-03-21)
- Local runtime stability hardening completed for backend make/scripts:
	- root `/.env` established as runtime source of truth for backend script actions.
	- migration and seed flows aligned with the same env-loading path.
- Local bootstrap for manual API testing added:
	- dummy-user seeding command available via `make py-backend-seed-dummy-user`.
	- demo credential email uses validator-safe domain (`demo@shoppinglist.dev`).
- Postman reliability improvements added:
	- native collection file added at `backend/openapi/python-api.postman_collection.json` with login token capture and protected-request auth propagation.
- Verification policy refinement:
	- automated tests remain required, but backend/API completion also requires quick manual smoke checks (run app, login, and one protected endpoint).

## Security Notes (Task 8)
- Risks considered: duplicate replayed mutations, ambiguous idempotency key reuse with altered payloads, and replay-store growth.
- Controls applied: optional `Idempotency-Key` handling on mutating list/item endpoints, request fingerprinting with deterministic scope, persistent response replay with configurable TTL, and stable 409 conflict contract using `IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD`.
- Residual risks: concurrent first-write races can still execute duplicate side effects under high contention before persistence conflict resolution.

## Security Notes (Task 9)
- Risks considered: unauthorized share-link consumption, token leakage in persistence, and revoked/expired link reuse.
- Controls applied: token hash-only persistence, authenticated consume path with deterministic revoked/expired conflict responses, membership checks on issue/revoke/expire operations, and revocation actor audit metadata.
- Residual risks: share-link abuse controls and rate limiting remain pending Milestone C hardening.

## Security Notes (Task 10)
- Risks considered: accidental or concurrent reset misuse, restore to stale state, and unauthorized reset/restore operations.
- Controls applied: transactional pre-reset snapshot creation before reset mutation, restore constrained to latest pre-reset snapshot, membership checks on reset/restore endpoints, and deterministic error response when no snapshot exists.
- Residual risks: snapshot pruning/retention automation is pending future hardening work.

## Security Notes (Milestone D)
- Risks considered: contract drift between implementation and published docs, insufficient realtime confidence under collaboration flows, and incomplete deployment security evidence.
- Controls applied: expanded contract/realtime integration suites, OpenAPI and WebSocket contract publication from runtime state, endpoint-level security checklist evidence, and dependency consistency check.
- Residual risks: distributed throttling and cross-process websocket fan-out remain pending beyond MVP single-instance constraints.

## Next Actions
1. Create implementation plan per feature with impact labels:
	- `001-auth`: full-stack
	- `002-dashboard`: full-stack
	- `003-shared-realtime-list`: full-stack
	- `004-template-and-reset`: full-stack
	- `005-platform-and-stack`: backend + frontend + devops
2. Begin implementation execution for feature `001-auth` with backend/frontend traceability updates.
3. Define Tamagui design tokens and base component layer for React Native screens.
4. Begin phase-4 execution for `006-ui-screen-map` following `006-ui-screen-map-tasks.md`.
5. Implement auth and list domains first (`001`, `002`) to unlock MVP usage.
6. Implement collaboration and reset workflows (`003`, `004`) with integration tests.
7. Extend backend test suites with integration and contract coverage for new routes.
8. Expand Milestone D security evidence with endpoint-level checklist and evaluate distributed rate limiting for multi-instance deployments.
9. Keep this file updated with requirement-to-code-to-test traceability as implementation progresses.
