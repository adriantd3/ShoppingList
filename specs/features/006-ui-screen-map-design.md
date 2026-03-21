# Feature 006 - Technical Design

## Scope
Technical design for MVP mobile UI implementation based on the approved screen-map requirements in `006-ui-screen-map.md`.

## Architecture Overview
The mobile app will be a new React Native + Expo codebase, Tamagui-first, with Expo Router for route orchestration and a state model optimized for realtime collaboration and offline actions.

### Runtime Architecture
- App shell: Expo Router + root providers
- UI layer: Tamagui components and project tokens
- Feature layer: auth, lists, list-detail, sharing, profile, onboarding
- Data layer: API client + React Query cache + offline queue persistence
- Integration layer: push notifications, connectivity, secure auth storage

### Route Architecture (Expo Router)
```text
app/
  _layout.tsx                       # providers + auth gate
  onboarding/
    index.tsx                       # first-run onboarding + push permission ask
  (auth)/
    _layout.tsx
    login.tsx
    register.tsx
    forgot-password.tsx
    verify-email.tsx
  (tabs)/
    _layout.tsx                     # two tabs only: lists, profile
    lists/
      index.tsx                     # collection view + create action
      [listId].tsx                  # active list detail
      members.tsx                   # members management view
      share.tsx                     # share link generate/copy/revoke
      history.tsx                   # closed-shopping history (basic)
    profile/
      index.tsx                     # basic user data + sign out + notifications
      about.tsx                     # app version and about
  modal/
    item-editor.tsx                 # full item edit modal
    confirm-action.tsx              # destructive action confirmation modal
```

## Navigation and Guard Strategy
- Root gate checks three conditions in order:
  - first launch -> onboarding flow
  - unauthenticated -> auth flow
  - authenticated -> lists flow
- Post-auth routing:
  - if last active list exists -> open `/(tabs)/lists/[listId]`
  - else -> open `/(tabs)/lists`
- Tabs are fixed to `Lists` and `Profile`; all other screens are pushed in stack from those contexts.

## State Model

### Global State Boundaries
- Auth session state: token lifecycle and identity metadata
- App preferences state: first-launch flag, notification preference toggles
- Connectivity state: online/offline and queue status

### Server State (React Query)
- Lists collection summaries
- Active list details (items grouped by category)
- Members and share-link status
- Closed-history summaries and details

### Offline Queue Model
- Queue type: append-only local operation queue
- MVP queued operations:
  - check item
  - uncheck item
  - quick item add
- Queue behavior:
  - enqueue while offline
  - optimistic UI update immediately
  - replay on reconnect in FIFO order
  - surface replay errors in per-screen error state

## Screen-Level Design Contracts

### Lists Collection Screen
- Inputs: list summaries + active list pointer
- Primary actions: create list, open list
- Secondary actions: open history
- Required states: loading, empty (no lists), error, offline banner

### Active List Screen
- Inputs: categorized list items, member count, progress summary
- Primary actions: checkbox toggle, inline add, open item editor
- Secondary actions: open members, open share, reset list, delete item
- Required states: loading, empty (no items), error, offline banner + queue count

### Item Editor Modal
- Fields: name, quantity, unit, category, note
- Validation:
  - name required
  - quantity numeric and positive
  - unit from predefined unit set
  - category from predefined category set
- Save behavior: optimistic update with rollback on hard failure

### Share and Members Screens
- Members screen:
  - show current members and membership metadata
- Share screen:
  - generate share link
  - copy link
  - revoke link
  - show expiration metadata

### Profile and About Screens
- Profile:
  - basic user data
  - notification toggle page entry
  - sign-out action
- About:
  - app version
  - build and environment metadata

### History Screen
- Closed-shopping list history with basic summaries
- Quick restore entry for last pre-reset snapshot
- No advanced filters/search in MVP

## Tamagui Design System Strategy

### Design Direction
- Clear and clean visual language
- No gradient-heavy decorative surfaces
- Mobile-first spacing rhythm and large touch affordances
- Emphasis on clarity for non-technical family users

### Token Layers
- Semantic colors:
  - background, surface, primary, success, warning, danger, muted-text
- Typography scale:
  - title, heading, body, caption
- Spacing scale:
  - xs, sm, md, lg, xl
- Radius scale:
  - small, medium, large

### Component Baseline
- `ScreenContainer`
- `SectionHeader`
- `ListSummaryCard`
- `CategoryBlock`
- `ItemRow` (with checkbox)
- `InlineAddBar`
- `OfflineBanner`
- `EmptyStatePanel`
- `ErrorStatePanel`
- `PrimaryActionButton`
- `DangerConfirmDialog`

## Accessibility Baseline
- Contrast and color usage aligned with readable foreground/background combinations
- Minimum comfortable touch target for actionable controls
- Readable text hierarchy with consistent typography scale
- Screen reader labels required on:
  - checkbox controls
  - destructive actions
  - navigation-critical buttons

## Push Permission UX
- Permission is requested during onboarding after context explanation screen
- If denied:
  - continue onboarding and app usage without blocking
  - expose re-enable path in Profile > Notifications

## Error and Confirmation Patterns
- Per-screen error panels with retry action
- Non-blocking inline errors for local validation
- Confirmation required for:
  - reset list
  - delete item
  - delete list
- Sign-out remains single-step action from profile

## Security and Privacy Considerations
- Auth tokens stored in secure mobile storage
- Share links are never embedded in static UI assets
- Sensitive actions routed through authenticated API paths only

## Test Strategy (Design-Level)
- Navigation integration tests:
  - auth gate routing
  - first-launch onboarding routing
  - last-active-list routing
- UI behavior tests:
  - checkbox toggles
  - inline add
  - item modal validation
  - destructive confirmations
- Offline tests:
  - queue creation
  - reconnect replay
  - replay error rendering
- Accessibility smoke checks for critical controls and labels

## Requirement-to-Design Mapping
- FR-ui-01/02/03/04 -> route tree + auth/onboarding gates
- FR-ui-05/06/07/08 -> list screens + item editor contracts
- FR-ui-09 -> members/share screen contracts
- FR-ui-10/11 -> profile/notifications contracts
- FR-ui-12 -> history + quick-restore contract
- FR-ui-13 -> loading/error/empty/offline state policy
- FR-ui-14/16 -> onboarding + permission strategy
- FR-ui-15 -> confirmation pattern policy
- FR-ui-17/18/19 -> Tamagui design direction + accessibility baseline
- NFR-01/02 -> low-tap action path and minimal-complexity composition
