---
applyTo: "**"
description: "Spec-Driven Development: Guidelines for building software with executable specifications, traceability, and continuous validation"
---

# Spec-Driven Development (SDD)

## Introducción

**Spec-Driven Development** es una metodología donde:
- Las **especificaciones** son el origen de la verdad
- Todo el código está **directamente vinculado** a requisitos
- Las **especificaciones son ejecutables** (pueden validarse automáticamente)
- Existe **trazabilidad completa** entre requisitos → código → tests

## Principios Fundamentales

### 1. **Especificación es Código**
- Los requisitos no son solo documentos, son definiciones ejecutables
- Se escriben en lenguaje cercano al negocio (BDD: Gherkin, Cucumber)
- Son verificables automáticamente

### 2. **Trazabilidad Completa**
```
Requisito (RF-001) 
    ↓
Scenario/Feature (Gherkin)
    ↓
Test (Jest, Playwright)
    ↓
Implementación (Código)
    ↓
Validación Automática
```

### 3. **Single Source of Truth**
- Una especificación clara = No ambigüedades
- Reduce retrasos por malentendidos
- Acelera el desarrollo

## Estructura de Proyecto SDD

```
proyecto/
├── .github/
│   ├── docs/
│   │   ├── REQUISITOS.md          # Documento de requisitos
│   │   ├── ARQUITECTURA.md        # Decisiones técnicas
│   │   └── CHANGELOG.md           # Cambios realizados
│   ├── specs/                     # Especificaciones ejecutables
│   │   ├── features/              # BDD Features (Gherkin)
│   │   │   ├── user-auth.feature
│   │   │   ├── product-list.feature
│   │   │   └── shopping-cart.feature
│   │   └── step-definitions/      # Implementación de steps
│   │       ├── user-auth.steps.ts
│   │       └── product-list.steps.ts
│   └── traceability/
│       ├── requirements.json      # Mapeo RF-001 → Code
│       ├── coverage.json          # Qué está cubierto
│       └── matrix.json            # Matriz de trazabilidad
├── src/
│   ├── features/                  # Organizado por características
│   │   ├── auth/
│   │   ├── products/
│   │   └── cart/
│   └── README.md                  # Documentación local
├── tests/
│   ├── unit/                      # Unit tests (Jest)
│   ├── integration/               # Integration tests
│   ├── e2e/                       # E2E tests (Playwright)
│   └── specs/                     # Spec-based tests
└── DEVELOPMENT.md                 # Guía de desarrollo SDD
```

## Workflow de Desarrollo SDD

### Paso 1: Definir Especificación (Antes de Código)

```gherkin
# .github/specs/features/user-auth.feature

Feature: User Authentication
  As a user
  I want to log in securely
  So that I can access my personal data

  Background:
    Given the application is running
    And the user database is available

  Scenario: Successful login with valid credentials
    Given a user exists with email "user@example.com"
    And the password is "SecurePass123"
    When the user enters email "user@example.com"
    And the user enters password "SecurePass123"
    And the user clicks login
    Then the user should be authenticated
    And the user should be redirected to dashboard
    And a session should be created

  Scenario: Failed login with invalid password
    Given a user exists with email "user@example.com"
    When the user enters email "user@example.com"
    And the user enters password "WrongPassword"
    And the user clicks login
    Then the user should see error "Invalid credentials"
    And the user should NOT be authenticated
```

### Paso 2: Vincular Requisito a Especificación

```markdown
# REQUISITOS.md

## RF-001: Autenticación de Usuario

**Descripción:** Sistema de login seguro con email y contraseña.

**Criterios de Aceptación:**
- [ ] Aceptar email y contraseña válidos
- [ ] Rechazar credenciales inválidas
- [ ] Crear sesión tras login exitoso
- [ ] Encriptar contraseñas (bcrypt, argon2)

**Especificación Ejecutable:**
→ Ver `.github/specs/features/user-auth.feature`

**Tests:**
→ Ver `tests/integration/user-auth.test.ts`

**Implementación:**
→ Ver `src/features/auth/login.ts`

**Estado:** ✅ Completado (v1.2)
**Última Actualización:** 2026-03-20
```

### Paso 3: Implementar Pasos (Step Definitions)

```typescript
// .github/specs/step-definitions/user-auth.steps.ts

import { Given, When, Then } from '@cucumber/cucumber';
import { loginUser, createUser, expectError } from '../../src/features/auth';

Given('a user exists with email {string}', async (email: string) => {
  await createUser({ email, password: 'SecurePass123' });
});

When('the user enters email {string}', function(email: string) {
  this.testContext.email = email;
});

When('the user enters password {string}', function(password: string) {
  this.testContext.password = password;
});

When('the user clicks login', async function() {
  this.testContext.result = await loginUser(
    this.testContext.email,
    this.testContext.password
  );
});

Then('the user should be authenticated', function() {
  expect(this.testContext.result.isAuthenticated).toBe(true);
});
```

### Paso 4: Implementar Funcionalidad

```typescript
// src/features/auth/login.ts

export async function loginUser(email: string, password: string) {
  // Validaciones
  if (!email || !password) {
    throw new Error('Email and password required');
  }

  // Buscar usuario
  const user = await db.users.findByEmail(email);
  if (!user) {
    throw new Error('Invalid credentials');
  }

  // Verificar contraseña
  const isValid = await bcrypt.compare(password, user.passwordHash);
  if (!isValid) {
    throw new Error('Invalid credentials');
  }

  // Crear sesión
  const session = await createSession(user.id);

  return {
    isAuthenticated: true,
    userId: user.id,
    sessionId: session.id,
  };
}
```

### Paso 5: Tests Automáticos

```typescript
// tests/integration/user-auth.test.ts

describe('User Authentication', () => {
  describe('RF-001: Login', () => {
    it('should allow login with valid credentials', async () => {
      const user = await createTestUser('user@example.com', 'SecurePass123');
      const result = await loginUser('user@example.com', 'SecurePass123');
      
      expect(result.isAuthenticated).toBe(true);
      expect(result.userId).toBe(user.id);
    });

    it('should reject invalid password', async () => {
      await createTestUser('user@example.com', 'SecurePass123');
      
      expect(async () => {
        await loginUser('user@example.com', 'WrongPassword');
      }).rejects.toThrow('Invalid credentials');
    });
  });
});
```

### Paso 6: Mapeo de Trazabilidad

```json
// .github/traceability/requirements.json

{
  "RF-001": {
    "titulo": "Autenticación de Usuario",
    "estado": "completado",
    "version": "1.0",
    "especificacion": ".github/specs/features/user-auth.feature",
    "tests": [
      "tests/integration/user-auth.test.ts:valid-credentials",
      "tests/integration/user-auth.test.ts:invalid-password"
    ],
    "implementacion": [
      "src/features/auth/login.ts",
      "src/features/auth/session.ts"
    ],
    "ultimaActualizacion": "2026-03-20",
    "autor": "Adrian Garcia"
  },
  "RF-002": { /* ... */ }
}
```

## Mejores Prácticas SDD

### ✅ DO (Haz esto)

1. **Escribir especificaciones primero**
   ```gherkin
   # Primero: Especificación clara
   Scenario: User can add product to cart
   
   # Luego: Implementar
   ```

2. **Usar lenguaje de negocio**
   ```gherkin
   # ✅ Bueno (entiende el negocio)
   When the user clicks "Add to Cart"
   
   # ❌ Malo (muy técnico)
   When POST /api/cart/items
   ```

3. **Una especificación = Un requisito**
   ```
   RF-001 ↔ user-auth.feature (1-to-1 mapping)
   ```

4. **Documentar cambios**
   ```markdown
   ## Changelog
   
   ### v1.2 (2026-03-20)
   - RF-001: Login ahora soporta OAuth2 (Adrian)
   - RF-002: Agregado 2FA (Maria)
   ```

5. **Mantener traceability actualizado**
   ```bash
   # Script para validar trazabilidad
   npm run validate:traceability
   ```

### ❌ DON'T (Evita esto)

1. ❌ Escribir código sin especificación
2. ❌ Mezclar múltiples requisitos en un scenario
3. ❌ Usar jerga técnica extrema en features
4. ❌ Olvidar actualizar trazabilidad
5. ❌ Dejar specs sin implementar

## Herramientas Recomendadas

| Herramienta | Propósito | Proyecto |
|-------------|-----------|----------|
| **Cucumber/Gherkin** | BDD Specifications | ✅ |
| **Jest** | Unit & Integration Tests | ✅ |
| **Playwright** | E2E Tests | ✅ |
| **OpenAPI/Swagger** | API Specs | ✅ |
| **GraphQL SDL** | API/Query Specs | Si aplica |
| **TypeScript** | Type Safety | ✅ |
| **ESLint** | Code Quality | ✅ |

## Flujo de Trabajo Diario

```
1. MORNING STANDUP
   - Reviewar requisitos asignados (RF-001, RF-002)
   - Verificar especificaciones (.github/specs/)
   - Verificar tests (tests/)

2. DEVELOPMENT
   - Leer feature/scenario
   - Escribir test cases
   - Implementar código
   - Todo debería estar vinculado

3. VALIDATION
   - Ejecutar: npm test
   - Verificar: npm run validate:traceability
   - Reviewar: traceability matrix

4. COMMIT
   git commit -m "Implement RF-001: Add user authentication
   
   - Added .github/specs/features/user-auth.feature
   - Implemented src/features/auth/login.ts
   - Added tests/integration/user-auth.test.ts
   - Updated .github/traceability/requirements.json"

5. DOCUMENTATION
   - Actualizar CHANGELOG
   - Marcar RF como "completado"
   - Agregar notas de implementación
```

## Scripts Útiles

```json
{
  "scripts": {
    "spec:validate": "cucumber-js",
    "spec:report": "cucumber-js --format html:spec-report.html",
    "traceability:validate": "ts-node scripts/validate-traceability.ts",
    "traceability:coverage": "ts-node scripts/coverage-matrix.ts",
    "dev:check": "npm test && npm run traceability:validate",
    "docs:generate": "ts-node scripts/generate-spec-docs.ts"
  }
}
```

## Checklist para Cada Feature

```markdown
## [Feature Name] - Checklist

### Pre-Implementation
- [ ] Requisito identificado y documentado (RF-XXX)
- [ ] Especificación escrita (Gherkin)
- [ ] Criterios de aceptación claros
- [ ] Caso de prueba diseñado

### Implementation
- [ ] Feature implementado
- [ ] Tests unitarios verdes
- [ ] Tests integración verdes
- [ ] Trazabilidad actualizada

### Post-Implementation
- [ ] Code review completado
- [ ] Documentation actualizada
- [ ] Changelog actualizado
- [ ] Tests E2E pasando
- [ ] Performance validado

### Release
- [ ] Versión actualizada
- [ ] CHANGELOG.md actualizado
- [ ] Requisito marcado como "Completado"
```

## Referencias y Recursos

- **Cucumber Documentation:** https://cucumber.io/docs/
- **BDD Best Practices:** https://cucumber.io/docs/bdd/
- **Spec by Example:** https://gojko.net/books/specification-by-example/
- **TDD Discipline:** https://www.typescriptlang.org/docs/handbook/testing.html

---

**Recuerda:** En SDD, la especificación NO es un documento estático - es código ejecutable que valida que tu implementación es correcta.
