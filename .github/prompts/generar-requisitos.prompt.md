---
name: generar-requisitos
description: "Use when: Necesitas elicitar requisitos de software mediante preguntas interactivas y generar un documento de especificaciones completo."
parameters:
  - name: "nombreProyecto"
    type: "string"
    description: "Nombre de tu proyecto (ej: ShoppingList, TaskManager)"
    required: false
---

# Generador de Documento de Requisitos

Te ayudaré a crear un documento de requisitos profesional y completo haciendo preguntas estructuradas sobre tu proyecto.

## Contexto

Tu proyecto: {{nombreProyecto}}

## Proceso

Responde estas preguntas de forma cuidadosa. Usaré tus respuestas para generar un documento de requisitos completo con:

✅ Descripción general del sistema  
✅ Actores identificados  
✅ Casos de uso con flujos  
✅ Requisitos funcionales (RF-001, RF-002, etc.)  
✅ Requisitos no funcionales  
✅ Restricciones y limitaciones  

## Fase 1: Visión y Contexto

**Pregunta 1:** ¿Cuál es el objetivo principal de {{nombreProyecto}}? ¿Qué problema específico resuelve?

**Pregunta 2:** ¿Quiénes son los usuarios principales? ¿Hay diferentes tipos de usuarios?

**Pregunta 3:** ¿Hay aplicaciones similares en el mercado? ¿Qué hace que tu solución sea diferente?

**Pregunta 4:** ¿Cuáles serían los 3 objetivos principales que debe cumplir esta aplicación?

## Fase 2: Actores y Stakeholders

**Pregunta 5:** Describe brevemente cada tipo de usuario/actor que usará el sistema.

**Pregunta 6:** ¿Hay sistemas externos que deben integrarse? (ej: bases de datos, APIs, servicios)

## Fase 3: Casos de Uso

**Pregunta 7:** ¿Cuáles son los 3-5 casos de uso principales? (ej: "Crear lista", "Agregar producto", etc.)

Para el primer caso de uso principal, describe:
- **La acción:** [Verbo + Sustantivo]
- **Quién la hace:** [Actor]
- **Pasos:** [Flujo paso a paso]
- **Resultado esperado:** [Postcondición]

## Fase 4: Requisitos Específicos

**Pregunta 8:** ¿Hay requisitos técnicos específicos? (ej: tecnologías, compatibilidad, base de datos)

**Pregunta 9:** ¿Qué requisitos no funcionales son críticos? (rendimiento, seguridad, escalabilidad)

**Pregunta 10:** ¿Hay limitaciones de presupuesto, tiempo o recursos que debamos documentar?

---

## Generando tu documento...

Compilaré todas tus respuestas en un documento estructurado que se guardará en:

`.github/docs/requisitos/requisitos-{{nombreProyecto}}.md`

Después de completar la elicitación, el documento incluirá:

```markdown
- Portada ejecutiva
- Descripción general
- Actores y stakeholders
- Casos de uso con diagramas
- Requisitos funcionales numerados
- Requisitos no funcionales
- Restricciones y limitaciones
- Glosario de términos
```

¿Listo? Vamos a empezar. 🚀

**¿Cuál es el nombre de tu proyecto?**
