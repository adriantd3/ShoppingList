# Feature 004 - Template and Reset Workflow

## Goal
Model the refrigerator-style shopping workflow: persistent base items, flexible changes during shopping, and quick reset for next cycle.

## Requirements
- FR-template-01: A user can define and maintain a base shopping template for recurring items.
- FR-template-02: A user can add temporary items to the active list without changing the base template.
- FR-template-03: A list member can reset a completed shopping list to prepare the next cycle.
- FR-template-04: Reset keeps template items as not-purchased and removes completion marks.
- FR-template-05: Reset action stores only the latest pre-reset snapshot per list and expires it after 30 days.
- FR-template-06: Any invited list member can execute reset in MVP.
- NFR-01: Reset operation should complete in <= 1500 ms for lists up to 300 items.

## Acceptance Criteria
- When a user marks items as recurring in template, the system shall include those items in the active list baseline.
- When a user adds a temporary item during shopping, the system shall append it to active list without forcing template update.
- When a list member triggers reset, the system shall set all purchased flags to not purchased for recurring items.
- When reset completes, the system shall keep list collaboration enabled and editable in real time.
- When reset is executed, the system shall replace any prior pre-reset snapshot with the latest one and keep it recoverable for 30 days.
- While another member is editing, when reset occurs, the system shall broadcast new list state to connected members.
- While measuring reset performance under MVP baseline, when 100 reset requests are executed at 10 concurrent virtual users in warm-runtime conditions for lists up to 300 items, the system shall keep p95 latency <= 1500 ms.

## Planned Tasks
- Define data model for template items versus temporary items.
- Implement active list reset command and snapshot metadata storage.
- Implement API endpoint for reset and optional restore from latest snapshot.
- Implement mobile UI actions for template management and reset.
- Implement realtime propagation for reset events.
- Add integration tests for template inclusion and reset behavior.
- Add integration tests for reset snapshot and recovery flow.

## Traceability
- Code: backend/python-api/app/modules/lists/**, backend/python-api/app/modules/realtime/**, frontend/mobile-app/features/lists/**
- Tests: backend/python-api/tests/integration/lists/test_reset_restore_contract.py, frontend/mobile-app/tests/**/reset/**
