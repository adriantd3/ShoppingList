# Feature 001 - Auth and Session

## Goal
Provide low-friction authentication for a family-oriented MVP using email/password and social login (Google/Apple), without provider lock-in.

## Requirements
- FR-auth-01: A user can register and sign in with email and password.
- FR-auth-02: A user can sign in with Google.
- FR-auth-03: A user can sign in with Apple.
- FR-auth-04: The system issues and validates JWT-based sessions for mobile clients.
- FR-auth-05: The system rejects invalid credentials with actionable error messages.
- FR-auth-06: The system allows explicit sign-out from active session.
- NFR-01: The auth module must be implementable with open source components in a FastAPI backend.
- NFR-02: 95% of successful sign-in requests should complete in <= 1500 ms under MVP expected load.

## Acceptance Criteria
- When a new user submits valid email/password data, the system shall create an account and return an authenticated session.
- When a user submits valid email/password credentials, the system shall authenticate and return an access token.
- When a user submits invalid credentials, the system shall deny access and return a clear error reason.
- When a user completes Google OAuth successfully, the system shall authenticate and return an access token.
- When a user completes Apple OAuth successfully, the system shall authenticate and return an access token.
- While a user holds a valid session token, when protected endpoints are requested, the system shall authorize the request.
- When a user signs out, the system shall invalidate or expire the active mobile session according to configured token policy.

## Planned Tasks
- Define auth domain model and token lifecycle in backend API contract.
- Implement email/password auth in FastAPI.
- Implement Google and Apple OAuth integration.
- Implement session validation middleware for protected routes.
- Implement React Native + Expo auth screens and token handling.
- Add backend integration tests for all auth flows.
- Add frontend integration tests for successful and failed sign-in states.

## Traceability
- Code: backend/python-api/auth/**, frontend/Dutylist/app/auth/**
- Tests: backend/python-api/tests/integration/auth/**, frontend/Dutylist/**/__tests__/auth/**
