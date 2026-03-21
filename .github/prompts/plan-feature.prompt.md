---
name: plan-feature
description: "Plan a feature from specs with requirements, design notes, tasks, and test strategy"
parameters:
  - name: feature
    type: string
    required: true
    description: "Feature file name in specs/features (for example 001-auth.md)"
---

Create an implementation plan for feature `{{feature}}` using SDD.

Steps:
1. Read `specs/project.md`, `specs/conventions.md`, `specs/current-state.md`, and `specs/features/{{feature}}`.
2. Extract requirements and acceptance criteria.
3. Propose technical approach for this repository.
4. Produce task list with explicit code and test paths.
5. Define validation commands and done criteria.
6. Update `specs/current-state.md` proposal section (do not mark done yet).

Output format:
- Summary
- Requirements mapping
- Task list
- Test strategy
- Risks/assumptions
