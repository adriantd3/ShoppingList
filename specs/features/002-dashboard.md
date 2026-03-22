# Feature 002 - Home and Active Lists

## Goal
Provide a practical post-login home screen where users can open the active shopping list quickly and manage list entry points without rigid flows.

## Requirements
- FR-dashboard-01: An authenticated user can view available shopping lists from the home screen.
- FR-dashboard-02: An authenticated user can open the active list in one action from the home screen.
- FR-dashboard-03: An authenticated user can create a new list from the home screen.
- FR-dashboard-04: An authenticated user can navigate to invite/share actions for a list from the home screen.
- FR-dashboard-05: The home screen shows enough status context to identify if a list is in-progress or reset-ready.
- NFR-01: 95% of home screen data loads should complete in <= 1200 ms under MVP expected load.

## Acceptance Criteria
- When an authenticated user opens the app, the system shall display the home screen with list summaries.
- When the user selects a list card, the system shall navigate to that list detail screen.
- When the user creates a new list, the system shall persist the list and show it in the home screen list.
- While lists exist for the user, when the home screen is refreshed, the system shall return current list state from backend.
- When a list has completed shopping state, the system shall show visual status that distinguishes it from actively edited lists.
- While measuring dashboard load performance under MVP baseline, when 100 successful list-summary requests are executed at 10 concurrent virtual users in warm-runtime conditions, the system shall keep p95 latency <= 1200 ms.

## Planned Tasks
- Define home/list-summary API contract.
- Implement backend endpoint(s) for list summaries and creation.
- Implement React Native + Expo home screen rendering and navigation.
- Implement list status indicator mapping in frontend.
- Add integration tests for list retrieval and creation.
- Add UI tests for navigation to list detail.

## Traceability
- Code: backend/python-api/app/modules/lists/**, frontend/mobile-app/app/(tabs)/lists/index.tsx
- Tests: backend/python-api/tests/integration/lists/**, frontend/mobile-app/tests/**/home/**
