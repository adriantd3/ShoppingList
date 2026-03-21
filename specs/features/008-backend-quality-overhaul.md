# Feature 008 - Backend Quality Overhaul

## Goal
Execute a backend architecture refactor that removes major anti-patterns, restores clean boundaries (SOLID), reduces duplication (DRY), and significantly improves test design quality for continuous development.

## Impact Scope
- Backend only (`backend/python-api`)
- Breaking changes allowed for internal contracts and error behavior
- No frontend changes in this feature

## Requirements
- FR-backend-quality-01: The backend shall enforce a transport-agnostic exception model where services and repositories do not raise HTTP transport exceptions directly.
- FR-backend-quality-02: The backend shall centralize error code/message mapping to remove repeated hardcoded error messages.
- FR-backend-quality-03: The auth module shall adopt the repository pattern and remove direct SQL execution from service/dependency orchestration code.
- FR-backend-quality-04: The backend shall remove hidden request-context dependencies from service signatures by making dependencies explicit.
- FR-backend-quality-05: The backend shall standardize transaction ownership for mutating flows.
- FR-backend-quality-06: The backend shall redesign test architecture to reduce monkeypatch-coupled contract tests and increase behavior-focused coverage.
- FR-backend-quality-07: The backend shall add architecture documentation artifacts (including Mermaid diagrams) to support ongoing development.
- NFR-quality-01: Refactor changes shall preserve or improve API security controls (authn, authz, validation, safe errors).
- NFR-quality-02: Requirement-to-code-to-test traceability shall be maintained in `specs/current-state.md`.

## Acceptance Criteria
- When a business rule fails in service logic, the system shall raise domain exceptions and map them to transport responses at API boundaries.
- When common error scenarios occur, the system shall resolve message text from a centralized catalog instead of repeated string literals across modules.
- When authentication queries are required, the auth module shall resolve them through an auth repository abstraction.
- While implementation continues, when each refactor slice is completed, the system shall update traceability entries linking requirements to code and tests.
- When the overhaul is completed, the system shall include architecture diagrams documenting layer boundaries, exception flow, transaction/idempotency flow, and test architecture.

## Planned Tasks
- See implementation plan: `specs/features/008-backend-quality-overhaul-tasks.md`.

## Traceability
- Code: `backend/python-api/app/**`
- Tests: `backend/python-api/tests/**`
- Design Artifacts:
  - `specs/features/008-backend-quality-overhaul-design.md`
  - `specs/features/008-backend-quality-overhaul-tasks.md`
