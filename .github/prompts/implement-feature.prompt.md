---
name: implement-feature
description: "Implement a planned feature from specs and keep traceability updated"
parameters:
  - name: feature
    type: string
    required: true
    description: "Feature file name in specs/features (for example 001-auth.md)"
---

Implement feature `{{feature}}` following SDD rules.

Execution rules:
1. Read the feature spec and acceptance criteria first.
2. Implement incrementally with tests.
3. Keep explicit links from requirement IDs to code/tests.
4. Run project checks relevant to changed modules.
5. Update `specs/current-state.md` with status and traceability notes.

Required output:
- Files changed
- Tests executed
- Requirement coverage
- Open follow-ups
