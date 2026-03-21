# Feature 004 - Template and Reset Workflow

## Goal
Model the refrigerator-style shopping workflow: persistent base items, flexible changes during shopping, and quick reset for next cycle.

## Requirements
- FR-template-01: A user can define and maintain a base shopping template for recurring items.
- FR-template-02: A user can add temporary items to the active list without changing the base template.
- FR-template-03: A list member can reset a completed shopping list to prepare the next cycle.
- FR-template-04: Reset keeps template items as not-purchased and removes completion marks.
- FR-template-05: Reset action stores minimal history so recent state can be recovered if reset was accidental.
- FR-template-06: Any invited list member can execute reset in MVP.
- NFR-01: Reset operation should complete in <= 1500 ms for lists up to 300 items.

## Acceptance Criteria
- When a user marks items as recurring in template, the system shall include those items in the active list baseline.
- When a user adds a temporary item during shopping, the system shall append it to active list without forcing template update.
- When a list member triggers reset, the system shall set all purchased flags to not purchased for recurring items.
- When reset completes, the system shall keep list collaboration enabled and editable in real time.
- When reset is executed, the system shall store the pre-reset snapshot metadata for recovery within configured MVP retention.
- While another member is editing, when reset occurs, the system shall broadcast new list state to connected members.

## Planned Tasks
- Define data model for template items versus temporary items.
- Implement active list reset command and snapshot metadata storage.
- Implement API endpoint for reset and optional restore from latest snapshot.
- Implement mobile UI actions for template management and reset.
- Implement realtime propagation for reset events.
- Add integration tests for template inclusion and reset behavior.
- Add integration tests for reset snapshot and recovery flow.

## Traceability
- Code: backend/python-api/templates/**, backend/python-api/lists/reset/**, frontend/Dutylist/components/lists/**
- Tests: backend/python-api/tests/integration/templates/**, backend/python-api/tests/integration/reset/**, frontend/Dutylist/**/__tests__/reset/**
