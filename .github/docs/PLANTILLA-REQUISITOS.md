# Plantilla: Documento de Requisitos

> **Nota:** Esta es una plantilla. Reemplaza con valores específicos de tu proyecto.

---

# Documento de Requisitos: [NOMBRE DEL PROYECTO]

**Proyecto:** [Nombre completo]  
**Versión:** 1.0  
**Fecha:** [DD/MM/YYYY]  
**Autor:** [Tu nombre]  
**Estado:** En Progreso / Aprobado / Revisión

---

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Descripción General](#descripción-general)
3. [Actores y Stakeholders](#actores-y-stakeholders)
4. [Casos de Uso Principales](#casos-de-uso-principales)
5. [Requisitos Funcionales](#requisitos-funcionales)
6. [Requisitos No Funcionales](#requisitos-no-funcionales)
7. [Restricciones y Limitaciones](#restricciones-y-limitaciones)
8. [Glosario](#glosario)

---

## 1. Introducción

### Propósito
[Describe brevemente el propósito de este documento de requisitos]

### Alcance
[Define qué está IN scope y qué está OUT of scope]

### Definiciones y Acrónimos
- **Acrónimo**: Definición completa
- **Usuario**: Persona que usa la aplicación

---

## 2. Descripción General

### 2.1 Visión del Proyecto
[¿Cuál es la gran visión? ¿Qué problema resuelve?]

**Problema a resolver:**
[Descripción del problema]

**Solución propuesta:**
[Cómo la aplicación resuelve el problema]

### 2.2 Objetivos Principales
- [ ] Objetivo 1
- [ ] Objetivo 2
- [ ] Objetivo 3

### 2.3 Usuarios Principales
[Describe brevemente los tipos de usuarios]

### 2.4 Diferenciadores del Mercado
[¿Qué hace que tu solución sea diferente?]

---

## 3. Actores y Stakeholders

### 3.1 Actores Principales

#### Actor 1: [Nombre del Actor]
- **Descripción:** [Quién es, qué hace]
- **Objetivos:** [Qué quiere lograr]
- **Características:** [Edad, experiencia técnica, etc.]

#### Actor 2: [Nombre del Actor]
- **Descripción:** [Quién es, qué hace]
- **Objetivos:** [Qué quiere lograr]
- **Características:** [Edad, experiencia técnica, etc.]

### 3.2 Actores Secundarios
[Sistemas externos, administradores, etc.]

### 3.3 Stakeholders
[Quiénes tienen interés en el proyecto]

---

## 4. Casos de Uso Principales

### Diagrama de Contexto

```
┌─────────────┐
│  [Sistema]  │
└─────────────┘
      ↕
[ Actores y Casos de Uso ]
```

### 4.1 Caso de Uso 1: [UC-001]

| Atributo | Descripción |
|----------|-------------|
| **Nombre** | [Verbo + Sustantivo] |
| **Actor Principal** | [Quién lo inicia] |
| **Actores Secundarios** | [Otros participantes] |
| **Precondiciones** | - [Condición previa 1]</br>- [Condición previa 2] |
| **Flujo Principal** | 1. [Paso 1]</br>2. [Paso 2]</br>3. [Paso 3] |
| **Flujos Alternativos** | **FA-1:** Si [condición]</br>&nbsp;&nbsp;entonces [pasos] |
| **Postcondiciones** | - [Estado resultante 1]</br>- [Estado resultante 2] |
| **Restricciones** | [Limitaciones especiales] |
| **Notas** | [Consideraciones adicionales] |

### 4.2 Caso de Uso 2: [UC-002]
[Repetir estructura]

### 4.3 Caso de Uso 3: [UC-003]
[Repetir estructura]

---

## 5. Requisitos Funcionales

### RF-001: [Nombre del Requisito]
**Descripción:** [Qué debe hacer el sistema]

**Criterios de Aceptación:**
- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Criterio 3

**Prioridad:** 🔴 Alta / 🟡 Media / 🟢 Baja  
**Dependencias:** [RF-002, RF-003]

---

### RF-002: [Nombre del Requisito]
**Descripción:** [Qué debe hacer el sistema]

**Criterios de Aceptación:**
- [ ] Criterio 1
- [ ] Criterio 2

**Prioridad:** 🔴 Alta / 🟡 Media / 🟢 Baja  
**Dependencias:** Ninguna

---

[Continúa con más requisitos funcionales...]

---

## 6. Requisitos No Funcionales

### Rendimiento (Performance)
- RNF-001: El sistema debe responder en menos de 2 segundos
- RNF-002: Soportar 1000 usuarios concurrentes

### Seguridad
- RNF-003: Todos los datos deben encriptarse
- RNF-004: Autenticación de dos factores

### Escalabilidad
- RNF-005: Arquitectura preparada para crecer a X usuarios

### Usabilidad
- RNF-006: Interfaz intuitiva para usuarios sin experiencia técnica
- RNF-007: Accesible según estándares WCAG 2.1

### Confiabilidad
- RNF-008: Disponibilidad del 99.9%
- RNF-009: Backup automático diario

---

## 7. Restricciones y Limitaciones

- **Tecnología:** [Stack recomendado o requerido]
- **Presupuesto:** [Límites financieros]
- **Tiempo:** [Timeline esperado]
- **Recursos:** [Equipo disponible]
- **Compatibilidad:** [Navegadores, SO, etc.]

---

## 8. Glosario

| Término | Definición |
|---------|-----------|
| **Usuario** | Persona que utiliza la aplicación |
| **Caso de Uso** | Secuencia de interacciones entre actor y sistema |
| **[Término 1]** | [Definición] |
| **[Término 2]** | [Definición] |

---

## ✅ Aprobaciones

| Rol | Nombre | Fecha | Firma |
|-----|--------|-------|-------|
| Product Owner | [Nombre] | [DD/MM/YYYY] | [ ] |
| Tech Lead | [Nombre] | [DD/MM/YYYY] | [ ] |
| Cliente | [Nombre] | [DD/MM/YYYY] | [ ] |

---

**Última actualización:** [DD/MM/YYYY]  
**Próxima revisión:** [DD/MM/YYYY]
