# Feature 006 - Mobile UI Screen Map (MVP)

## Goal
Define the exact MVP mobile screens, navigation behavior, and interaction contracts before implementation, aligned with a family-first shopping workflow.

## Requirements
- FR-ui-01: When unauthenticated, the app entry shall route to authentication flow.
- FR-ui-02: When authenticated, the app entry shall route to the last active shopping list inside the Lists tab.
- FR-ui-03: Main authenticated navigation shall use two tabs only: Lists and Profile.
- FR-ui-04: Auth flow shall include Login, Register, Password Recovery, and Email Verification screens.
- FR-ui-05: Lists tab shall include list collection view with summary metadata (last update, members, purchased progress) and create-list action.
- FR-ui-06: Active list screen shall support inline quick-add and full edit modal for items.
- FR-ui-07: Full item edit modal shall include name, quantity, unit, category, and note.
- FR-ui-08: Item purchase toggle shall use explicit checkbox interaction.
- FR-ui-09: Sharing UX shall include Members screen and Share screen with link generation, copy, and revoke.
- FR-ui-10: Profile tab shall include user basic data, sign-out, notifications settings, and About/version screen.
- FR-ui-11: Notifications MVP shall support shared-list change push events only.
- FR-ui-12: History UX in MVP shall include quick restore of last pre-reset state and basic closed-shopping history view.
- FR-ui-13: UI state coverage shall include loading, per-screen error states, empty states, and offline banner with pending queue indicator.
- FR-ui-14: Onboarding shall be short and shown only on first app launch.
- FR-ui-15: Destructive confirmations shall be required for reset list, delete item, and delete list.
- FR-ui-16: Push permission request shall be asked during onboarding flow.
- FR-ui-17: Visual style shall be clear and clean, without gradient-based decorative styling.
- FR-ui-18: Mobile UI must use Tamagui components and tokens as primary building blocks.
- FR-ui-19: Accessibility baseline shall guarantee readable typography, sufficient color contrast, and touch target sizing for mobile comfort.
- NFR-01: Primary shopping actions (check item, add item, open edit) should be executable in <= 2 taps from active list screen.
- NFR-02: UI composition should avoid unnecessary visual complexity and preserve clear hierarchy for non-technical users.

## Acceptance Criteria
- When an authenticated user launches the app and a last active list exists, the system shall open that list directly.
- When an authenticated user launches the app and no active list exists, the system shall open Lists tab collection view.
- When unauthenticated user launches the app, the system shall open Login screen.
- When user opens auth flow, the system shall provide routes for register, password recovery, and email verification.
- While user is in active list, when adding a quick item, the system shall allow inline add without opening full modal.
- While user edits full item details, when save is confirmed, the system shall persist name, quantity, unit, category, and note.
- When user toggles purchased state, the system shall update item state through checkbox interaction.
- When user opens sharing from a list, the system shall provide members view and share-link management view.
- When user opens profile, the system shall provide access to basic account data, notifications settings, about/version, and sign-out.
- While app is offline, when pending changes exist, the system shall display offline banner and pending queue indicator.
- When user starts app for first time, the system shall display short onboarding and ask notification permission in that flow.
- When user executes reset list, delete item, or delete list, the system shall require explicit confirmation before applying action.
- When user opens any MVP screen, the system shall render with clean non-gradient visual language and Tamagui component primitives.

## Planned Tasks
- See implementation plan: `specs/features/006-ui-screen-map-tasks.md`.

## Traceability
- Code: frontend/mobile-app/app/**, frontend/mobile-app/components/**, frontend/mobile-app/features/**
- Tests: frontend/mobile-app/tests/ui/**, frontend/mobile-app/tests/integration/navigation/**
