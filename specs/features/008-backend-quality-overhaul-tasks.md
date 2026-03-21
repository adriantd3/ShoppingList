# Feature 008 - Implementation Plan

## Tasks
- [x] 1. Create feature requirements and design baseline
  - Add feature spec, technical design, and task breakdown for backend quality overhaul.
  - Include architecture diagrams for continuous development guidance.
  - Requirement: FR-backend-quality-07, NFR-quality-02

- [x] 2. Implement domain exception foundation and centralized mapping
  - Add domain exception taxonomy.
  - Add transport mapping strategy and message catalog integration.
  - Requirement: FR-backend-quality-01, FR-backend-quality-02, NFR-quality-01

- [x] 3. Refactor auth module to repository pattern
  - Add auth repository and remove direct SQL from service/dependency orchestration.
  - Requirement: FR-backend-quality-03

- [x] 4. Add tests for exception and auth repository refactor
  - Update auth unit/integration tests for new exception boundaries.
  - Requirement: FR-backend-quality-06, NFR-quality-02

- [x] 5. Refactor service signatures to explicit dependencies
  - Remove hidden request-context access in targeted services.
  - Progress: sharing, notifications/profile, and lists services/endpoints now pass explicit `db` and `principal`.
  - Requirement: FR-backend-quality-04

- [x] 6. Normalize transaction ownership and idempotency boundary
  - Remove mixed commit ownership and reduce route-level duplication.
  - Progress: list-route idempotency boundary consolidated through reusable helper in `app/api/rest/v1/endpoints/lists.py`; repository-level commits removed from lists/sharing/notifications/realtime modules and service-level transaction ownership enforced with explicit `db.begin()` boundaries.
  - Requirement: FR-backend-quality-05

- [x] 7. Redesign test architecture slices and coverage gaps
  - Improve fixtures and reduce monkeypatch-coupled contracts.
  - Progress: added shared unit transactional fixture, added notifications unit service coverage, and added behavior-first profile authz contract tests with reduced monkeypatch reliance.
  - Add missing negative-path and module coverage.
  - Requirement: FR-backend-quality-06, NFR-quality-02

- [x] 8. Update traceability and current state
  - Add requirement-to-code-to-test mappings and validation evidence.
  - Requirement: NFR-quality-02

## Validation Gate (per slice)
- `uv run ruff check .`
- `uv run mypy app tests`
- `uv run pytest -q`
- Manual smoke: login and one protected route
