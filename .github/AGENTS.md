# Agent Registry

## Available Project Agents

### Requirements Analyst
- File: `.github/agents/requirements-analyst.agent.md`
- Purpose: requirement elicitation, use-case discovery, and specification drafting.
- Use for: transforming ideas into actionable feature specs in `specs/features/`.

## Repository Rule
When an agent starts feature work, it should read:
1. `specs/project.md`
2. `specs/conventions.md`
3. `specs/current-state.md`
4. The target file in `specs/features/`

Before proposing changes, the agent should identify whether the feature impacts `frontend/`, `backend/`, or both.

## Execution Defaults (SDD-Aligned)

### 1. Plan Mode Default
- Enter plan mode for any non-trivial task (3+ steps or architectural decisions).
- If something goes sideways, stop and re-plan immediately.
- Use plan mode for verification steps, not only implementation.
- Write or update the relevant feature spec upfront to reduce ambiguity.

### 2. Subagent Strategy
- Use subagents liberally to keep main context clean.
- Offload research, exploration, and parallel analysis to subagents.
- For complex problems, use parallel subagents to increase throughput.
- Use one task per subagent for focused execution.

### 3. Self-Improvement Loop
- After any user correction, update `tasks/lessons.md` with the pattern.
- Add a concrete rule that prevents repeating the same mistake.
- Iterate on lessons continuously to reduce repeated errors.
- Review relevant lessons at session start.

### 4. Verification Before Done
- Never mark a task complete without proving it works.
- Compare behavior before/after changes when relevant.
- Ask: "Would a staff engineer approve this?"
- Run tests, check logs, and demonstrate correctness.

### 5. Demand Elegance (Balanced)
- For non-trivial changes, ask if there is a more elegant solution.
- If a fix is hacky, re-implement cleanly with current knowledge.
- Skip over-engineering for simple, obvious fixes.
- Challenge your own solution before presenting it.

### 6. Autonomous Bug Fixing
- When given a bug report, proceed to reproduce and fix directly.
- Use logs, errors, and failing tests as primary signals.
- Minimize context switching required from the user.
- Resolve failing CI checks relevant to the requested scope.

## Task Management (SDD)
1. Plan first in the feature spec (`specs/features/*.md`) and keep planned tasks checkable.
2. Confirm acceptance criteria and impact (`frontend`, `backend`, or both) before implementing.
3. Track progress by updating task status as you complete steps.
4. Keep requirement-to-code-to-test traceability explicit.
5. Update `specs/current-state.md` with progress and coverage notes.
6. Capture reusable lessons in `tasks/lessons.md` after corrections.

## Core Principles
- Simplicity first: change the minimum code required to satisfy requirements.
- No laziness: find root causes; avoid temporary fixes.

## Backend Test Layout Convention
- For `backend/python-api`, keep all tests under `backend/python-api/tests` (never under `backend/python-api/app/tests`).
- Organize tests by layer and module:
	- `tests/unit/<module>/...`
	- `tests/integration/<module>/...`
- Keep only shared fixtures at `tests/conftest.py`.
