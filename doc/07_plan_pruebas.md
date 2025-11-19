# Plan de Pruebas - LogiCo

## 1. Introducción

Este documento describe el plan de pruebas para el sistema LogiCo, un sistema de logística farmacéutica. El plan incluye casos de uso, requerimientos funcionales y no funcionales, y tres tipos de pruebas: funcionales, de integración y de usabilidad.

---

## 2. Alcance del Plan de Pruebas

### 2.1. Objetivos
- Verificar que el sistema cumple con todos los requerimientos funcionales
- Validar que el sistema cumple con los requerimientos no funcionales
- Asegurar la calidad y confiabilidad del software
- Identificar defectos antes de la puesta en producción

### 2.2. Cobertura
- Todos los módulos del sistema
- Todos los casos de uso implementados
- Interfaces de usuario
- API REST
- Base de datos

---

## 3. Requerimientos Funcionales

### RF-01: Gestión de Usuarios
**Descripción:** El sistema debe permitir gestionar usuarios con diferentes roles.

**Casos de Uso:**
- CU-01: Crear usuario (solo admin)
- CU-02: Editar usuario (admin edita todo, coordinador solo moto)
- CU-03: Listar usuarios (según rol)
- CU-04: Ver detalle de usuario
- CU-05: Cambiar estado de turno (solo repartidor)

**Criterios de Aceptación:**
- Admin puede crear usuarios con RUT, rol, teléfono
- Coordinador puede cambiar moto de usuarios
- Repartidor solo se ve a sí mismo
- Validación de descanso máximo 1 hora

### RF-02: Gestión de Motos
**Descripción:** El sistema debe permitir gestionar la flota de motos.

**Casos de Uso:**
- CU-06: Crear moto (solo coordinador/admin)
- CU-07: Editar moto (solo coordinador/admin)
- CU-08: Listar motos
- CU-09: Asignar repartidor a moto (solo coordinador/admin)
- CU-10: Ver detalle de moto

**Criterios de Aceptación:**
- Solo coordinador/admin pueden crear/editar motos
- Asignación de repartidor actualiza estado de moto
- Validación de patente única

### RF-03: Gestión de Órdenes
**Descripción:** El sistema debe permitir gestionar órdenes de medicamentos.

**Casos de Uso:**
- CU-11: Crear orden (solo coordinador/admin)
- CU-12: Editar orden (solo coordinador/admin)
- CU-13: Listar órdenes (filtrado por rol)
- CU-14: Ver detalle de orden
- CU-15: Cambiar estado de orden
- CU-16: Asignar repartidor a orden (solo coordinador/admin)
- CU-17: Agregar medicamentos a orden

**Criterios de Aceptación:**
- Prioridad automática según tipo de orden
- Repartidor solo ve sus órdenes asignadas
- Historial de movimientos registrado

### RF-04: Gestión de Despachos
**Descripción:** El sistema debe permitir gestionar despachos de órdenes.

**Casos de Uso:**
- CU-18: Crear despacho
- CU-19: Listar despachos (solo último intento por orden)
- CU-20: Ver detalle de despacho
- CU-21: Registrar resultado de entrega
- CU-22: Subir foto de entrega
- CU-23: Registrar coordenadas GPS

**Criterios de Aceptación:**
- Múltiples intentos de despacho por orden
- Solo se muestra último intento en lista
- Contador de intentos totales visible

### RF-05: Dashboard y Reportes
**Descripción:** El sistema debe mostrar estadísticas y reportes.

**Casos de Uso:**
- CU-24: Ver dashboard con estadísticas
- CU-25: Ver gráficos de entregas
- CU-26: Generar reporte diario
- CU-27: Exportar reporte a CSV

**Criterios de Aceptación:**
- Estadísticas actualizadas en tiempo real
- Gráficos interactivos con Chart.js
- Exportación funcional

### RF-06: Autenticación y Autorización
**Descripción:** El sistema debe gestionar autenticación y permisos.

**Casos de Uso:**
- CU-28: Iniciar sesión
- CU-29: Cerrar sesión
- CU-30: Validar permisos por rol
- CU-31: Acceso a API con token

**Criterios de Aceptación:**
- Login funcional
- Redirección según rol
- API protegida con autenticación

---

## 4. Requerimientos No Funcionales

### RNF-01: Rendimiento
- Tiempo de respuesta < 2 segundos para páginas
- API responde en < 500ms
- Base de datos optimizada con índices

### RNF-02: Seguridad
- Protección CSRF activa
- Autenticación requerida
- Validación de entrada
- Prevención SQL Injection
- Protección XSS

### RNF-03: Usabilidad
- Interfaz intuitiva
- Diseño responsivo
- Navegación clara
- Mensajes de error claros

### RNF-04: Compatibilidad
- Compatible con navegadores modernos
- Responsive en móviles y tablets
- Compatible con PostgreSQL 12+

### RNF-05: Escalabilidad
- Base de datos normalizada
- Consultas optimizadas
- Paginación en listados

---

## 5. Casos de Uso Implementados

### 5.1. Diagrama de Casos de Uso

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       ├─── Gestionar Usuarios
       ├─── Gestionar Motos
       ├─── Gestionar Órdenes
       ├─── Gestionar Despachos
       ├─── Ver Dashboard
       ├─── Generar Reportes
       └─── Autenticarse
```

### 5.2. Lista Completa de Casos de Uso

| ID | Nombre | Actor | Prioridad | Estado |
|----|--------|-------|-----------|--------|
| CU-01 | Crear Usuario | Admin | Alta | ✅ |
| CU-02 | Editar Usuario | Admin/Coordinador | Alta | ✅ |
| CU-03 | Listar Usuarios | Todos | Media | ✅ |
| CU-04 | Ver Detalle Usuario | Todos | Media | ✅ |
| CU-05 | Cambiar Estado Turno | Repartidor | Alta | ✅ |
| CU-06 | Crear Moto | Coordinador/Admin | Alta | ✅ |
| CU-07 | Editar Moto | Coordinador/Admin | Alta | ✅ |
| CU-08 | Listar Motos | Todos | Media | ✅ |
| CU-09 | Asignar Repartidor a Moto | Coordinador/Admin | Alta | ✅ |
| CU-10 | Ver Detalle Moto | Todos | Media | ✅ |
| CU-11 | Crear Orden | Coordinador/Admin | Alta | ✅ |
| CU-12 | Editar Orden | Coordinador/Admin | Alta | ✅ |
| CU-13 | Listar Órdenes | Todos | Alta | ✅ |
| CU-14 | Ver Detalle Orden | Todos | Alta | ✅ |
| CU-15 | Cambiar Estado Orden | Todos | Alta | ✅ |
| CU-16 | Asignar Repartidor a Orden | Coordinador/Admin | Alta | ✅ |
| CU-17 | Agregar Medicamentos | Coordinador/Admin | Media | ✅ |
| CU-18 | Crear Despacho | Todos | Alta | ✅ |
| CU-19 | Listar Despachos | Todos | Media | ✅ |
| CU-20 | Ver Detalle Despacho | Todos | Media | ✅ |
| CU-21 | Registrar Resultado Entrega | Repartidor | Alta | ✅ |
| CU-22 | Subir Foto Entrega | Repartidor | Media | ✅ |
| CU-23 | Registrar Coordenadas GPS | Repartidor | Baja | ✅ |
| CU-24 | Ver Dashboard | Todos | Alta | ✅ |
| CU-25 | Ver Gráficos | Todos | Media | ✅ |
| CU-26 | Generar Reporte Diario | Admin | Media | ✅ |
| CU-27 | Exportar Reporte CSV | Admin | Baja | ✅ |
| CU-28 | Iniciar Sesión | Todos | Alta | ✅ |
| CU-29 | Cerrar Sesión | Todos | Alta | ✅ |
| CU-30 | Validar Permisos | Sistema | Alta | ✅ |
| CU-31 | Acceso API con Token | Desarrollador | Media | ✅ |

---

## 6. Tipos de Pruebas

### 6.1. Pruebas Funcionales

**Objetivo:** Verificar que cada funcionalidad cumple con sus requerimientos.

**Alcance:**
- Todas las funcionalidades del sistema
- Validaciones de negocio
- Reglas de permisos
- Flujos de trabajo

**Estrategia:**
- Pruebas manuales caso por caso
- Verificación de resultados esperados
- Validación de mensajes de error
- Pruebas de casos límite

### 6.2. Pruebas de Integración

**Objetivo:** Verificar que los módulos funcionan correctamente juntos.

**Alcance:**
- Integración frontend-backend
- Integración con base de datos
- Integración API REST
- Flujos completos de usuario

**Estrategia:**
- Pruebas end-to-end
- Verificación de datos entre capas
- Validación de transacciones
- Pruebas de API

### 6.3. Pruebas de Usabilidad

**Objetivo:** Verificar que la interfaz es intuitiva y fácil de usar.

**Alcance:**
- Navegación
- Diseño responsivo
- Mensajes al usuario
- Flujos de trabajo

**Estrategia:**
- Pruebas con usuarios reales
- Checklist de usabilidad
- Pruebas en diferentes dispositivos
- Evaluación de accesibilidad

---

## 7. Casos de Prueba Detallados

### 7.1. Pruebas Funcionales

#### PF-01: Crear Usuario (Admin)
**Prioridad:** Alta
**Precondiciones:** Usuario autenticado como admin

**Pasos:**
1. Ir a "Usuarios" → "Nuevo Usuario"
2. Completar formulario:
   - Username: "testuser"
   - Email: "test@test.com"
   - Contraseña: "test1234"
   - RUT: "12345678-9"
   - Teléfono: "123456789"
   - Rol: "repartidor"
3. Hacer clic en "Guardar"

**Resultado Esperado:**
- Usuario creado exitosamente
- Mensaje de éxito mostrado
- Redirección a detalle de usuario
- Usuario visible en lista

**Resultado Obtenido:** [A completar en ejecución]

---

#### PF-02: Asignar Repartidor a Orden (Coordinador)
**Prioridad:** Alta
**Precondiciones:** 
- Usuario autenticado como coordinador
- Orden existente sin repartidor asignado
- Repartidor con moto asignada

**Pasos:**
1. Ir a detalle de orden
2. En sección "Asignar Repartidor", seleccionar repartidor
3. Hacer clic en "Asignar"

**Resultado Esperado:**
- Repartidor asignado a orden
- Mensaje de éxito
- Movimiento registrado en historial
- Orden visible en lista del repartidor

**Resultado Obtenido:** [A completar en ejecución]

---

#### PF-03: Cambiar Estado de Turno (Repartidor)
**Prioridad:** Alta
**Precondiciones:** Usuario autenticado como repartidor

**Pasos:**
1. Ir a "Usuarios" → Ver mi perfil
2. Seleccionar "Descanso" en estado de turno
3. Hacer clic en "Cambiar Estado"
4. Esperar 1 hora
5. Intentar cambiar estado nuevamente

**Resultado Esperado:**
- Estado cambia a "Descanso"
- Fecha de inicio registrada
- Después de 1 hora, cambio automático a "Disponible"
- Mensaje informativo mostrado

**Resultado Obtenido:** [A completar en ejecución]

---

#### PF-04: Listar Despachos (Solo Último Intento)
**Prioridad:** Media
**Precondiciones:** Orden con múltiples intentos de despacho

**Pasos:**
1. Crear orden
2. Crear despacho #1 (fallido)
3. Crear despacho #2 (fallido)
4. Crear despacho #3 (exitoso)
5. Ir a lista de despachos

**Resultado Esperado:**
- Solo se muestra despacho #3
- Badge muestra "3 intentos"
- Información del último intento visible

**Resultado Obtenido:** [A completar en ejecución]

---

### 7.2. Pruebas de Integración

#### PI-01: Flujo Completo de Orden
**Prioridad:** Alta

**Pasos:**
1. Admin crea orden
2. Coordinador asigna repartidor
3. Repartidor cambia estado a "ocupado"
4. Repartidor crea despacho
5. Repartidor registra resultado "entregado"
6. Sistema actualiza estado de orden
7. Dashboard muestra estadísticas actualizadas

**Resultado Esperado:**
- Todos los pasos ejecutados sin errores
- Datos consistentes en todas las vistas
- Historial completo registrado
- Estadísticas actualizadas

**Resultado Obtenido:** [A completar en ejecución]

---

#### PI-02: Integración API REST
**Prioridad:** Media

**Pasos:**
1. Obtener token de autenticación
2. Crear orden vía API
3. Listar órdenes vía API
4. Actualizar orden vía API
5. Asignar repartidor vía API

**Resultado Esperado:**
- Autenticación exitosa
- CRUD completo funcional
- Respuestas JSON correctas
- Códigos HTTP apropiados

**Resultado Obtenido:** [A completar en ejecución]

---

### 7.3. Pruebas de Usabilidad

#### PU-01: Navegación del Sistema
**Prioridad:** Alta

**Checklist:**
- [ ] Sidebar visible y funcional
- [ ] Enlaces correctos
- [ ] Breadcrumbs presentes
- [ ] Botones de acción claros
- [ ] Mensajes de feedback visibles

**Resultado Obtenido:** [A completar en ejecución]

---

#### PU-02: Diseño Responsivo
**Prioridad:** Media

**Dispositivos a Probar:**
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

**Checklist:**
- [ ] Layout se adapta correctamente
- [ ] Sidebar colapsa en móvil
- [ ] Tablas son scrollables
- [ ] Formularios son usables
- [ ] Botones son accesibles

**Resultado Obtenido:** [A completar en ejecución]

---

## 8. Matriz de Trazabilidad

| Requerimiento | Casos de Uso | Casos de Prueba | Estado |
|---------------|--------------|-----------------|--------|
| RF-01 | CU-01 a CU-05 | PF-01, PF-03 | ⏳ Pendiente |
| RF-02 | CU-06 a CU-10 | PF-02 | ⏳ Pendiente |
| RF-03 | CU-11 a CU-17 | PF-02, PI-01 | ⏳ Pendiente |
| RF-04 | CU-18 a CU-23 | PF-04, PI-01 | ⏳ Pendiente |
| RF-05 | CU-24 a CU-27 | - | ⏳ Pendiente |
| RF-06 | CU-28 a CU-31 | PI-02 | ⏳ Pendiente |

---

## 9. Criterios de Éxito

### 9.1. Criterios de Aceptación
- ✅ 100% de casos de uso críticos probados
- ✅ 90% de casos de uso totales probados
- ✅ 0 bugs críticos
- ✅ Máximo 5 bugs menores
- ✅ Todas las validaciones funcionando
- ✅ Todos los permisos validados

### 9.2. Criterios de Finalización
- Todas las pruebas ejecutadas
- Resultados documentados
- Bugs reportados y priorizados
- Plan de corrección definido

---

## 10. Recursos Necesarios

### 10.1. Ambiente de Pruebas
- Servidor de desarrollo
- Base de datos de pruebas
- Usuarios de prueba (admin, coordinador, repartidor)
- Datos de prueba cargados

### 10.2. Herramientas
- Navegadores: Chrome, Firefox, Safari, Edge
- Dispositivos móviles para pruebas responsivas
- Postman/Insomnia para pruebas de API
- Herramientas de captura de pantalla

---

## 11. Cronograma de Pruebas

| Fase | Duración | Responsable |
|------|----------|-------------|
| Preparación | 2 días | Equipo |
| Pruebas Funcionales | 5 días | Tester 1 |
| Pruebas de Integración | 3 días | Tester 2 |
| Pruebas de Usabilidad | 2 días | Tester 3 |
| Análisis y Reporte | 2 días | Equipo |
| **Total** | **14 días** | |

---

## 12. Plantilla de Caso de Prueba

```markdown
### CP-XXX: [Nombre del Caso de Prueba]

**ID:** CP-XXX
**Tipo:** Funcional / Integración / Usabilidad
**Prioridad:** Alta / Media / Baja
**Caso de Uso Relacionado:** CU-XX

**Precondiciones:**
- Condición 1
- Condición 2

**Datos de Prueba:**
- Dato 1: Valor
- Dato 2: Valor

**Pasos:**
1. Paso 1
2. Paso 2
3. Paso 3

**Resultado Esperado:**
- Resultado 1
- Resultado 2

**Resultado Obtenido:**
[A completar durante ejecución]

**Estado:** ⏳ Pendiente / ✅ Pasó / ❌ Falló
**Observaciones:**
[Notas adicionales]
```

---

## 13. Conclusión

Este plan de pruebas proporciona una guía completa para validar el sistema LogiCo. La ejecución sistemática de estos casos de prueba garantizará la calidad y confiabilidad del software antes de su puesta en producción.

**Próximos Pasos:**
1. Revisar y aprobar plan de pruebas
2. Preparar ambiente de pruebas
3. Ejecutar casos de prueba
4. Documentar resultados
5. Analizar y reportar hallazgos

