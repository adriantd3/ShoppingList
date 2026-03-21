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

- [ ] 7. Implement lists and items REST contracts
  - Build CRUD routes for lists and items with strict validation.
  - Enforce category and predefined unit constraints.
  - Implement deterministic sort/index behavior for list items.
  - Requirement: FR-backend-03, FR-backend-08

- [ ] 8. Implement idempotency and offline replay support
  - Add `Idempotency-Key` middleware/dependency for mutating endpoints.
  - Persist operation fingerprints and replay windows.
  - Return deterministic responses for duplicate and conflicting replays.
  - Requirement: FR-backend-06

- [ ] 9. Implement sharing lifecycle contracts
  - Add share-link issue, consume, expire, revoke endpoints.
  - Store link tokens as hashes only.
  - Add audit metadata for creator, timestamps, and revoke actor.
  - Requirement: FR-backend-03, FR-backend-09

- [ ] 10. Implement reset and quick-restore backend semantics
  - Add transactional pre-reset snapshot creation.
  - Add reset command behavior according to MVP policy.
  - Add restore-latest endpoint constrained to latest restorable snapshot.
  - Requirement: FR-backend-07

- [ ] 11. Implement realtime event infrastructure
  - Add event builder service and envelope schema.
  - Persist events and publish notifications via PostgreSQL LISTEN/NOTIFY.
  - Implement WebSocket channel auth and list membership checks.
  - Requirement: FR-backend-04, FR-backend-05

- [ ] 12. Implement realtime list event emission
  - Emit canonical events for item create/update/delete/toggle.
  - Emit events for reset/restore and membership changes.
  - Ensure versioned payload compatibility.
  - Requirement: FR-backend-04, FR-backend-07

- [ ] 13. Implement profile and notifications endpoints
  - Add profile read/update endpoints.
  - Add notification preferences endpoints.
  - Add device push token registration endpoint.
  - Requirement: FR-backend-03

- [ ] 14. Add API security hardening controls
  - Add abuse controls/rate-limits on auth and share-link endpoints.
  - Add request size/body limits and strict content-type handling.
  - Add security headers and CORS policy by environment.
  - Requirement: FR-backend-05, FR-backend-10, NFR-02

- [ ] 15. Add contract test suite
  - Validate request/response schemas and error code contracts.
  - Validate WebSocket event envelope schema and type safety.
  - Requirement: FR-backend-12, NFR-03

- [ ] 16. Add integration test suite
  - Test auth and authorization paths, including forbidden access.
  - Test idempotency replay behavior and conflict responses.
  - Test share-link lifecycle, reset/restore semantics, and membership transitions.
  - Requirement: FR-backend-05, FR-backend-06, FR-backend-07, FR-backend-09, FR-backend-12

- [ ] 17. Add realtime integration tests
  - Verify multi-client fan-out behavior.
  - Verify ordering guarantees and eventual consistency under concurrent writes.
  - Requirement: FR-backend-04, FR-backend-12

- [ ] 18. Add security review checklist evidence
  - Run endpoint-level API security checklist across all routes.
  - Record applied controls and remaining accepted risks.
  - Add dependency hygiene review notes.
  - Requirement: FR-backend-10, NFR-02

- [ ] 19. Publish backend OpenAPI and WS contract docs
  - Export OpenAPI with examples and error codes.
  - Publish WebSocket event catalog with versioning policy.
  - Link contracts into feature traceability.
  - Requirement: FR-backend-03, FR-backend-04, NFR-03

- [ ] 20. Update traceability and current-state
  - Map implemented modules and tests to all backend requirements.
  - Update `specs/current-state.md` with coverage and execution status.
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
