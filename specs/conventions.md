# SDD Conventions

## Language
- Use English as default for specs, prompts, and skills.
- Keep naming stable and explicit.

## Requirement Format
Use IDs per feature:
- `FR-<feature>-<nn>` for functional requirements.
- `NFR-<nn>` for non-functional requirements.

Example:
- `FR-auth-01`: User can sign in with email/password.

## Acceptance Criteria Style
Use EARS when practical:
- `When <trigger>, the system shall <response>.`
- `While <state>, when <trigger>, the system shall <response>.`

## Feature File Naming
- `specs/features/001-auth.md`
- `specs/features/002-dashboard.md`

## Traceability
Each feature spec must include:
- Related requirements IDs.
- Planned tasks.
- Code paths.
- Test paths.

## Test-First Task Policy
- Every implementation task in `specs/features/*-tasks.md` must include a test scope bullet.
- A task is not complete unless its linked tests are added/updated and passing.
- The minimum expectation per implemented behavior is:
	- at least one happy-path assertion,
	- at least one negative or error-path assertion,
	- explicit mapping from requirement ID to test file path.

## Test Quality Rules (Anti-Overfitting)
- Prefer behavior and user-visible outcomes over implementation details.
- Avoid assertions tied to private internals, call order noise, or brittle snapshots.
- Keep tests deterministic (fixed inputs, isolated state, controlled mocks).
- Use realistic fixtures that reflect production contracts.
- For bug fixes, add a regression test that fails before the fix and passes after it.

## Definition of Done
A feature is done when:
- Spec exists and is approved.
- Tasks are complete.
- Tests pass.
- Traceability links are updated in `specs/current-state.md`.
