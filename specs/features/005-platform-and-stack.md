# Feature 005 - Platform and Stack Baseline

## Goal
Define a brownfield-aware MVP technology baseline that replaces Java backend direction with FastAPI while preserving delivery speed and maintainability.

## Requirements
- FR-platform-01: MVP backend uses Python FastAPI as primary API and realtime service.
- FR-platform-02: MVP primary database is PostgreSQL.
- FR-platform-03: Realtime list updates use FastAPI WebSocket and PostgreSQL LISTEN/NOTIFY in initial architecture.
- FR-platform-04: Mobile frontend uses React Native with Expo.
- FR-platform-05: Existing Java backend code is legacy historical reference only, receives no further development, is not in MVP runtime path, and may be archived or removed.
- FR-platform-06: Authentication is implemented with open source components in FastAPI stack (FastAPI Users, JWT, OAuth providers).
- FR-platform-07: Architecture avoids hard dependency on a managed cloud provider for core functionality.
- FR-platform-08: Mobile UI components use Tamagui as the primary design system and component library.
- FR-platform-09: Legacy frontend (`frontend/Dutylist`) is not part of MVP runtime and may be removed or archived without affecting MVP delivery.
- FR-platform-10: MVP frontend is rebuilt from scratch in a new React Native + Expo codebase and does not reuse legacy frontend runtime code.
- FR-platform-11: MVP frontend dependencies must start on current stable versions at project bootstrap.
- FR-platform-12: MVP performance validation should use the simplest lightweight approach (local scripted runs) and remain non-blocking for CI until post-MVP hardening.
- FR-platform-13: MVP deployment topology is a single-instance monolith for backend runtime.
- NFR-01: Local developer environment shall be runnable with open source infrastructure services.
- NFR-02: Initial architecture should be understandable and maintainable by a single developer.

## Acceptance Criteria
- When MVP services are started, the system shall run with FastAPI backend, PostgreSQL database, and React Native + Expo client.
- When realtime list updates are triggered, the backend shall deliver updates through WebSocket without requiring external proprietary realtime services.
- When authentication providers are configured, the backend shall support email/password and OAuth login using open source server components.
- While Java backend modules exist in repository, when MVP deployment manifests are produced, the Java modules shall be excluded from active runtime services and from active development scope.
- When a new MVP mobile screen is implemented, the system shall compose UI with Tamagui components and theme tokens by default.
- When MVP frontend runtime is started, the system shall use only the new `frontend/mobile-app` codebase and not require `frontend/Dutylist` to run.
- When frontend bootstrap is executed for MVP, the system shall create a new clean app baseline and keep legacy frontend out of MVP runtime path.
- When dependency manifests are defined, the system shall pin current stable package versions compatible with selected Expo SDK.
- When onboarding a new developer, the project shall provide setup steps for local execution with open source dependencies.
- When MVP performance validation is executed, the system shall use lightweight local scripts with baseline thresholds and without a blocking CI gate.
- When MVP deployment is executed, the backend shall run as a single-instance monolith and multi-instance scaling concerns shall be deferred to post-MVP hardening.

## Planned Tasks
- Define architecture decision record for FastAPI/PostgreSQL/WebSocket baseline.
- Create backend service skeleton for FastAPI with modular domains.
- Define PostgreSQL schema baseline for users, lists, items, sharing, templates, and events.
- Define auth module with FastAPI Users + JWT + OAuth configuration.
- Define Tamagui theme tokens and base UI primitives for mobile app screens.
- Define archive/removal plan for `frontend/Dutylist` and keep it out of MVP runtime path.
- Define rebuild plan for `frontend/mobile-app` workspace structure and legacy deprecation status.
- Define dependency baseline policy and update cadence for Expo/Tamagui/react-navigation packages.
- Define local development compose environment for PostgreSQL and API dependencies.
- Define archive/removal plan for legacy Java modules and keep them out of MVP runtime and active development scope.
- Define lightweight performance check scripts and local execution steps for MVP baseline validation.
- Define deployment manifests/scripts aligned with single-instance monolith topology.
- Add smoke tests for service startup and core health checks.

## Traceability
- Code: backend/python-api/**, frontend/mobile-app/**, docs/architecture/**
- Tests: backend/python-api/tests/smoke/**, backend/python-api/tests/integration/health/**, frontend/mobile-app/tests/**
