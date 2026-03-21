# Feature 003 - Shared Realtime List

## Goal
Allow invited family members to edit the same shopping list in near real time with simple conflict behavior suitable for MVP.

## Requirements
- FR-shared-01: A user can invite another user to a list using a secure share link.
- FR-shared-02: A share link has expiration and can be revoked by a list member.
- FR-shared-03: Any invited member can add, edit, delete, and check/uncheck list items.
- FR-shared-04: Changes made by one member are visible to connected members in near real time.
- FR-shared-05: Concurrent edits follow last-write-wins behavior in MVP.
- FR-shared-06: List items are grouped by predefined supermarket-style categories.
- FR-shared-07: Inside each category, the system applies a simple deterministic order for MVP.
- FR-shared-08: List item quantity supports numeric value and unit selected from predefined units.
- FR-shared-09: The system supports offline read and check/uncheck updates and synchronizes them on reconnect.
- NFR-01: 95% of realtime update deliveries to connected clients should complete in <= 1000 ms under MVP expected load.
- NFR-02: The collaboration backend must be implementable with FastAPI + PostgreSQL and open source libraries.

## Acceptance Criteria
- When a list member generates a share link, the system shall create a tokenized link with expiration.
- When a non-member uses a valid, unexpired share link, the system shall grant access to the shared list.
- When a share link is revoked, the system shall deny further access attempts through that link.
- While two or more members edit the same list, when one member updates an item, the system shall broadcast the updated state to connected members.
- While concurrent writes happen on the same item, when updates race, the system shall persist the latest committed write.
- When a member adds an item, the system shall require category selection from predefined categories.
- When a member sets item quantity, the system shall require a numeric quantity and a predefined unit value.
- While a client is offline, when the user checks or unchecks an existing item, the app shall store the action locally and sync it after reconnect.

## Planned Tasks
- Define collaboration and sharing API contracts.
- Implement share token generation, expiration, and revocation.
- Implement WebSocket channel for list updates in FastAPI.
- Implement PostgreSQL LISTEN/NOTIFY based update fan-out.
- Implement category and predefined unit constraints in data model and API validation.
- Implement offline check/uncheck queue and reconnect synchronization in mobile app.
- Add integration tests for sharing, token expiration, and revocation.
- Add integration tests for realtime broadcast and concurrent edit behavior.
- Add mobile tests for offline queue and reconnect sync.

## Traceability
- Code: backend/python-api/collaboration/**, backend/python-api/lists/**, frontend/Dutylist/components/lists/**
- Tests: backend/python-api/tests/integration/collaboration/**, backend/python-api/tests/integration/lists/**, frontend/Dutylist/**/__tests__/collaboration/**
