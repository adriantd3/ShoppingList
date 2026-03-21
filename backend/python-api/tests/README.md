# Backend Test Layout

This project keeps tests outside `app/` and organizes them by test layer and module.

## Required structure

- `tests/conftest.py` shared fixtures.
- `tests/unit/<module>/` unit tests by module.
- `tests/integration/<module>/` integration tests by module.

## Rules

- Do not create `app/tests`.
- Do not place test files directly under `tests/unit` or `tests/integration` roots.
- Add new test files under a module folder (for example: `tests/unit/lists/`, `tests/integration/core/`).

## Automatic enforcement

- `tests/unit/core/test_layout_guard.py` fails if:
  - `app/tests` exists.
  - flat test files exist at `tests/unit/test_*.py` or `tests/integration/test_*.py`.
