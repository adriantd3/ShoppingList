---
applyTo: "backend/**,frontend/**,specs/**,**/tests/**"
description: "Automatic skill routing for backend/frontend/spec work. Load relevant testing and SDD skills before implementation."
---

# Auto Skill Routing (Workspace)

## Purpose
Ensure relevant skills are loaded automatically based on task scope and touched paths.

## Mandatory loading rules
When a task matches any rule below, load the listed skills before taking implementation actions.

### 1) Python backend testing work (`backend/**`, Python API tests)
Load:
- `python-testing-patterns`
- `testing-best-practices`

Triggers:
- Writing or updating pytest tests.
- FastAPI route/service/repository changes that require unit or integration tests.
- Test reliability, fixture design, mocking, or coverage improvements.

### 2) React Native testing work (`frontend/**`, RN components/screens)
Load:
- `react-native-testing`
- `testing-best-practices`

Triggers:
- Writing or updating Jest/RNTL tests.
- Component behavior, async UI, user events, or screen-flow testing.
- Test flakiness or rendering/query strategy fixes.

### 3) Spec-driven feature workflow (`specs/**` or feature implementation with acceptance criteria)
Load:
- `spec-driven-development`
- `implement-feature` (for implementation from existing specs)
- `requirements-elicitation` (when requirements are incomplete)

Triggers:
- New feature planning.
- Requirement/design/task breakdown.
- Requirement-to-code-to-test traceability updates.

## Combined contexts
If a task spans domains, load all relevant skills.

Examples:
- Backend feature with new API contracts + tests: `spec-driven-development` + `implement-feature` + `python-testing-patterns` + `testing-best-practices`.
- Frontend feature with RN screens + tests from spec: `spec-driven-development` + `implement-feature` + `react-native-testing` + `testing-best-practices`.

## Safety and quality notes
- Prefer stable, high-signal tests over high test counts.
- Always include negative-path and authorization/error-path coverage for API work.
- Keep deterministic test setup (clock/timezone/locale/isolation) where relevant.
