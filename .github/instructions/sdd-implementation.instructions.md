---
applyTo: "src/**,tests/**"
description: "Implementation guidelines for SDD: Every implementation must be linked to a requirement with tests and specification"
---

# SDD Implementation Guidelines

## Core Rule
Every implementation change must map to a documented feature spec.

Traceability chain:

`specs/features/*.md -> src/** -> tests/** -> specs/current-state.md`

## Implementation Sequence
1. Read the feature spec and acceptance criteria.
2. Write or update tests first where possible.
3. Implement the minimal code needed to satisfy criteria.
4. Run validation for touched modules.
5. Update feature status and traceability notes in `specs/current-state.md`.

## Code Annotation (Recommended)
When useful, annotate files with requirement IDs, for example:

`// Requirement: FR-auth-01`

## Review Gate
Do not consider a feature complete unless:
- Acceptance criteria are covered by tests.
- Relevant tests pass.
- Spec links to code/tests are clear.
- `specs/current-state.md` is updated.

## Anti-Patterns
- Implementing behavior not present in specs.
- Large mixed changes across unrelated features.
- Leaving tests for later without explicit agreement.
const reports = allRFs.map(validateRequirement);

console.log('📊 Traceability Report');
reports.forEach(r => {
  const status = r.isComplete ? '✅' : '❌';
  console.log(`${status} ${r.requirementId}: ${r.missingParts.join(', ') || 'Complete'}`);
});

const coverage = (reports.filter(r => r.isComplete).length / reports.length * 100).toFixed(2);
console.log(`\n📈 Implementation Coverage: ${coverage}%`);
```

Ejecútalo:
```bash
npm run validate:traceability
```

## Commits Descriptivos

Todo commit debe mencionar el requisito:

```bash
git commit -m "Implement RF-001: User authentication with email and password

- Added login feature specification (.github/specs/features/auth/login.feature)
- Implemented loginUser() function (src/features/auth/login.ts)
- Added unit and integration tests (tests/integration/auth.test.ts)
- Updated requirement status in .github/docs/REQUISITOS.md
- Added session management (src/features/auth/session.ts)

Specification: ✅
Tests: ✅ (8 passing)
Traceability: ✅
Code Review: Ready

Closes #15
"
```

## Matriz de Trazabilidad

Mantén actualizado el archivo `.github/traceability/requirements.json`:

```json
{
  "RF-001": {
    "titulo": "User Login",
    "status": "completed",
    "version": "1.0",
    "specification": "tests/specs/features/auth/login.feature",
    "tests": [
      "tests/integration/auth.test.ts",
      "tests/e2e/full-auth-flow.test.ts"
    ],
    "implementation": [
      "src/features/auth/login.ts",
      "src/features/auth/session.ts"
    ],
    "coverage": "100%",
    "dateCompleted": "2026-03-20",
    "author": "Adrian Garcia",
    "reviewedBy": "Team Lead"
  },
  "RF-002": { /* ... */ }
}
```

## Documentación Local

Cada feature debe tener si propio README:

```markdown
# Feature: User Authentication

## Overview
Handles user login, session creation, and authentication state.

## Requirements
- RF-001: User Login
- RF-002: Session Management

## Architecture
```
┌────────────┐
│  UI Layer  │
└─────┬──────┘
      ↓
┌────────────┐
│   Login    │
│  Service   │
└─────┬──────┘
      ↓
┌────────────┐
│  Database  │
└────────────┘
```

## Files
- `login.ts`: Login functionality
- `session.ts`: Session management
- `types.ts`: TypeScript interfaces

## Tests
- Unit: `__tests__/login.test.ts`
- Integration: `../../tests/integration/auth.test.ts`
- E2E: `../../tests/e2e/full-auth-flow.test.ts`

## Specification
See `tests/specs/features/auth/login.feature`
```

## Validación Continua

En CI/CD, ejecuta:

```yaml
# .github/workflows/spec-validation.yml

name: Spec-Driven Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run BDD Specs
        run: npm run spec:validate
      
      - name: Run All Tests
        run: npm test -- --coverage
      
      - name: Validate Traceability
        run: npm run traceability:validate
      
      - name: Check Implementation Coverage
        run: npm run coverage:check -- --threshold=80
      
      - name: Generate Report
        run: npm run docs:generate
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

---

**Recuerda:** Si falta el requisito, falta la especificación, falta el test o falta el código = ❌ No está listo.
