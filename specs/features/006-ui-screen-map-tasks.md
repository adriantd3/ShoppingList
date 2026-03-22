# Feature 006 - Implementation Plan

## Execution Strategy
- Implement vertical slices in this order: app shell and routing, auth screens, lists flow, item interactions, sharing, profile, history, and cross-cutting quality gates.
- Keep each task small and releasable with tests before moving to the next task.
- Update this file as tasks progress.

## Tasks

- [ ] 1. Bootstrap new mobile app workspace
  - Create a new React Native + Expo project scaffold for MVP runtime.
  - Add initial folder structure for app routes, components, features, services, and tests.
  - Ensure legacy frontend is not part of MVP runtime.
  - Requirement: FR-platform-10, FR-platform-11, FR-ui-18

- [ ] 2. Install and configure core dependencies
  - Install Expo Router, Tamagui, React Query, secure storage, network status, and notification dependencies.
  - Lock dependency versions to stable compatible set with selected Expo SDK.
  - Add baseline scripts for lint, test, and typecheck.
  - Requirement: FR-platform-11, FR-ui-18

- [ ] 3. Implement root providers and route guards
  - Implement app root layout with providers for auth, query cache, connectivity, and theme.
  - Add first-launch guard for onboarding flow.
  - Add auth guard for protected routes.
  - Requirement: FR-ui-01, FR-ui-02, FR-ui-03, FR-ui-14

- [ ] 4. Implement onboarding flow with push permission
  - Build first-run onboarding screen sequence.
  - Request push permission in onboarding and store result.
  - Add fallback path when permission is denied.
  - Requirement: FR-ui-14, FR-ui-16, FR-ui-11

- [ ] 5. Implement authentication screens and navigation
  - Build login, register, forgot-password, and verify-email screens.
  - Wire navigation transitions between auth screens.
  - Connect auth actions to API contracts and session persistence.
  - Requirement: FR-ui-01, FR-ui-04

- [ ] 6. Implement tab shell and app entry routing
  - Build two-tab layout (Lists, Profile).
  - Implement post-auth redirection to last active list.
  - Fallback to lists collection if no active list exists.
  - Requirement: FR-ui-02, FR-ui-03

- [ ] 7. Implement Lists collection screen
  - Build lists overview with summary metadata cards.
  - Add create-list action and empty/loading/error/offline states.
  - Add entry point to history screen.
  - Requirement: FR-ui-05, FR-ui-12, FR-ui-13

- [ ] 8. Implement active list screen core interactions
  - Render categorized item groups.
  - Add explicit checkbox purchase toggle.
  - Add inline quick-add bar.
  - Implement pending queue badge and offline banner.
  - Requirement: FR-ui-06, FR-ui-08, FR-ui-13, NFR-01

- [ ] 9. Implement item editor modal
  - Build full edit modal with name, quantity, unit, category, and note.
  - Add validation and save/cancel behaviors.
  - Add optimistic update and rollback handling.
  - Requirement: FR-ui-06, FR-ui-07, FR-ui-13

- [ ] 10. Implement destructive confirmation patterns
  - Add confirmations for reset list, delete item, and delete list.
  - Keep sign-out action without destructive modal.
  - Add reusable danger dialog component.
  - Requirement: FR-ui-15

- [ ] 11. Implement sharing and members flows
  - Build members screen with membership details.
  - Build share screen with generate, copy, revoke link actions.
  - Display link expiration and action feedback states.
  - Requirement: FR-ui-09

- [ ] 12. Implement profile and about screens
  - Build profile screen with basic user data and sign-out action.
  - Build notifications settings screen entry and toggle controls.
  - Build about/version screen.
  - Requirement: FR-ui-10, FR-ui-11

- [ ] 13. Implement history and quick restore flows
  - Build closed-shopping history basic view.
  - Add quick restore action for last pre-reset snapshot.
  - Include empty/error/loading states.
  - Requirement: FR-ui-12, FR-ui-13

- [ ] 14. Implement Tamagui token and component baseline
  - Define clear, non-gradient token palette and typography scale.
  - Build reusable primitives used by all screens.
  - Apply consistent spacing and hierarchy rules.
  - Requirement: FR-ui-17, FR-ui-18, NFR-02

- [ ] 15. Implement accessibility baseline checks
  - Verify touch target sizes and readable typography across screens.
  - Ensure contrast policy in semantic tokens.
  - Add accessibility labels on critical controls.
  - Requirement: FR-ui-19

- [ ] 16. Implement offline queue service
  - Add persistent queue for item mutations (add/edit/delete/check/uncheck).
  - Replay queued actions on reconnect with retry policy.
  - Surface replay failures in per-screen error state.
  - Requirement: FR-ui-13

- [ ] 17. Add integration and UI test suite for navigation and flows
  - Add tests for routing guards and last-active-list entry.
  - Add tests for auth, lists, item interactions, sharing, profile, history.
  - Add tests for confirmation dialogs and offline queue behavior.
  - Requirement: FR-ui-01 through FR-ui-16, NFR-01

- [ ] 18. Add visual and accessibility smoke tests
  - Add checks for non-gradient visual policy and component consistency.
  - Add baseline accessibility smoke tests in critical paths.
  - Requirement: FR-ui-17, FR-ui-18, FR-ui-19, NFR-02

- [ ] 19. Update traceability and status
  - Link implemented paths and test paths back into feature spec traceability.
  - Update current-state with completion notes and coverage status.
  - Requirement: FR-ui-01 through FR-ui-19, NFR-01, NFR-02

## Milestone Checks
- Milestone A: Tasks 1 to 6 complete -> app boots with auth/onboarding/tabs routing.
- Milestone B: Tasks 7 to 13 complete -> full MVP screen flow available.
- Milestone C: Tasks 14 to 18 complete -> quality, accessibility, and resilience gates covered.
- Milestone D: Task 19 complete -> traceability and status up to date.
