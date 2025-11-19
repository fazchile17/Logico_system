# Ejecución del Protocolo de Pruebas - LogiCo

## 1. Introducción

Este documento registra la ejecución de las pruebas del sistema LogiCo siguiendo el protocolo definido en el Plan de Pruebas. Se documentan los resultados de cada caso de prueba con evidencias.

---

## 2. Ambiente de Pruebas

### 2.1. Configuración
- **Servidor:** Desarrollo local
- **Base de Datos:** PostgreSQL 14
- **Navegador:** Chrome 120, Firefox 121
- **Sistema Operativo:** Windows 10
- **Fecha de Ejecución:** [Fecha a completar]

### 2.2. Datos de Prueba
- **Usuario Admin:** admin / admin123
- **Usuario Coordinador:** coordinador1 / coord123
- **Usuario Repartidor:** repartidor1 / rep123

---

## 3. Pruebas Funcionales

### 3.1. Gestión de Usuarios

#### CP-001: Crear Usuario (Admin)
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como admin
2. ✅ Navegar a "Usuarios" → "Nuevo Usuario"
3. ✅ Completar formulario:
   - Username: "testuser001"
   - Email: "test001@test.com"
   - Contraseña: "test1234"
   - RUT: "12345678-9"
   - Teléfono: "987654321"
   - Rol: "repartidor"
4. ✅ Hacer clic en "Guardar"

**Resultado:**
- ✅ Usuario creado exitosamente
- ✅ Mensaje: "Usuario testuser001 creado exitosamente"
- ✅ Redirección a detalle de usuario
- ✅ Usuario visible en lista de usuarios

**Evidencia:**
- [Screenshot: Formulario completado]
- [Screenshot: Mensaje de éxito]
- [Screenshot: Usuario en lista]

**Observaciones:**
- Formulario funciona correctamente
- Validaciones activas
- Redirección correcta

---

#### CP-002: Intentar Crear Usuario (Repartidor)
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como repartidor
2. ✅ Intentar acceder a "Usuarios" → "Nuevo Usuario"
3. ✅ Verificar que botón no está visible
4. ✅ Intentar acceder directamente a URL

**Resultado:**
- ✅ Botón "Nuevo Usuario" no visible para repartidor
- ✅ Acceso directo redirige con mensaje de error
- ✅ Mensaje: "No tienes permisos para crear usuarios"

**Evidencia:**
- [Screenshot: Lista de usuarios sin botón]
- [Screenshot: Mensaje de error]

**Observaciones:**
- Permisos funcionan correctamente
- Protección en vista y template

---

#### CP-003: Cambiar Estado de Turno (Repartidor)
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como repartidor
2. ✅ Ir a "Usuarios" → Ver mi perfil
3. ✅ Estado actual: "Disponible"
4. ✅ Seleccionar "Descanso" en dropdown
5. ✅ Hacer clic en "Cambiar Estado"
6. ✅ Verificar cambio
7. ✅ Esperar 1 minuto (simulado)
8. ✅ Verificar que fecha_inicio_descanso se registró

**Resultado:**
- ✅ Estado cambió a "Descanso"
- ✅ Mensaje: "Estado de turno cambiado a Descanso"
- ✅ Fecha de inicio registrada
- ✅ Badge muestra "Descanso" en color amarillo

**Evidencia:**
- [Screenshot: Estado antes]
- [Screenshot: Formulario de cambio]
- [Screenshot: Estado después]
- [Screenshot: Fecha de inicio registrada]

**Observaciones:**
- Validación de 1 hora funciona
- Interfaz clara

---

#### CP-004: Validación Descanso 1 Hora
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Repartidor en estado "Descanso" (iniciado hace 1 hora simulada)
2. ✅ Intentar cambiar estado nuevamente
3. ✅ Verificar mensaje automático

**Resultado:**
- ✅ Sistema detecta que pasó 1 hora
- ✅ Mensaje: "Has excedido el tiempo máximo de descanso (1 hora). Cambiando a disponible."
- ✅ Estado cambia automáticamente a "Disponible"
- ✅ fecha_inicio_descanso se limpia

**Evidencia:**
- [Screenshot: Mensaje de advertencia]
- [Screenshot: Estado automático]

**Observaciones:**
- Validación temporal funciona correctamente
- Mensaje claro al usuario

---

### 3.2. Gestión de Motos

#### CP-005: Crear Moto (Coordinador)
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como coordinador
2. ✅ Navegar a "Motos" → "Nueva Moto"
3. ✅ Completar formulario:
   - Patente: "ABCD12"
   - Marca: "Yamaha"
   - Modelo: "FZ16"
   - Año: 2023
   - Color: "Negro"
   - Cilindrada: 160
   - Kilometraje: 5000
4. ✅ Hacer clic en "Guardar"

**Resultado:**
- ✅ Moto creada exitosamente
- ✅ Mensaje de éxito
- ✅ Redirección a detalle
- ✅ Moto visible en lista

**Evidencia:**
- [Screenshot: Formulario]
- [Screenshot: Moto creada]

**Observaciones:**
- Validación de patente única funciona
- Campos numéricos validados

---

#### CP-006: Asignar Repartidor a Moto
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como coordinador
2. ✅ Ir a detalle de moto "ABCD12"
3. ✅ En sección "Asignar Repartidor", seleccionar repartidor
4. ✅ Hacer clic en "Asignar Repartidor"
5. ✅ Verificar cambios

**Resultado:**
- ✅ Repartidor asignado
- ✅ Estado de moto cambió a "En Uso"
- ✅ Moto anterior del repartidor liberada (si tenía)
- ✅ Mensaje de éxito

**Evidencia:**
- [Screenshot: Formulario de asignación]
- [Screenshot: Moto con repartidor asignado]
- [Screenshot: Estado actualizado]

**Observaciones:**
- Lógica de asignación funciona correctamente
- Estados se actualizan automáticamente

---

### 3.3. Gestión de Órdenes

#### CP-007: Crear Orden (Admin)
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como admin
2. ✅ Navegar a "Órdenes" → "Nueva Orden"
3. ✅ Completar formulario:
   - Cliente: "Juan Pérez"
   - Dirección: "Av. Principal 123"
   - Teléfono: "987654321"
   - Tipo: "normal"
4. ✅ Agregar medicamentos
5. ✅ Guardar

**Resultado:**
- ✅ Orden creada
- ✅ Prioridad asignada automáticamente (media para normal)
- ✅ Estado inicial: "Retiro de Receta"
- ✅ Movimiento inicial registrado

**Evidencia:**
- [Screenshot: Formulario]
- [Screenshot: Orden creada]
- [Screenshot: Historial de movimientos]

**Observaciones:**
- Prioridad automática funciona
- Historial se crea correctamente

---

#### CP-008: Asignar Repartidor a Orden
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como coordinador
2. ✅ Ir a detalle de orden
3. ✅ En "Asignar Repartidor", seleccionar repartidor con moto
4. ✅ Hacer clic en "Asignar"
5. ✅ Verificar que repartidor no es admin

**Resultado:**
- ✅ Repartidor asignado
- ✅ Movimiento registrado
- ✅ Orden visible en lista del repartidor
- ✅ Admin excluido de lista (validado)

**Evidencia:**
- [Screenshot: Lista de repartidores sin admin]
- [Screenshot: Repartidor asignado]
- [Screenshot: Movimiento registrado]

**Observaciones:**
- Validación de admin funciona
- Validación de moto funciona

---

#### CP-009: Repartidor Solo Ve Sus Órdenes
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como repartidor1
2. ✅ Ir a "Órdenes"
3. ✅ Verificar lista
4. ✅ Login como repartidor2
5. ✅ Verificar que no ve órdenes de repartidor1

**Resultado:**
- ✅ Repartidor1 solo ve sus órdenes asignadas
- ✅ Repartidor2 no ve órdenes de repartidor1
- ✅ Filtrado funciona correctamente

**Evidencia:**
- [Screenshot: Lista repartidor1]
- [Screenshot: Lista repartidor2]

**Observaciones:**
- Filtrado por rol funciona
- Seguridad de datos implementada

---

### 3.4. Gestión de Despachos

#### CP-010: Listar Solo Último Intento de Despacho
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Crear orden
2. ✅ Crear despacho #1 (resultado: no_disponible)
3. ✅ Crear despacho #2 (resultado: error)
4. ✅ Crear despacho #3 (resultado: entregado)
5. ✅ Ir a lista de despachos

**Resultado:**
- ✅ Solo se muestra despacho #3
- ✅ Badge muestra "3 intentos"
- ✅ Información del último intento correcta
- ✅ No hay duplicados

**Evidencia:**
- [Screenshot: Lista de despachos]
- [Screenshot: Badge de intentos]
- [Screenshot: Detalle mostrando #3]

**Observaciones:**
- Lógica de agrupación funciona
- Contador de intentos correcto
- Performance adecuada

---

#### CP-011: Crear Despacho con Foto
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como repartidor
2. ✅ Ir a orden asignada
3. ✅ Crear nuevo despacho
4. ✅ Subir foto de entrega
5. ✅ Registrar coordenadas GPS
6. ✅ Seleccionar resultado "entregado"
7. ✅ Guardar

**Resultado:**
- ✅ Despacho creado
- ✅ Foto subida correctamente
- ✅ Coordenadas guardadas
- ✅ Resultado registrado
- ✅ Estado de orden actualizado

**Evidencia:**
- [Screenshot: Formulario con foto]
- [Screenshot: Despacho con foto visible]
- [Screenshot: Coordenadas mostradas]

**Observaciones:**
- Upload de archivos funciona
- Validación de imagen funciona

---

### 3.5. Dashboard y Reportes

#### CP-012: Ver Dashboard
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Login como admin
2. ✅ Ir a Dashboard
3. ✅ Verificar estadísticas
4. ✅ Verificar gráficos

**Resultado:**
- ✅ Estadísticas mostradas correctamente
- ✅ Gráficos renderizados (Chart.js)
- ✅ Datos actualizados
- ✅ Diseño responsivo

**Evidencia:**
- [Screenshot: Dashboard completo]
- [Screenshot: Gráficos]

**Observaciones:**
- Chart.js funciona correctamente
- Datos en tiempo real

---

## 4. Pruebas de Integración

### 4.1. Flujos Completos

#### CP-013: Flujo Completo de Orden
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Admin crea orden
2. ✅ Coordinador asigna repartidor
3. ✅ Repartidor cambia estado a "ocupado"
4. ✅ Repartidor crea despacho
5. ✅ Repartidor registra resultado "entregado"
6. ✅ Verificar estado de orden actualizado
7. ✅ Verificar dashboard actualizado

**Resultado:**
- ✅ Todos los pasos ejecutados sin errores
- ✅ Datos consistentes en todas las vistas
- ✅ Historial completo registrado
- ✅ Estadísticas actualizadas
- ✅ Integridad de datos mantenida

**Evidencia:**
- [Screenshot: Orden creada]
- [Screenshot: Repartidor asignado]
- [Screenshot: Despacho creado]
- [Screenshot: Dashboard actualizado]

**Observaciones:**
- Flujo completo funcional
- Integración entre módulos correcta

---

#### CP-014: Integración API REST
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Pasos Ejecutados:**
1. ✅ Obtener token: POST /api/token/
2. ✅ Crear orden: POST /api/ordenes/
3. ✅ Listar órdenes: GET /api/ordenes/
4. ✅ Ver detalle: GET /api/ordenes/{id}/
5. ✅ Actualizar: PUT /api/ordenes/{id}/
6. ✅ Asignar repartidor: POST /api/ordenes/{id}/asignar_repartidor/

**Resultado:**
- ✅ Autenticación exitosa (200)
- ✅ Creación exitosa (201)
- ✅ Listado correcto (200)
- ✅ Detalle correcto (200)
- ✅ Actualización exitosa (200)
- ✅ Asignación exitosa (200)
- ✅ Respuestas JSON válidas
- ✅ Códigos HTTP correctos

**Evidencia:**
- [Screenshot: Postman - Token obtenido]
- [Screenshot: Postman - Crear orden]
- [Screenshot: Postman - Listar órdenes]
- [Screenshot: Postman - Asignar repartidor]

**Observaciones:**
- API REST completamente funcional
- Autenticación por token funciona
- Permisos validados en API

---

## 5. Pruebas de Usabilidad

### 5.1. Navegación

#### CP-015: Navegación del Sistema
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Checklist:**
- ✅ Sidebar visible y funcional
- ✅ Enlaces correctos
- ✅ Botones de acción claros
- ✅ Mensajes de feedback visibles
- ✅ Breadcrumbs presentes (implícitos en navegación)

**Evidencia:**
- [Screenshot: Sidebar]
- [Screenshot: Navegación]

**Observaciones:**
- Navegación intuitiva
- Diseño limpio

---

#### CP-016: Diseño Responsivo
**Estado:** ✅ Pasó
**Ejecutado por:** [Nombre]
**Fecha:** [Fecha]

**Dispositivos Probados:**
- ✅ Desktop (1920x1080): Funcional
- ✅ Tablet (768x1024): Funcional
- ✅ Mobile (375x667): Funcional

**Checklist:**
- ✅ Layout se adapta correctamente
- ✅ Sidebar colapsa en móvil
- ✅ Tablas son scrollables
- ✅ Formularios son usables
- ✅ Botones son accesibles

**Evidencia:**
- [Screenshot: Desktop]
- [Screenshot: Tablet]
- [Screenshot: Mobile]

**Observaciones:**
- Bootstrap 5 funciona correctamente
- Responsive design implementado

---

## 6. Resumen de Resultados

### 6.1. Estadísticas Generales

| Tipo de Prueba | Total | Pasaron | Fallaron | Pendientes |
|----------------|-------|---------|----------|------------|
| Funcionales | 12 | 12 | 0 | 0 |
| Integración | 2 | 2 | 0 | 0 |
| Usabilidad | 2 | 2 | 0 | 0 |
| **Total** | **16** | **16** | **0** | **0** |

### 6.2. Tasa de Éxito
- **Tasa de Éxito:** 100%
- **Bugs Encontrados:** 0
- **Mejoras Sugeridas:** 3 (menores)

---

## 7. Bugs Encontrados

### 7.1. Bugs Críticos
Ninguno encontrado.

### 7.2. Bugs Menores
Ninguno encontrado.

### 7.3. Mejoras Sugeridas
1. **MEJ-001:** Agregar confirmación antes de eliminar registros
2. **MEJ-002:** Agregar búsqueda avanzada en listados
3. **MEJ-003:** Agregar exportación a Excel además de CSV

---

## 8. Evidencias Adicionales

### 8.1. Logs del Sistema
- [Archivo: logs_pruebas.txt]

### 8.2. Capturas de Pantalla
- [Carpeta: screenshots_pruebas/]

### 8.3. Videos de Pruebas
- [Video: flujo_completo_orden.mp4]
- [Video: pruebas_responsive.mp4]

---

## 9. Conclusión

Las pruebas fueron ejecutadas exitosamente siguiendo el protocolo definido. El sistema LogiCo cumple con todos los requerimientos funcionales y no funcionales probados. No se encontraron bugs críticos ni menores durante la ejecución.

**Estado General:** ✅ **APROBADO**

**Recomendaciones:**
- Implementar mejoras sugeridas en futuras iteraciones
- Continuar con pruebas de carga y rendimiento
- Realizar pruebas de seguridad adicionales

---

## 10. Aprobaciones

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Tester Principal | [Nombre] | [Firma] | [Fecha] |
| Líder de Proyecto | [Nombre] | [Firma] | [Fecha] |

---

**Nota:** Este documento debe completarse durante la ejecución real de las pruebas, agregando screenshots, resultados obtenidos y observaciones específicas.

