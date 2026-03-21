# ShoppingList Python API

FastAPI backend foundation for ShoppingList MVP.

## Stack
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- JWT auth baseline

## Quick Start
1. Install dependencies:
	- `uv sync --all-groups`
2. Configure environment variables (example):
	- copy `.env.example` values into your shell/environment
3. Run API:
	- `uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`

## Validation
- Lint: `uv run ruff check .`
- Type check: `uv run mypy app tests`
- Tests: `uv run pytest`

## Database Migrations
- Upgrade: `uv run alembic upgrade head`
- New revision: `uv run alembic revision -m "your_message"`

## Security Baseline (Milestone A)
- Secrets are loaded from environment variables.
- JWT secret minimum length is enforced.
- Production config blocks unsafe toggles (`debug`, docs without explicit policy).
- Error responses follow a stable contract with `trace_id`.
