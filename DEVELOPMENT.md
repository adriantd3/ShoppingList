# Development Workflow

This project follows lightweight Spec-Driven Development (SDD).

## Source of Truth

Always start with:
- `specs/project.md`
- `specs/conventions.md`
- `specs/current-state.md`
- `specs/features/*.md`

## Feature Lifecycle

1. Write or update a feature spec in `specs/features/`.
2. Use `/plan-feature` to produce tasks and test strategy.
3. Use `/implement-feature` to implement incrementally.
4. Update `specs/current-state.md` with completion notes and traceability.

## Minimum Traceability

For each feature:
- Spec file in `specs/features/`.
- Related code paths in `src/`.
- Related tests in `tests/`.
- Status update in `specs/current-state.md`.

## Recommended Commit Style

Use commits that mention requirement/feature IDs, for example:

`feat(auth): implement FR-auth-01 login flow`

`test(auth): add integration coverage for FR-auth-01`

`docs(specs): update 001-auth acceptance criteria`

## Practical Notes

- Keep specs concise and executable.
- Prefer English in specs/prompts/skills for tool compatibility.
- Avoid process overhead: enough structure to support speed and quality.
- If a behavior is not in a spec, treat it as out of scope until clarified.
```bash
# Opción 1: Usa el agent interactivo
# En el chat: /requirements-analyst

# Opción 2: Usa el skill
# En el chat: /requirements-elicitation
```

### Paso 2: Documento se Genera Automáticamente
El agent/skill creará:
- `REQUISITOS.md` actualizado
- `spec.feature` en `.github/specs/`
- Template de test
- Template de implementación

### Paso 3: Implementar
```bash
# Copiar template de código
# Escribir tests primero (TDD)
# Luego implementar
# Validar
npm run dev:check
```

### Paso 4: Commit
```bash
git commit -m "Implement RF-XXX: [Descripción]

- Added specification in .github/specs/features/
- Implemented src/features/
- Added tests in tests/
- Updated traceability

Specification: ✅
Tests: ✅
"
```

## 🔍 Mapeo Requisito ↔ Código

Para encontrar dónde está implementado un requisito:

```bash
# Buscar RF-001 en todo el proyecto
grep -r "RF-001" .

# Ver archivo de trazabilidad
cat .github/traceability/requirements.json | grep "RF-001"
```

Resultado esperado:
```
RF-001: User Login
spec:        .github/specs/features/auth/login.feature
code:        src/features/auth/login.ts
tests:       tests/integration/auth.test.ts
status:      ✅ Completado
coverage:    100%
```

## 🎓 Mejores Prácticas

### ✅ Haz Esto
- Escribe especificación → Escribe tests → Implementa
- Mantén trazabilidad actualizada
- Documenta metadatos (`@requirement`, `@feature`, etc.)
- Groupea código por características (no por técnica)
- Valida con `npm run dev:check` antes de push

### ❌ No Hagas Esto
- No escribas código sin especificación
- No olvides actualizar trazabilidad
- No mezcles requisitos diferentes en un PR
- No dejes specs sin tests
- No cambies requisitos viejos sin actualizar documentación

## 📚 Recursos

- **SDD Guía Completa:** `.github/SDD-BEST-PRACTICES.md`
- **Implementación Guidelines:** `.github/instructions/sdd-implementation.instructions.md`
- **Requisitos Template:** `.github/docs/PLANTILLA-REQUISITOS.md`
- **Requirements Analyst Agent:** `.github/agents/requirements-analyst.agent.md`

## 🤖 Usar el Requirements Analyst

En cualquier momento puedes pedir ayuda al agente especializado:

```bash
# En el chat/editor, escribe:
/requirements-analyst

# Te preguntará sobre:
# 1. Visión del proyecto
# 2. Actores

# 3. Casos de uso
# 4. Requisitos
# 5. Generará documento automáticamente
```

## 📞 Cuando Necesites Ayuda

1. **¿Cómo agrego un nuevo requisito?**
   → Usa `/requirements-analyst` o `/requirements-elicitation`

2. **¿Dónde está implementado RF-001?**
   → Busca en `.github/traceability/requirements.json`

3. **¿Qué especificaciones hay?**
   → Mira `.github/specs/features/`

4. **¿Cómo valido mi cambio?**
   → Ejecuta `npm run dev:check`

5. **¿Cómo genero un reporte?**
   → `npm run traceability:report` o `npm run coverage:report`

---

**¡Bienvenido a SDD! 🚀** 

Tu proyecto está ahora estructurado de forma que cada línea de código está vinculada a un requisito verificable. Esto significa:

✅ Menos bugs (porque todo está testeado)  
✅ Mejor mantenibilidad (porque está documentado)  
✅ Onboarding más fácil (porque es claro qué hace cada cosa)  
✅ Desarrollo más rápido (porque sabes exactamente qué hacer)
