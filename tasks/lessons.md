# Lessons

## 2026-03-21 - Architecture and implementation defaults
- Prefer scalable solutions and eliminate duplicated logic (DRY).
- Enforce SOLID principles when defining module boundaries and responsibilities.
- Evaluate design-pattern fit before implementation and choose the simplest pattern that meets current and near-term needs.

## Operational rule
- Apply these defaults on every backend/frontend/spec change unless a requirement explicitly justifies a different tradeoff.

## 2026-03-21 - Local backend DX and manual verification
- For backend/API changes, do not stop at green tests; run the backend and perform at least one real manual login + protected endpoint check.
- Use root `/.env` as the single runtime source of truth for backend make/script flows; avoid parallel active env files.
- For seeded demo users, use email domains accepted by strict validators (for example `.dev` instead of `.local`).
- For Postman automation, prefer importing the native Postman collection over OpenAPI conversion when token scripts are required.
