POWERSHELL ?= powershell -NoProfile -ExecutionPolicy Bypass
PY_BACKEND_SCRIPT := scripts/python-api/backend.ps1

.PHONY: help py-backend-setup py-backend-run py-backend-test py-backend-lint py-backend-typecheck py-backend-check py-backend-migrate-up py-backend-migrate-revision py-backend-seed-dummy-user

help:
	@echo Available targets:
	@echo   py-backend-setup      Prepare Python backend environment
	@echo   py-backend-run        Run FastAPI app in reload mode
	@echo   py-backend-test       Run pytest suite
	@echo   py-backend-lint       Run ruff checks
	@echo   py-backend-typecheck  Run mypy checks
	@echo   py-backend-check      Run lint + typecheck + tests
	@echo   py-backend-migrate-up Upgrade database to latest revision
	@echo   py-backend-migrate-revision MSG="name"  Create alembic revision
	@echo   py-backend-seed-dummy-user  Create/update local dummy login user

py-backend-setup:
	$(POWERSHELL) -File $(PY_BACKEND_SCRIPT) -Action setup

py-backend-run:
	$(POWERSHELL) -File $(PY_BACKEND_SCRIPT) -Action run

py-backend-test:
	$(POWERSHELL) -File $(PY_BACKEND_SCRIPT) -Action test

py-backend-lint:
	$(POWERSHELL) -File $(PY_BACKEND_SCRIPT) -Action lint

py-backend-typecheck:
	$(POWERSHELL) -File $(PY_BACKEND_SCRIPT) -Action typecheck

py-backend-check:
	$(POWERSHELL) -File $(PY_BACKEND_SCRIPT) -Action check

py-backend-migrate-up:
	$(POWERSHELL) -File $(PY_BACKEND_SCRIPT) -Action migrate-up

py-backend-migrate-revision:
	$(POWERSHELL) -File $(PY_BACKEND_SCRIPT) -Action migrate-revision -Message "$(MSG)"

py-backend-seed-dummy-user:
	$(POWERSHELL) -File $(PY_BACKEND_SCRIPT) -Action seed-dummy-user
