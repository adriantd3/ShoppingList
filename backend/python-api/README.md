# ShoppingList Python API

FastAPI backend foundation for ShoppingList MVP.

## Stack
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- JWT auth baseline

## Quick Start
1. Prepare environment:
	- `make py-backend-setup`
2. Run API:
	- `make py-backend-run`
3. Run quality checks:
	- `make py-backend-check`

## Environment Configuration
- Runtime source of truth for backend make targets is repository root `.env`.
- Keep `backend/python-api/.env.example` as template/reference only.
- Avoid maintaining a second active `backend/python-api/.env` with different values to prevent configuration drift.

### Root Automation (Makefile)
- `make py-backend-setup`
- `make py-backend-run`
- `make py-backend-test`
- `make py-backend-lint`
- `make py-backend-typecheck`
- `make py-backend-check`
- `make py-backend-migrate-up`
- `make py-backend-migrate-revision MSG="your_message"`
- `make py-backend-seed-dummy-user`

## Validation
- Lint: `make py-backend-lint`
- Type check: `make py-backend-typecheck`
- Tests: `make py-backend-test`

## Database Migrations
- Upgrade: `make py-backend-migrate-up`
- New revision: `make py-backend-migrate-revision MSG="your_message"`

## Local Dummy Login User
- Seed (idempotent): `make py-backend-seed-dummy-user`
- This command applies migrations and then creates/updates a local test user.
- Default credentials:
	- email: `demo@shoppinglist.dev`
	- password: `DemoPass123!`

## Published Contracts (Milestone D)
- OpenAPI snapshot: `backend/openapi/python-api.openapi.json`
- WebSocket event catalog: `backend/openapi/python-api-ws-events.md`

## Manual Testing with Postman
1. Start backend locally:
	- `make py-backend-run`
2. Import native Postman collection (recommended):
	- `backend/openapi/python-api.postman_collection.json`
3. Run `Auth / Login` first.
	- The collection test script stores `access_token` into collection variable `jwt_token`.
4. Call protected endpoints (for example `Lists / Get Lists`).
	- A collection-level pre-request script injects `Authorization: Bearer {{jwt_token}}` automatically.

Fallback:
- If you import from OpenAPI (`backend/openapi/python-api.openapi.json`) instead, Postman may ignore vendor extensions depending on importer version and mode.

## Security Baseline (Milestone A)
- Secrets are loaded from environment variables.
- JWT secret minimum length is enforced.
- Production config blocks unsafe toggles (`debug`, docs without explicit policy).
- Error responses follow a stable contract with `trace_id`.
