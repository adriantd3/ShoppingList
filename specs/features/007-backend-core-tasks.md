# Feature 007 - Implementation Plan

## Execution Strategy
- Execute backend in contract-first vertical slices to avoid frontend rework.
- Prioritize high-risk concerns first: authz, idempotency, realtime contract, reset safety.
- Gate every slice with security and integration checks before expanding scope.

## Tasks

- [x] 1. Create backend workspace skeleton
  - Create `backend/python-api` structure aligned with module boundaries in design.
  - Add FastAPI app bootstrap, config loading, and environment profiles.
  - Define baseline CI scripts: lint, typecheck, test.
  - Requirement: FR-backend-11, NFR-01, NFR-03

- [x] 2. Configure security and secrets baseline
  - Implement secret loading from environment only.
  - Add secure logging redaction for tokens, credentials, and PII.
  - Add transport/security defaults and production-safe configuration toggles.
  - Requirement: FR-backend-10, NFR-02

- [x] 3. Implement database foundation and migrations
  - Create SQLAlchemy models for all MVP entities.
  - Add Alembic migration baseline with foreign keys, uniqueness, and indexes.
  - Add integrity constraints for ownership and membership semantics.
  - Requirement: FR-backend-01, FR-backend-02, NFR-01

- [x] 4. Implement authentication core
  - Add email/password auth and JWT issue/verify flow.
  - Add OAuth identity linkage model and service contracts.
  - Implement auth middleware/dependencies for REST and WebSocket paths.
  - Requirement: FR-backend-03, FR-backend-05, FR-platform-06

- [x] 5. Implement authorization policy layer
  - Centralize permission checks for owner/member/non-member actions.
  - Enforce least privilege by endpoint and list resource.
  - Add deny-by-default behavior for non-members.
  - Requirement: FR-backend-05

- [x] 6. Implement error contract standardization
  - Add centralized exception mapping to machine-readable error codes.
  - Ensure safe messages in production responses.
  - Add trace_id correlation in all error responses.
  - Requirement: FR-backend-10

- [x] 7. Implement lists and items REST contracts
  - Build CRUD routes for lists and items with strict validation.
  - Enforce category and predefined unit constraints.
  - Implement deterministic sort/index behavior for list items.
  - Requirement: FR-backend-03, FR-backend-08

- [x] 8. Implement idempotency and offline replay support
  - Add `Idempotency-Key` middleware/dependency for mutating endpoints.
  - Persist operation fingerprints and replay windows.
  - Return deterministic responses for duplicate and conflicting replays.
  - Requirement: FR-backend-06

- [x] 9. Implement sharing lifecycle contracts
  - Add share-link issue, consume, expire, revoke endpoints.
  - Store link tokens as hashes only.
  - Add audit metadata for creator, timestamps, and revoke actor.
  - Requirement: FR-backend-03, FR-backend-09

- [x] 10. Implement reset and quick-restore backend semantics
  - Add transactional pre-reset snapshot creation.
  - Add reset command behavior according to MVP policy.
  - Add restore-latest endpoint constrained to latest restorable snapshot.
  - Requirement: FR-backend-07

- [x] 11. Implement realtime event infrastructure
  - Add event builder service and envelope schema.
  - Persist events and publish notifications via PostgreSQL LISTEN/NOTIFY.
  - Implement WebSocket channel auth and list membership checks.
  - Requirement: FR-backend-04, FR-backend-05

- [x] 12. Implement realtime list event emission
  - Emit canonical events for item create/update/delete/toggle.
  - Emit events for reset/restore and membership changes.
  - Ensure versioned payload compatibility.
  - Requirement: FR-backend-04, FR-backend-07

- [x] 13. Implement profile and notifications endpoints
  - Add profile read/update endpoints.
  - Add notification preferences endpoints.
  - Add device push token registration endpoint.
  - Requirement: FR-backend-03

- [x] 14. Add API security hardening controls
  - Add abuse controls/rate-limits on auth and share-link endpoints.
  - Add request size/body limits and strict content-type handling.
  - Add security headers and CORS policy by environment.
  - Requirement: FR-backend-05, FR-backend-10, NFR-02

- [x] 15. Add contract test suite
  - Scope: close contract drift risk for REST and WebSocket surfaces delivered in tasks 7 to 14.
  - Build endpoint contract matrix covering happy path + deterministic error paths for:
    - Auth (`/auth/login`).
    - Lists/items (`/lists`, `/lists/{list_id}`, `/lists/{list_id}/items/*`).
    - Sharing (`/lists/{list_id}/share-links`, `/share-links/consume`).
    - Profile/notifications (`/profile`, `/profile/notifications`, `/profile/push-tokens`).
  - Add JSON shape assertions for standardized error contract (`error.code`, `error.message`, `error.details`, `error.trace_id`) and stable machine-readable codes.
  - Add WebSocket envelope schema assertions (`event_id`, `event_type`, `list_id`, `occurred_at`, `actor_user_id`, `payload`, `version`) including invalid/unauthorized connection cases.
  - Ensure OpenAPI-operation alignment checks are covered for implemented routes to prevent undocumented response drift.
  - Deliverables:
    - Contract test modules under `backend/python-api/tests/integration/**` for all shipped MVP routes.
    - Reusable schema/assert helpers to keep test intent DRY and maintainable.
  - Done criteria:
    - Contract tests pass with no flaky timing assumptions.
    - New/updated tests demonstrate explicit mapping to FR-backend-03, FR-backend-04, FR-backend-10, FR-backend-12.
  - Requirement: FR-backend-12, NFR-03

- [x] 16. Add integration test suite
  - Scope: verify multi-step domain behavior and cross-module invariants under realistic API usage.
  - Add end-to-end integration scenarios for:
    - AuthN/AuthZ: owner/member/non-member access matrix including `403` invariants.
    - Idempotency: replay same payload and conflict on altered payload with same key.
    - Sharing: issue, consume, expire, revoke lifecycle and post-revocation behavior.
    - Reset/restore: snapshot creation before reset and restore-latest constraints.
    - Membership transitions: user joins through share-link then receives authorized access.
  - Add negative-path assertions for unauthorized list access, expired/revoked links, missing snapshots, and malformed payloads.
  - Validate persistence side effects using repository/state checks where API-only assertions are insufficient.
  - Deliverables:
    - Integration suites under `backend/python-api/tests/integration/lists/`, `backend/python-api/tests/integration/sharing/`, and `backend/python-api/tests/integration/core/`.
    - Shared fixture updates for deterministic setup/cleanup and role-based actors.
  - Done criteria:
    - Integration suites are deterministic and parallel-safe in local CI mode.
    - Coverage proves FR-backend-05, FR-backend-06, FR-backend-07, FR-backend-09, FR-backend-12 behaviors from public API surfaces.
  - Requirement: FR-backend-05, FR-backend-06, FR-backend-07, FR-backend-09, FR-backend-12

- [x] 17. Add realtime integration tests
  - Scope: validate realtime consistency guarantees for collaborative list editing.
  - Add multi-client websocket integration scenarios:
    - Multiple authorized clients subscribed to the same list receive canonical events.
    - Unauthorized/non-member websocket clients are rejected deterministically.
    - Membership-join transition followed by websocket subscribe succeeds.
  - Add ordering and eventual-consistency checks:
    - For sequential writes, receiving clients observe monotonic event order.
    - For concurrent writes, clients converge to database-committed final state and event envelopes remain schema-valid.
  - Add resilience checks for disconnect/reconnect and stale connection cleanup semantics.
  - Deliverables:
    - Realtime integration suite under `backend/python-api/tests/integration/core/`.
    - Reusable websocket test harness helpers for auth/connect/receive assertions.
  - Done criteria:
    - Realtime suites pass consistently with bounded waits/timeouts.
    - Evidence demonstrates FR-backend-04 and FR-backend-12 contract confidence for MVP single-instance runtime.
  - Requirement: FR-backend-04, FR-backend-12

- [x] 18. Add security review checklist evidence
  - Scope: produce auditable endpoint-level security evidence for all implemented MVP backend routes.
  - Execute API security checklist per route group (auth, lists/items, sharing, profile/notifications, websocket):
    - Authentication enforcement present.
    - Authorization checks aligned with membership/role policy.
    - Input validation and content-type constraints enforced.
    - Error responses avoid sensitive data leakage.
    - Rate-limit/abuse controls applied where required.
  - Capture dependency hygiene evidence:
    - Run dependency vulnerability scan and record findings + disposition.
    - Confirm no hardcoded secrets and environment-only secret sources.
  - Record accepted residual risks with mitigation path and owner:
    - Process-local rate limiting in multi-instance topology.
    - Cross-process realtime fan-out hardening beyond MVP scope.
  - Deliverables:
    - Security evidence section appended to `specs/current-state.md`.
    - Endpoint checklist artifact under `docs/` (or linked section in specs if docs path is not used).
  - Done criteria:
    - Each public route/event channel has explicit pass/fail checklist evidence.
    - Residual risks are documented with rationale and follow-up direction.
  - Requirement: FR-backend-10, NFR-02

- [x] 19. Publish backend OpenAPI and WS contract docs
  - Scope: publish implementation-aligned contracts as single source for frontend/backoffice integrations.
  - Generate and persist backend OpenAPI snapshot from runtime app state.
  - Ensure OpenAPI includes:
    - Endpoint paths and auth requirements.
    - Request/response examples for key routes.
    - Standard error code examples and schema references.
  - Publish WebSocket contract catalog including:
    - Event type table with payload fields.
    - Event envelope version policy and compatibility notes.
    - Auth/connect requirements and expected rejection codes.
  - Link published contract artifacts from feature 007 specs and current-state traceability sections.
  - Deliverables:
    - Updated/published files under `backend/openapi/` and/or `backend/python-api/README.md` contract section.
    - WebSocket catalog document under `docs/` or `specs/features/`.
  - Done criteria:
    - Published contract artifacts match tested behavior from tasks 15 to 17.
    - Consumers can integrate without reading implementation source code.
  - Requirement: FR-backend-03, FR-backend-04, NFR-03

- [x] 20. Update traceability and current-state
  - Scope: finalize milestone closure with full requirement-to-code-to-test evidence.
  - Update feature traceability with explicit mapping for FR-backend-01 through FR-backend-12 and NFR-01 through NFR-03.
  - Add Milestone D validation evidence block (lint, typing, full test suite, and contract/realtime suites if split commands are used).
  - Reconcile implementation plan task checklist statuses and milestone completion notes.
  - Add concise post-mortem notes:
    - What changed in architecture confidence.
    - Remaining known gaps intentionally deferred.
  - Deliverables:
    - `specs/current-state.md` updated with Milestone D completion and traceability rollup.
    - `specs/features/007-backend-core-tasks.md` task statuses synced with execution reality.
  - Done criteria:
    - No requirement remains without code/test traceability reference.
    - Current-state snapshot is sufficient for next feature planning without ambiguity.
  - Requirement: FR-backend-01 through FR-backend-12, NFR-01 through NFR-03

## Milestone Checks
- Milestone A: Tasks 1 to 6 complete -> secure backend foundation and stable error/auth policy.
- Milestone B: Tasks 7 to 10 complete -> core list/share/reset contracts available.
- Milestone C: Tasks 11 to 14 complete -> realtime and security hardening complete.
- Milestone D: Tasks 15 to 20 complete -> tests, docs, and traceability complete.

## Security Notes
- Risks considered:
  - Broken access control on list resources.
  - Replay inconsistencies for offline queued mutations.
  - Share-link leakage and unauthorized consumption.
  - Sensitive data exposure in logs/errors.
- Controls applied in plan:
  - Centralized authorization policy and deny-by-default checks.
  - Idempotency key contract with conflict handling.
  - Hashed share-link tokens with expiration and revocation lifecycle.
  - Standardized safe error contract and log redaction baseline.
- Remaining risks (to validate during implementation):
  - Performance impact of idempotency storage under burst replay.
  - Event ordering edge cases during high concurrency.

## Milestone A Execution Notes (2026-03-21)
- Validation evidence:
  - `uv run ruff check .` -> pass
  - `uv run mypy app tests` -> pass
  - `uv run pytest` -> pass (5 passed, 1 deprecation warning from Starlette constant)
- Requirement-to-code-to-test traceability:
  - FR-backend-11, NFR-01, NFR-03 -> `backend/python-api/app/main.py`, `backend/python-api/pyproject.toml` -> `backend/python-api/tests/test_health.py`
  - FR-backend-10, NFR-02 -> `backend/python-api/app/core/config.py`, `backend/python-api/app/core/logging.py`, `backend/python-api/app/core/errors.py` -> `backend/python-api/tests/test_error_contract.py`
  - FR-backend-01, FR-backend-02 -> `backend/python-api/app/db/models.py`, `backend/python-api/migrations/versions/20260321_0001_backend_core_baseline.py` -> foundation validated by app import/type checks
  - FR-backend-03, FR-backend-05 -> `backend/python-api/app/modules/auth/*`, `backend/python-api/app/modules/lists/policies.py`, `backend/python-api/app/api/ws/auth.py` -> `backend/python-api/tests/test_security.py`, `backend/python-api/tests/test_error_contract.py`

### Security notes - Block 1 (Task 1: skeleton)
- Risks considered: weak baseline structure causing ad-hoc auth/error handling and drift from contracts.
- Controls applied: module boundaries aligned to design; mandatory validation commands wired in project config.
- Residual risks: websocket and realtime modules are scaffolds only; behavior-level controls are pending later milestones.

### Security notes - Block 2 (Task 2: security/secrets baseline)
- Risks considered: hardcoded secrets, sensitive log leakage, unsafe prod toggles.
- Controls applied: `Settings` loads from environment, JWT minimum length enforced, production guards (`debug/docs/cors`) enforced, sensitive log redaction filter added.
- Residual risks: no KMS/secret rotation yet; secure secret distribution remains deployment responsibility.

### Security notes - Block 3 (Task 3: DB foundation)
- Risks considered: broken referential integrity, ownership bypass through orphan records, migration drift.
- Controls applied: normalized SQLAlchemy models with FK/unique constraints; Alembic baseline migration created with deterministic naming conventions.
- Residual risks: owner-membership invariant is not yet enforced by trigger/check constraint and will be addressed in domain operations.

### Security notes - Block 4 (Task 4: auth core)
- Risks considered: credential brute-force abuse, token forgery, invalid token reuse.
- Controls applied: secure password hashing (PBKDF2), JWT signed tokens with exp/iat/jti required claims, strict token decode errors, REST+WebSocket auth helpers.
- Residual risks: rate limiting and refresh-token rotation are pending Milestone C hardening tasks.

### Security notes - Block 5 (Task 5: authorization)
- Risks considered: broken access control / IDOR on list resources.
- Controls applied: centralized list policy functions (`require_list_membership`, `require_list_owner`) with deny-by-default behavior.
- Residual risks: policy is currently role-string based; richer permission matrix enforcement per action is pending in feature endpoints.

### Security notes - Block 6 (Task 6: error contract)
- Risks considered: internal info leakage, inconsistent frontend handling, missing traceability for incidents.
- Controls applied: centralized `ApiError` mapping with stable machine-readable codes, safe production message policy, `trace_id` in headers and body.
- Residual risks: centralized audit/event logging for incident pipelines is pending.

## Milestone B Progress Notes (2026-03-21)
- Task 7 executed (lists/items REST contracts):
  - Added list and item endpoints under `app/api/rest/v1/endpoints/lists.py`.
  - Added strict request/response schemas and predefined category/unit validation.
  - Added list/item service and repository methods with deterministic list item ordering (`sort_index`, `updated_at`, `id`).
  - Added contract tests for list creation and list-item validation behavior.
  - Validation evidence:
    - `uv run ruff check .` -> pass
    - `uv run mypy app tests` -> pass
    - `uv run pytest` -> pass (8 passed)

- Task 8 executed (idempotency and offline replay):
  - Added `Idempotency-Key` handling for mutating list/item endpoints with optional header semantics.
  - Added persistent idempotency records with payload fingerprint, stored response, and replay TTL window.
  - Added deterministic replay behavior:
    - same key + same payload -> replay stored response
    - same key + different payload -> `409 IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_PAYLOAD`
  - Added unit and integration tests covering replay and conflict behavior.
  - Validation evidence:
    - `uv run ruff check .` -> pass
    - `uv run mypy app tests` -> pass
    - `uv run pytest` -> pass (21 passed, 3 warnings)

- Task 9 executed (sharing lifecycle contracts):
  - Added share-link issue, consume, revoke, and expire endpoints.
  - Implemented share-link service/repository flow with membership checks and lifecycle validation.
  - Persisted share-link audit metadata for revocation actor and timestamps.
  - Enforced token-hash-only persistence and deterministic error responses for revoked/expired links.
  - Added unit and integration tests for sharing contracts and token hashing behavior.
  - Validation evidence:
    - `uv run ruff check .` -> pass
    - `uv run mypy app tests` -> pass
    - `uv run pytest` -> pass (28 passed, 3 warnings)

- Task 10 executed (reset and quick-restore semantics):
  - Added reset endpoint contract with transactional pre-reset snapshot creation.
  - Implemented reset behavior using MVP policy (`keep-and-uncheck` items).
  - Added restore-latest endpoint constrained to latest `pre_reset` snapshot.
  - Added list snapshot repository operations and reset/restore service orchestration.
  - Added unit and integration tests for reset/restore contract and service behavior.
  - Validation evidence:
    - `uv run ruff check .` -> pass
    - `uv run mypy app tests` -> pass
    - `uv run pytest` -> pass (33 passed, 3 warnings)

### Security notes - Block 7 (Task 7: lists/items contracts)
- Risks considered: broken access control, malformed input leading to inconsistent state, error response leakage.
- Controls applied: authenticated route dependencies, strict schema validation with forbidden unknown fields, deterministic item ordering, safe validation error serialization.
- Residual risks: endpoint-level rate limiting and payload size throttling remain scheduled for Milestone C hardening.

### Security notes - Block 8 (Task 8: idempotency)
- Risks considered: duplicate offline replays causing repeated mutations, key reuse ambiguity across payloads, and unbounded replay storage growth.
- Controls applied: request-scoped idempotency key handling on mutating list/item endpoints, SHA-256 payload fingerprinting, deterministic conflict response (`409` + stable error code), persistent response replay with configurable TTL.
- Residual risks: concurrent first-write races can still execute duplicate side effects under high contention and will require additional locking/rate controls in future hardening milestones.

### Security notes - Block 9 (Task 9: sharing lifecycle)
- Risks considered: unauthorized list joining through leaked links, replay of revoked links, and accidental plaintext token persistence.
- Controls applied: authenticated consume flow, membership checks for issue/revoke/expire operations, token hashing before persistence, explicit revoked/expired conflict handling with stable error codes, and revoke-actor audit metadata.
- Residual risks: no rate-limiting yet on share-link operations; abuse controls remain in Milestone C hardening.

### Security notes - Block 10 (Task 10: reset/restore)
- Risks considered: accidental destructive reset, inconsistent restore source selection, and unauthorized reset actions.
- Controls applied: list-membership authorization checks, transactional pre-reset snapshot persistence before mutation, restore constrained to latest `pre_reset` snapshot, and deterministic 404 when no restorable snapshot exists.
- Residual risks: snapshot retention policy cleanup is not yet automated and requires future lifecycle hardening.

## Milestone C Progress Notes (2026-03-21)
- Task 11 executed (realtime event infrastructure):
  - Added canonical realtime envelope schema and event persistence/publish service.
  - Added PostgreSQL `NOTIFY` publish bridge and in-process websocket connection manager.
  - Added websocket list channel route with bearer-token auth and list-membership authorization checks.
  - Added unit/integration tests for realtime service and websocket access contract behavior.

- Task 12 executed (realtime list event emission):
  - Added canonical list event type catalog for item lifecycle, reset/restore, and membership change events.
  - Emitted realtime events on item create/update/delete and purchased toggle semantics.
  - Emitted realtime events for reset/restore flows and share-link membership join transitions.
  - Added/updated unit tests covering event emission behavior and event type selection.

- Task 13 executed (profile/notifications endpoints):
  - Added `/profile` read/update endpoints.
  - Added `/profile/notifications` read/update endpoints.
  - Added `/profile/push-tokens` registration endpoint.
  - Added notification/profile repository and service layer plus contract tests.

- Task 14 executed (API security hardening):
  - Added scoped in-memory rate limiting controls for auth and share-link endpoints.
  - Added request body size guard and strict JSON content-type enforcement for payload-bearing mutating requests.
  - Added baseline security response headers and environment-aware CORS behavior.
  - Added integration tests for hardening controls (headers, content-type, size limits, rate limiting).

- Validation evidence:
  - `uv run ruff check .` -> pass
  - `uv run mypy app tests` -> pass
  - `uv run pytest -q` -> pass (52 passed, 3 warnings)

### Security notes - Block 11 (Task 11: realtime infrastructure)
- Risks considered: unauthorized websocket channel access, event spoofing from unauthenticated clients, and missing realtime audit trail.
- Controls applied: websocket bearer token validation, membership authorization checks before channel acceptance, persisted realtime event records, and publish bridge through PostgreSQL notifications.
- Residual risks: cross-process websocket fan-out from `LISTEN` subscribers is not yet implemented and remains part of future realtime integration hardening.

### Security notes - Block 12 (Task 12: realtime emission)
- Risks considered: inconsistent event semantics across list operations and missing membership transition notifications.
- Controls applied: centralized canonical event type constants, deterministic emission for create/update/delete/toggle/reset/restore/member-joined operations, and test coverage for event selection.
- Residual risks: ordering guarantees under concurrent multi-node writes are still pending dedicated realtime integration tests (Task 17).

### Security notes - Block 13 (Task 13: profile/notifications)
- Risks considered: unauthorized profile mutation and unvalidated push token registration payloads.
- Controls applied: authenticated endpoint dependencies, strict request models for profile/preferences/token registration, and service-layer user resolution with safe auth error semantics.
- Residual risks: push-token lifecycle cleanup and anti-abuse token registration controls are not yet automated.

### Security notes - Block 14 (Task 14: API hardening)
- Risks considered: auth/share-link brute-force abuse, oversized payload abuse, and insecure default API response headers.
- Controls applied: endpoint-scoped rate limiting, max request-size guard, strict content-type checks for mutating payloads, baseline defensive security headers, and environment-aware CORS defaults.
- Residual risks: in-memory rate limiting is process-local for MVP and should be replaced by distributed throttling for multi-instance deployments.

## Milestone D Progress Notes (2026-03-21)
- Task 15 executed (contract suite expansion):
  - Added auth contract coverage for login success and deterministic invalid-credentials error contract.
  - Added websocket envelope contract checks for required fields and schema shape under fan-out scenarios.
  - Verified stable error envelope keys (`code`, `message`, `details`, `trace_id`) on authentication failures.

- Task 16 executed (integration suite completion):
  - Consolidated integration coverage across core/lists/sharing/profile modules with negative-path checks.
  - Preserved deterministic idempotency, share-link lifecycle, and reset/restore contract validations.
  - Confirmed integration suite remains deterministic in local CI mode.

- Task 17 executed (realtime integrations):
  - Added multi-client websocket fan-out integration test validating identical envelope delivery.
  - Added ordered sequential event assertions for monotonic delivery semantics.
  - Added membership transition scenario (non-member rejected, then accepted after role update).

- Task 18 executed (security evidence):
  - Added endpoint-level security checklist artifact with pass/partial findings and residual risk register.
  - Captured dependency hygiene evidence with `uv pip check`.

- Task 19 executed (contract publication):
  - Published FastAPI OpenAPI snapshot to `backend/openapi/python-api.openapi.json`.
  - Published websocket event catalog to `backend/openapi/python-api-ws-events.md`.
  - Linked published artifacts in `backend/python-api/README.md`.

- Task 20 executed (traceability/state sync):
  - Updated `specs/current-state.md` with Milestone D execution status, traceability mapping, and validation evidence.

- Validation evidence:
  - `.venv/Scripts/python.exe -m ruff check .` -> pass
  - `.venv/Scripts/python.exe -m mypy app tests` -> pass
  - `.venv/Scripts/python.exe -m pytest -q` -> pass (57 passed, 3 warnings)
  - `uv pip check` -> pass (dependency metadata consistency check)

### Security notes - Block 15-20 (Milestone D closure)
- Risks considered: undocumented contract drift, incomplete realtime confidence, and missing release security evidence.
- Controls applied: contract test expansion, websocket integration fan-out/order validation, published OpenAPI+WS artifacts, and endpoint-level security checklist with residual risk register.
- Residual risks: distributed rate limiting and cross-process websocket fan-out remain out of MVP single-instance scope.
