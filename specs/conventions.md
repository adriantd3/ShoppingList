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

## Definition of Done
A feature is done when:
- Spec exists and is approved.
- Tasks are complete.
- Tests pass.
- Traceability links are updated in `specs/current-state.md`.
