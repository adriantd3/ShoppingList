---
name: requirements-elicitation
description: "Use when: you need structured requirement elicitation and feature spec drafting for Spec-Driven Development."
---

# Requirements Elicitation Skill

## When to use
Use this skill when you need to define feature requirements through guided Q&A before implementation.

## Inputs
- `specs/project.md`
- `specs/conventions.md`
- `specs/current-state.md`

## Process
1. Clarify feature goal and user value.
2. Identify actors and key use cases.
3. Define requirements and constraints.
4. Write measurable acceptance criteria.
5. Draft or update `specs/features/<id>-<name>.md`.

## Output contract
The resulting spec should include:
- Goal
- Requirement IDs
- Acceptance criteria
- Planned tasks
- Initial traceability placeholders

## Quality checks
- No ambiguous acceptance criteria.
- No hidden assumptions.
- No implementation work started before spec agreement.
