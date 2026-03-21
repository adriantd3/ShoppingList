# Feature 007 - Backend Core Planning (MVP)

## Goal
Define the backend planning contract for FastAPI + PostgreSQL, including domain model boundaries, ER design targets, API and realtime contracts, and delivery order before implementation.

## Requirements
- FR-backend-01: The backend planning shall define a canonical domain model for users, lists, list items, memberships, share links, templates, reset snapshots, and realtime events.
- FR-backend-02: The backend planning shall produce an initial ER model that enforces ownership, membership, and referential integrity constraints.
- FR-backend-03: The backend planning shall define REST endpoint contracts for auth, lists, items, sharing, templates, history, and profile settings.
- FR-backend-04: The backend planning shall define WebSocket event contracts for realtime list synchronization.
- FR-backend-05: The backend planning shall define authorization rules per endpoint and per event channel.
- FR-backend-06: The backend planning shall define offline replay compatibility rules (idempotency keys, conflict behavior, replay response semantics).
- FR-backend-07: The backend planning shall define reset and quick-restore backend semantics aligned with MVP workflow.
- FR-backend-08: The backend planning shall define predefined categories and unit catalogs with extensibility rules.
- FR-backend-09: The backend planning shall define share-link lifecycle (issue, expire, revoke, consume) and audit metadata.
- FR-backend-10: The backend planning shall define error contract standards for frontend-safe handling.
- FR-backend-11: The backend planning shall define initial module boundaries for FastAPI project structure.
- FR-backend-12: The backend planning shall define minimum test strategy for contract, integration, and realtime behavior.
- NFR-01: The planning output shall keep architecture maintainable by one developer without over-engineering.
- NFR-02: The planning output shall avoid provider lock-in and rely on open source runtime services.
- NFR-03: The planning output shall preserve requirement-to-design-to-task traceability.

## Acceptance Criteria
- When backend planning is approved, the system shall provide an ER model that covers all MVP entities and relations required by features 001 to 006.
- When backend planning is approved, the system shall provide REST contract definitions for all MVP-critical user flows.
- When backend planning is approved, the system shall provide WebSocket event types and payload schemas for collaborative list editing.
- While offline replay is required, when queued actions are replayed, the backend contract shall define deterministic success/error behavior.
- When reset and quick-restore are invoked, the backend contract shall define snapshot creation, retention, and restore semantics.
- When share links are managed, the backend contract shall define expiration, revocation, and validation behavior.
- When frontend consumes backend errors, the backend contract shall provide stable machine-readable error codes.
- When the planning phase closes, the resulting design shall be sufficient to start implementation without endpoint-level ambiguity.

## Planned Tasks
- See implementation plan: `specs/features/007-backend-core-tasks.md`.

## Traceability
- Code: backend/python-api/**
- Tests: backend/python-api/tests/**
- Design Artifacts: specs/features/007-backend-core-design.md, specs/features/007-backend-core-tasks.md
