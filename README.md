# ShoppingList

Personal project configured for lightweight Spec-Driven Development (SDD).

## Recommended Structure

```
mi-proyecto/
├─ .github/
│  ├─ copilot-instructions.md
│  ├─ prompts/
│  │  ├─ plan-feature.prompt.md
│  │  └─ implement-feature.prompt.md
│  └─ skills/
│     └─ implement-feature/
│        └─ SKILL.md
│
├─ specs/
│  ├─ project.md
│  ├─ conventions.md
│  ├─ current-state.md
│  └─ features/
│     ├─ 001-auth.md
│     └─ 002-dashboard.md
│
├─ src/
├─ tests/
├─ README.md
└─ AGENTS.md
```

## Quick Start

1. Define or update a feature in `specs/features/`.
2. Use `/plan-feature` to create a technical plan.
3. Use `/implement-feature` to execute incrementally.
4. Update `specs/current-state.md` after each completed feature.

## Active Customizations

- Repository instructions: `.github/copilot-instructions.md`
- Path instructions: `.github/instructions/*.instructions.md`
- Prompts: `.github/prompts/`
- Skills: `.github/skills/`
- Agents registry: `AGENTS.md` and `.github/AGENTS.md`

## Notes

- Keep prompts/skills in English for better model portability.
- Prefer plain formatting over emojis in specs and governance docs.
- Keep SDD lightweight: enough structure to maintain traceability, not process overhead.