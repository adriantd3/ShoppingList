# ShoppingList - Estado del Proyecto

Este documento proporciona una **vista clara de qué se ha hecho, qué falta, y cómo todo está documentado** usando Spec-Driven Development.

## 📊 Estado General

```
Proyecto: ShoppingList
Metodología: Spec-Driven Development (SDD)
Estado: 🟡 En Configuración
Última Actualización: 2026-03-20
```

## ✅ Lo Que Se Ha Configurado

### 1. **Infraestructura SDD** ✅
- ✅ Requirements Analyst Agent (`.github/agents/`)
- ✅ Requirements Elicitation Skill (`.github/skills/`)
- ✅ Guí de mejores prácticas SDD (`.github/SDD-BEST-PRACTICES.md`)
- ✅ Guidelines de implementación (`.github/instructions/`)
- ✅ Copilot instructions (`.github/copilot-instructions.md`)
- ✅ spec-workflow skill (instalado globalmente)

### 2. **Plantillas y Templates** ✅
- ✅ Plantilla de requisitos (`.github/docs/PLANTILLA-REQUISITOS.md`)
- ✅ README de documentación (`.github/docs/README.md`)
- ✅ Guía de desarrollo (DEVELOPMENT.md)

### 3. **Agents Disponibles** ✅
- ✅ Requirements Analyst - Elicitar requisitos interactivamente
- ✅ Explore - Exploración del codebase (subagent)

## 📋 Requisitos Planificados

No hay requisitos documentados aún. El siguiente paso es:

1. Usar `/requirements-analyst` o `/requirements-elicitation`
2. Describir tu idea para ShoppingList
3. El agente generará un documento `REQUISITOS.md` completo

### Ejemplo de Requisitos Esperados

Para una aplicación de lista de compras típica:

```
RF-001: Creación de Lista de Compras
RF-002: Agregar Productos a Lista
RF-003: Marcar Producto como Comprado
RF-004: Eliminar Producto de Lista
RF-005: Compartir Lista con Otros Usuarios
RF-006: Usuario Authentication (Login)
RF-007: Sincronización en Tiempo Real
```

## 📁 Estructura de Carpetas SDD

```
.github/
├── docs/ .......................... Documentación
│   ├── REQUISITOS.md .............. [VACÍO - Crear con agent]
│   ├── ARQUITECTURA.md ............ [VACÍO - Crear después de requisitos]
│   ├── CHANGELOG.md ............... [VACÍO - Se actualiza con cada release]
│   └── PLANTILLA-REQUISITOS.md .... [✅ Plantilla lista]
│
├── specs/ ......................... Especificaciones Ejecutables
│   ├── features/ .................. [VACÍO - Crear uno por requisito]
│   │   └── ejemplo.feature ........ [Plantilla]
│   └── step-definitions/ ......... [VACÍO - Implementación de steps]
│
├── traceability/ .................. Mapeos RF ↔ Código
│   ├── requirements.json ......... [VACÍO - Se genera automáticamente]
│   ├── coverage-matrix.json ...... [VACÍO]
│   └── feature-matrix.html ....... [VACÍO]
│
├── agents/
│   └── requirements-analyst.agent.md ... [✅ Lissto para usar]
│
├── skills/
│   └── requirements-elicitation/SKILL.md [✅ Listo para usar]
│
└── instructions/
    ├── requirements.instructions.md ...... [✅ Normas documentadas]
    └── sdd-implementation.instructions.md [✅ Guidelines listos]

src/
├── features/ ....................... [VACÍO - Se crea por requisito]
│   ├── auth/
│   ├── products/
│   └── cart/
└── (estructura sin implementación aún)

tests/
├── specs/ .......................... [VACÍO]
├── integration/ ................... [VACÍO]
└── e2e/ ........................... [VACÍO]

DEVELOPMENT.md ...................... [✅ Guía completa lista]
```

## 🎯 Próximos Pasos

### Fase 1: Elicitación de Requisitos (Hoy)

**Acción:** Usa el Requirements Analyst Agent

```bash
# En el chat de VS Code, escribe:
/requirements-analyst

# El agente te preguntará:
# 1. ¿Cuál es el objetivo de ShoppingList?
# 2. ¿Quiénes son los usuarios?
# 3. ¿Cuáles son los casos de uso principales?
# 4. ¿Qué requisitos funcionales/no funcionales hay?

# Resultado: Se generará `.github/docs/REQUISITOS.md`
```

**Output Esperado:**
```
✅ .github/docs/REQUISITOS.md
   - RF-001 a RF-XXX documentados
   - Casos de uso definidos
   - Actores identificados
```

### Fase 2: Crear Especificaciones BDD (Próximo)

Para cada requisito, crear un `.feature` file:

```bash
.github/specs/features/
├── user-auth.feature
├── shopping-list.feature
├── products.feature
└── cart.feature
```

**Estructura:**
```gherkin
Feature: [Nombre]
  Scenario: [Caso positivo]
  Scenario: [Caso negativo]
```

### Fase 3: Implementación (Después)

Por cada requisito:
1. Tests en `tests/integration/`
2. Implementación en `src/features/`
3. Actualizar trazabilidad

### Fase 4: Validación Continua

```bash
npm run dev:check  # Antes de cada commit
npm run traceability:report  # Para ver progreso
```

## 🔗 Cómo Navegar el Proyecto

### "¿Qué se debe hacer?"
```bash
cat .github/docs/REQUISITOS.md
```

### "¿Dónde está RF-001 implementado?"
```bash
cat .github/traceability/requirements.json | grep RF-001
# Resultado: spec, tests, código, status
```

### "¿Hoy qué trabajo debo hacer?"
```bash
# Ver requirements sin completar
npm run traceability:report
# O revisar el tablero de Traceability
```

### "¿Cómo sé si mi código está bien?"
```bash
npm run dev:check
# Ejecuta:
# - npm test (tests unitarios)
# - npm run spec:validate (specs BDD)
# - npm run traceability:validate (mapeo de trazabilidad)
```

## 📊 Matriz de Responsabilidades

Quién hace qué en SDD:

```
┌─────────────────┬──────────────────┬──────────────────┐
│ Fase            │ Quién lo hace     │ Dónde se guarda  │
├─────────────────┼──────────────────┼──────────────────┤
│ Elicitar Req    │ Requirements Anal │ .github/docs/    │
│ Especificación  │ Product Owner     │ .github/specs/   │
│ Tests           │ QA / Developer    │ tests/           │
│ Implementación  │ Developer         │ src/features/    │
│ Validación      │ CI/CD (automático)│ reports/         │
│ Trazabilidad    │ (automático)      │ .github/tracer./ │
└─────────────────┴──────────────────┴──────────────────┘
```

## 🎓 Cómo Entender SDD en Este Proyecto

**Si tienes preguntas sobre:**

- **"¿Cómo agrego un requisito nuevo?"**
  → Lee: `DEVELOPMENT.md` → "Agregar Nuevo Requisito"
  → Ejecuta: `/requirements-analyst`

- **"¿Cómo escribo una especificación?"**
  → Lee: `.github/SDD-BEST-PRACTICES.md` → "Workflow de Desarrollo SDD"
  → Mira ejemplos en: `.github/specs/features/`

- **"¿Cómo vinculo código a requisitos?"**
  → Lee: `.github/instructions/sdd-implementation.instructions.md`
  → Busca: `@requirement` en ejemplos

- **"¿Cómo valido que todo está bien?"**
  → Ejecuta: `npm run dev:check`
  → Genera reporte: `npm run traceability:report`

## 📈 Progreso Esperado

```
Hoy (Día 1):
  ✅ Infraestructura SDD configurada
  ✅ Agentes y skills instalados
  🟡 Requisitos → Próximo paso

Semana 1:
  ✅ REQUISITOS.md completo
  ✅ Especificaciones BDD escritas
  🟡 Implementación → Próximo paso

Semana 2:
  ✅ Features implementadas
  ✅ Tests pasando
  ✅ Trazabilidad 100%

Mes 1:
  ✅ MVP completado
  ✅ Changelog documentado
  ✅ Proyecto listo para producción
```

## 🔍 Estado de Agents/Skills

### Agents Disponibles

| Agent | Estado | Ubicación | Uso |
|-------|--------|-----------|-----|
| **Requirements Analyst** | ✅ Listo | `.github/agents/` | `/requirements-analyst` |
| **Explore** | ✅ Listo | (built-in) | (subagent) |

### Skills Instalados

| Skill | Installs | Estado | Ubicación |
|-------|---------|--------|-----------|
| find-skills | 636K | ✅ Global | `~/.agents/skills/` |
| spec-workflow | 617 | ✅ Global | `~/.agents/skills/` |
| requirements-elicitation | Local | ✅ Project | `.github/skills/` |

## 💡 Pro Tips

1. **Usa `/requirements-analyst`** - Es tu mejor amigo para empezar
2. **Lee DEVELOPMENT.md** - Es tu guía de referencia siempre
3. **Valida con `npm run dev:check`** - Antes de cada commit
4. **Mantén trazabilidad actualizada** - Es tu mapa de ruta
5. **Documenta decisiones** - En `.github/docs/ARQUITECTURA.md`

## 🚀 Let's Go!

**¿Listo para empezar?**

```bash
# Opción 1: Usa el Agent interactivo
/requirements-analyst

# Opción 2: Usa el Skill
/requirements-elicitation

# Opción 3: Lee la guía primero
cat DEVELOPMENT.md
```

¡Bienvenido a ShoppingList con Spec-Driven Development! 🎉
