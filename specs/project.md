# Project Specification

## Purpose
ShoppingList is a personal project to manage shopping lists, products, and user workflows.

## Project Reality (Brownfield)
This is not a greenfield project.

- The repository already contains a `frontend/` area and a `backend/` area.
- Future work may redefine product scope, but must account for existing code and structure.
- Specs should state whether a feature is a refactor, replacement, or new capability.

## Product Goals
- Capture shopping tasks quickly.
- Keep list and product state consistent across frontend and backend.
- Evolve features through executable specifications before implementation.
- Reuse robust UI libraries to reduce custom UI logic and accelerate delivery.

## Scope
In scope:
- Requirements capture and refinement.
- Feature-level specifications.
- Traceability from requirement -> spec -> task -> code -> tests.
- Brownfield-aware planning for `frontend/` and `backend/`.
- UI system decisions for React Native stack, including component-library standardization.

Out of scope (for now):
- Enterprise governance.
- Heavy process overhead.

## Success Criteria
- Every implemented feature has a spec file in `specs/features/`.
- Every feature has acceptance criteria and linked tests.
- Every implementation task has explicit test scope and passing evidence.
- Tests validate behavior (including negative paths), not just implementation internals.
- Agent guidance remains concise and actionable.
- Mobile UI is built primarily on a shared component system (Tamagui) instead of custom one-off components.
