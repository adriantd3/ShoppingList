---
applyTo: "specs/**,.github/docs/**"
description: "Documentation rules for requirements and specifications"
---

# Requirements and Specs Documentation

## Language and Style
- Use English by default.
- Prefer plain formatting.
- Keep documents short, concrete, and testable.

## Required Structure for Feature Specs
Each file in `specs/features/` should include:
1. Goal
2. Requirements (IDs)
3. Acceptance criteria
4. Planned tasks
5. Traceability (code/tests)

## Requirement Quality
- Use stable IDs (for example `FR-auth-01`, `NFR-01`).
- Write acceptance criteria in executable style (EARS where possible).
- Avoid ambiguous terms such as "fast" or "user-friendly" without measurable criteria.

## Consistency Rules
- `specs/project.md`: project-level scope and goals.
- `specs/conventions.md`: naming and process conventions.
- `specs/current-state.md`: progress and coverage status.
- `specs/features/*.md`: per-feature contract for implementation.

## Anti-Patterns
- Do not include implementation details in requirement statements unless required.
- Do not mark a feature done if tests/coverage mapping are missing.
- Do not leave acceptance criteria implicit.
