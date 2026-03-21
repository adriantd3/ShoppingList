---
applyTo: "frontend/**,backend/**"
description: "Security baseline for mobile frontend and backend implementation. Apply OWASP checks, secret handling, authz/authn controls, and dependency hygiene in every change."
---

# Security Implementation Baseline

## Scope
- Applies to all implementation work in `frontend/` and `backend/`.
- Use security-focused skills when relevant: `owasp-security`, `api-security-review`, `mobile-security-coder`.

## Mandatory Security Checks
- Validate input at trust boundaries and reject malformed data early.
- Enforce authentication and authorization explicitly on protected operations.
- Never hardcode secrets, tokens, or credentials in source files.
- Avoid sensitive data leakage in logs, errors, and API responses.
- Use secure defaults for transport and storage of sensitive data.
- Add dependency updates or notes when introducing packages with security impact.

## Frontend Mobile (React Native)
- Do not store access tokens in plaintext or insecure storage.
- Avoid exposing sensitive runtime values through debug logs.
- Validate deep link and navigation params before use.
- Minimize app permissions and document security rationale for any new permission.

## Backend (Python/FastAPI and services)
- Validate request models strictly and return safe error messages.
- Enforce least-privilege access to routes and business operations.
- Prevent common API risks: broken access control, excessive data exposure, injection.
- Apply rate limiting or abuse controls on sensitive endpoints when applicable.

## Delivery Gate
- For each security-relevant change, include a short "Security notes" section in the PR/task summary with:
  - Risks considered
  - Controls applied
  - Remaining risks (if any)
