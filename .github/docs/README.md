# Requirements Elicitation

Esta carpeta contiene herramientas para elicitar, documentar y estructurar requisitos de software de forma profesional.

## 📁 Estructura

```
.github/
├── agents/
│   └── requirements-analyst.agent.md      # Custom Agent especializado
├── skills/
│   └── requirements-elicitation/
│       └── SKILL.md                       # Skill invocable
├── instructions/
│   └── requirements.instructions.md       # Normas de formato
└── docs/
    ├── PLANTILLA-REQUISITOS.md            # Template para documentos
    └── requisitos/                         # Documentos generados
```

## 🚀 Cómo Usar

### Opción 1: Usar el Custom Agent
Abre el chat y escribe:
```
/requirements-analyst
```

El agente especializado te hará preguntas interactivas y documentará todo.

### Opción 2: Usar el Skill
Escribe en el chat:
```
/requirements-elicitation
```

Para buscar y usar el skill: 
```bash
npx skills find requirements elicitation
```

### Opción 3: Instalación desde repositorio
Desde tu proyecto, ejecuta:
```bash
npx skills add . --skill requirements-elicitation
```

## 📝 Proceso

El agente te guiará a través de 5 fases:

1. **Visión y Contexto** (5-10 min)
   - Objetivo principal
   - Usuarios
   - Problema a resolver

2. **Actores y Stakeholders** (5-10 min)
   - Tipos de usuarios
   - Roles y responsabilidades

3. **Casos de Uso** (15-30 min)
   - Flujos principales
   - Flujos alternativos
   - Precondiciones/postcondiciones

4. **Requisitos** (10-20 min)
   - Requisitos funcionales (RF-001, etc.)
   - Requisitos no funcionales

5. **Documento Final** (Automático)
   - Generación de especificación completa
   - Exportación a markdown

## 🎯 Salida Esperada

Recibirás un archivo markdown en `.github/docs/requisitos/` con:

✅ Descripción clara del proyecto  
✅ Casos de uso estructurados  
✅ Requisitos funcionales numerados  
✅ Requisitos no funcionales  
✅ Restricciones y limitaciones  
✅ Glosario de términos  

## ⌨️ Comandos Rápidos

Durante la sesión con el agente:

| Comando | Efecto |
|---------|--------|
| `/usa-casos` | Saltar a fase de casos de uso |
| `/requisitos` | Saltar a fase de requisitos |
| `/generar` | Generar documento final |
| `/revisar` | Revisar lo documentado |
| `/exportar` | Exportar a diferentes formatos |

## 📚 Referencia

- **Plantilla:** Ver `PLANTILLA-REQUISITOS.md`
- **Instrucciones:** Ver `.github/instructions/requirements.instructions.md`
- **Custom Agent:** Ver `.github/agents/requirements-analyst.agent.md`

## 💡 Tips

1. **Dedica tiempo:** 45-60 minutos ininterrumpidos para mejores resultados
2. **Sé específico:** Describe detalles que parecerían obvios
3. **Itera:** El documento se puede revisar y actualizar
4. **Valida:** Al final, revisa con stakeholders principales

## 🔗 Integración

Este agente/skill funciona mejor con:
- **GitHub Copilot**
- **Claude Code**
- **Cursor**
- **Cline**
- **Otros agentes IA** (ver skills.sh)

---

**¿Listo para empezar?**

Escribe en el chat: `/requirements-analyst` o `/requirements-elicitation`

¡Tu agente te guiará desde aquí! 🚀
