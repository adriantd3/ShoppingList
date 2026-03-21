---
name: implement-feature
description: "Use when: implementing a feature from specs/features with requirement-to-code traceability and test-first validation."
---

# Implement Feature

## When to use
Use this skill when a feature spec exists in `specs/features/` and you want disciplined implementation.

## Inputs
- `specs/project.md`
- `specs/conventions.md`
- `specs/current-state.md`
- `specs/features/<feature>.md`

## Workflow
1. Read the feature spec and list requirement IDs.
2. Convert acceptance criteria into executable test cases.
3. Implement minimal code to satisfy tests.
4. Validate with project test/build commands.
5. Update `specs/current-state.md` with coverage and status.

## Rules
- Do not implement undocumented behavior.
- Keep changes small and reviewable.
- Preserve traceability in commit messages and summaries.

## Output
- Requirement coverage table
- Changed files
- Validation evidence
- Remaining risks
