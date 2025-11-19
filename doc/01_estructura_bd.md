# Estructura de Base de Datos - LogiCo

## 1. Modelo Conceptual

### Descripción General
El sistema LogiCo gestiona la logística farmacéutica mediante un modelo de datos relacional que permite:
- Gestión de usuarios con diferentes roles (Admin, Coordinador, Repartidor)
- Control de flota de motos
- Seguimiento de órdenes de medicamentos
- Registro de despachos y movimientos
- Generación de reportes

### Entidades Principales

#### 1. Usuario (User - Django Auth)
**Descripción:** Usuario del sistema con credenciales de autenticación.

**Atributos:**
- `id` (PK): Identificador único
- `username`: Nombre de usuario único
- `email`: Correo electrónico
- `first_name`: Nombre
- `last_name`: Apellido
- `password`: Contraseña encriptada
- `is_active`: Estado activo/inactivo
- `date_joined`: Fecha de registro

#### 2. UsuarioProfile
**Descripción:** Perfil extendido del usuario con información específica del negocio.

**Atributos:**
- `id` (PK): Identificador único
- `user_id` (FK): Referencia a User (OneToOne)
- `rut`: RUT del usuario (opcional)
- `telefono`: Número de teléfono
- `rol`: Rol del usuario (admin, coordinador, repartidor)
- `foto`: Foto del perfil (opcional)
- `moto_id` (FK): Referencia a Moto (OneToOne, opcional)
- `estado_turno`: Estado actual (disponible, ocupado, descanso)
- `fecha_inicio_descanso`: Fecha de inicio del descanso
- `fecha_creacion`: Fecha de creación del perfil
- `activo`: Estado activo/inactivo

**Relaciones:**
- **OneToOne** con User
- **OneToOne** con Moto (opcional)
- **OneToMany** con Orden (como responsable)
- **OneToMany** con Despacho
- **OneToMany** con OrdenMovimiento
- **OneToMany** con Ruta

#### 3. Moto
**Descripción:** Vehículo utilizado para el reparto de medicamentos.

**Atributos:**
- `id` (PK): Identificador único
- `patente`: Patente única del vehículo
- `marca`: Marca de la moto
- `modelo`: Modelo de la moto
- `año`: Año de fabricación
- `color`: Color del vehículo
- `cilindrada`: Cilindrada en cc
- `kilometraje`: Kilometraje actual
- `estado`: Estado (disponible, en_uso, mantenimiento, fuera_servicio)
- `fecha_ingreso`: Fecha de ingreso al sistema
- `fecha_ultimo_mantenimiento`: Fecha del último mantenimiento
- `proximo_mantenimiento`: Fecha del próximo mantenimiento
- `observaciones`: Observaciones adicionales
- `activa`: Estado activo/inactivo

**Relaciones:**
- **OneToOne** con UsuarioProfile (repartidor asignado)

#### 4. Orden
**Descripción:** Orden de medicamentos solicitada por un cliente.

**Atributos:**
- `id` (PK): Identificador único
- `cliente`: Nombre del cliente
- `direccion`: Dirección de entrega
- `telefono_cliente`: Teléfono de contacto
- `descripcion`: Descripción adicional
- `prioridad`: Prioridad (alta, media, baja)
- `tipo`: Tipo de orden (receta_detendida, normal)
- `estado_actual`: Estado actual (retiro_receta, traslado, despacho, re_despacho)
- `responsable_id` (FK): Referencia a UsuarioProfile (opcional)
- `fecha_creacion`: Fecha de creación
- `fecha_actualizacion`: Fecha de última actualización

**Relaciones:**
- **ManyToOne** con UsuarioProfile (responsable)
- **OneToMany** con Medicamento
- **OneToMany** con Despacho
- **OneToMany** con OrdenMovimiento
- **ManyToMany** con Ruta

#### 5. Medicamento
**Descripción:** Medicamento incluido en una orden.

**Atributos:**
- `id` (PK): Identificador único
- `orden_id` (FK): Referencia a Orden
- `codigo`: Código del medicamento
- `nombre`: Nombre del medicamento
- `cantidad`: Cantidad solicitada
- `observaciones`: Observaciones adicionales

**Relaciones:**
- **ManyToOne** con Orden

#### 6. Despacho
**Descripción:** Intento de entrega de una orden.

**Atributos:**
- `id` (PK): Identificador único
- `orden_id` (FK): Referencia a Orden
- `numero_despacho`: Número secuencial del despacho (único por orden)
- `repartidor_id` (FK): Referencia a UsuarioProfile
- `estado`: Estado (despacho, re_despacho)
- `resultado`: Resultado (entregado, no_disponible, error)
- `foto_entrega`: Foto de la entrega (opcional)
- `observaciones`: Observaciones del despacho
- `coordenadas_lat`: Latitud GPS
- `coordenadas_lng`: Longitud GPS
- `fecha`: Fecha y hora del despacho

**Relaciones:**
- **ManyToOne** con Orden
- **ManyToOne** con UsuarioProfile (repartidor)
- **OneToMany** con OrdenMovimiento

**Restricciones:**
- `(orden_id, numero_despacho)` debe ser único

#### 7. OrdenMovimiento
**Descripción:** Historial de cambios de estado de una orden (auditoría).

**Atributos:**
- `id` (PK): Identificador único
- `orden_id` (FK): Referencia a Orden
- `estado`: Estado registrado
- `descripcion`: Descripción del movimiento
- `repartidor_id` (FK): Referencia a UsuarioProfile (opcional)
- `despacho_id` (FK): Referencia a Despacho (opcional)
- `timestamp`: Fecha y hora del movimiento

**Relaciones:**
- **ManyToOne** con Orden
- **ManyToOne** con UsuarioProfile (repartidor, opcional)
- **ManyToOne** con Despacho (opcional)

#### 8. Ruta
**Descripción:** Ruta de reparto que agrupa múltiples órdenes.

**Atributos:**
- `id` (PK): Identificador único
- `nombre`: Nombre de la ruta
- `descripcion`: Descripción de la ruta
- `zona`: Zona geográfica
- `vehiculo`: Identificación del vehículo
- `repartidor_id` (FK): Referencia a UsuarioProfile (opcional)
- `activa`: Estado activo/inactivo
- `fecha_creacion`: Fecha de creación

**Relaciones:**
- **ManyToOne** con UsuarioProfile (repartidor, opcional)
- **ManyToMany** con Orden

#### 9. Reporte
**Descripción:** Reporte diario de entregas y estadísticas.

**Atributos:**
- `id` (PK): Identificador único
- `fecha`: Fecha del reporte (única)
- `entregas_totales`: Total de entregas
- `entregas_exitosas`: Entregas exitosas
- `entregas_fallidas`: Entregas fallidas
- `tiempo_promedio`: Tiempo promedio de entrega
- `ingresos_dia`: Ingresos del día
- `observaciones`: Observaciones del reporte
- `fecha_creacion`: Fecha de creación del reporte

**Relaciones:**
- Ninguna (tabla independiente)

---

## 2. Modelo Lógico

### Diagrama de Relaciones

```
User (1) ──────< (1) UsuarioProfile (1) ──────< (1) Moto
                          │
                          │ (1)
                          │
                          ▼ (N)
                        Orden (1) ──────< (N) Medicamento
                          │
                          │ (1)
                          │
                          ▼ (N)
                      Despacho (1) ──────< (N) OrdenMovimiento
                          │
                          │ (N)
                          │
                          ▼ (1)
                    UsuarioProfile

Orden (N) ──────< (M) Ruta (1) ──────< (N) UsuarioProfile
```

### Tablas y Relaciones Detalladas

#### Tabla: auth_user (Django)
- **PK:** id
- **Índices:** username (UNIQUE), email

#### Tabla: core_usuarioprofile
- **PK:** id
- **FK:** user_id → auth_user(id) ON DELETE CASCADE
- **FK:** moto_id → core_moto(id) ON DELETE SET NULL
- **Índices:** user_id (UNIQUE), moto_id (UNIQUE), rol, activo

#### Tabla: core_moto
- **PK:** id
- **Índices:** patente (UNIQUE), estado, activa

#### Tabla: core_orden
- **PK:** id
- **FK:** responsable_id → core_usuarioprofile(id) ON DELETE SET NULL
- **Índices:** responsable_id, estado_actual, prioridad, fecha_creacion

#### Tabla: core_medicamento
- **PK:** id
- **FK:** orden_id → core_orden(id) ON DELETE CASCADE
- **Índices:** orden_id, codigo

#### Tabla: core_despacho
- **PK:** id
- **FK:** orden_id → core_orden(id) ON DELETE CASCADE
- **FK:** repartidor_id → core_usuarioprofile(id) ON DELETE SET NULL
- **Índices:** orden_id, repartidor_id, fecha
- **UNIQUE:** (orden_id, numero_despacho)

#### Tabla: core_ordenmovimiento
- **PK:** id
- **FK:** orden_id → core_orden(id) ON DELETE CASCADE
- **FK:** repartidor_id → core_usuarioprofile(id) ON DELETE SET NULL
- **FK:** despacho_id → core_despacho(id) ON DELETE SET NULL
- **Índices:** orden_id, timestamp, estado

#### Tabla: core_ruta
- **PK:** id
- **FK:** repartidor_id → core_usuarioprofile(id) ON DELETE SET NULL
- **Índices:** repartidor_id, activa, fecha_creacion

#### Tabla: core_ruta_ordenes (ManyToMany)
- **PK:** id
- **FK:** ruta_id → core_ruta(id) ON DELETE CASCADE
- **FK:** orden_id → core_orden(id) ON DELETE CASCADE
- **UNIQUE:** (ruta_id, orden_id)

#### Tabla: core_reporte
- **PK:** id
- **Índices:** fecha (UNIQUE)

---

## 3. Diccionario de Datos

### Tabla: core_usuarioprofile

| Campo | Tipo | Longitud | Null | Default | Descripción |
|-------|------|----------|------|---------|-------------|
| id | INTEGER | - | NO | AUTO | Clave primaria |
| user_id | INTEGER | - | NO | - | FK a auth_user |
| rut | VARCHAR | 12 | YES | NULL | RUT del usuario |
| telefono | VARCHAR | 20 | NO | - | Teléfono de contacto |
| rol | VARCHAR | 20 | NO | 'repartidor' | Rol: admin, coordinador, repartidor |
| foto | VARCHAR | 100 | YES | NULL | Ruta de la foto |
| moto_id | INTEGER | - | YES | NULL | FK a core_moto |
| estado_turno | VARCHAR | 20 | NO | 'disponible' | Estado: disponible, ocupado, descanso |
| fecha_inicio_descanso | TIMESTAMP | - | YES | NULL | Inicio del descanso |
| fecha_creacion | TIMESTAMP | - | NO | NOW() | Fecha de creación |
| activo | BOOLEAN | - | NO | TRUE | Estado activo |

**Índices:**
- PRIMARY KEY: id
- UNIQUE: user_id
- UNIQUE: moto_id
- INDEX: rol
- INDEX: activo
- FOREIGN KEY: user_id → auth_user(id)
- FOREIGN KEY: moto_id → core_moto(id)

### Tabla: core_moto

| Campo | Tipo | Longitud | Null | Default | Descripción |
|-------|------|----------|------|---------|-------------|
| id | INTEGER | - | NO | AUTO | Clave primaria |
| patente | VARCHAR | 10 | NO | - | Patente única |
| marca | VARCHAR | 50 | NO | - | Marca de la moto |
| modelo | VARCHAR | 50 | NO | - | Modelo de la moto |
| año | INTEGER | - | NO | - | Año de fabricación |
| color | VARCHAR | 30 | NO | - | Color del vehículo |
| cilindrada | INTEGER | - | NO | - | Cilindrada en cc |
| kilometraje | INTEGER | - | NO | 0 | Kilometraje actual |
| estado | VARCHAR | 20 | NO | 'disponible' | Estado actual |
| fecha_ingreso | TIMESTAMP | - | NO | NOW() | Fecha de ingreso |
| fecha_ultimo_mantenimiento | DATE | - | YES | NULL | Último mantenimiento |
| proximo_mantenimiento | DATE | - | YES | NULL | Próximo mantenimiento |
| observaciones | TEXT | - | YES | NULL | Observaciones |
| activa | BOOLEAN | - | NO | TRUE | Estado activo |

**Índices:**
- PRIMARY KEY: id
- UNIQUE: patente
- INDEX: estado
- INDEX: activa

### Tabla: core_orden

| Campo | Tipo | Longitud | Null | Default | Descripción |
|-------|------|----------|------|---------|-------------|
| id | INTEGER | - | NO | AUTO | Clave primaria |
| cliente | VARCHAR | 200 | NO | - | Nombre del cliente |
| direccion | TEXT | - | NO | - | Dirección de entrega |
| telefono_cliente | VARCHAR | 20 | NO | - | Teléfono del cliente |
| descripcion | TEXT | - | YES | NULL | Descripción adicional |
| prioridad | VARCHAR | 10 | NO | 'media' | Prioridad: alta, media, baja |
| tipo | VARCHAR | 20 | NO | 'normal' | Tipo: receta_detendida, normal |
| estado_actual | VARCHAR | 20 | NO | 'retiro_receta' | Estado actual |
| responsable_id | INTEGER | - | YES | NULL | FK a UsuarioProfile |
| fecha_creacion | TIMESTAMP | - | NO | NOW() | Fecha de creación |
| fecha_actualizacion | TIMESTAMP | - | NO | NOW() | Fecha de actualización |

**Índices:**
- PRIMARY KEY: id
- INDEX: responsable_id
- INDEX: estado_actual
- INDEX: prioridad
- INDEX: fecha_creacion
- FOREIGN KEY: responsable_id → core_usuarioprofile(id)

### Tabla: core_medicamento

| Campo | Tipo | Longitud | Null | Default | Descripción |
|-------|------|----------|------|---------|-------------|
| id | INTEGER | - | NO | AUTO | Clave primaria |
| orden_id | INTEGER | - | NO | - | FK a core_orden |
| codigo | VARCHAR | 50 | NO | - | Código del medicamento |
| nombre | VARCHAR | 200 | NO | - | Nombre del medicamento |
| cantidad | INTEGER | - | NO | - | Cantidad (>= 1) |
| observaciones | TEXT | - | YES | NULL | Observaciones |

**Índices:**
- PRIMARY KEY: id
- INDEX: orden_id
- INDEX: codigo
- FOREIGN KEY: orden_id → core_orden(id) ON DELETE CASCADE

### Tabla: core_despacho

| Campo | Tipo | Longitud | Null | Default | Descripción |
|-------|------|----------|------|---------|-------------|
| id | INTEGER | - | NO | AUTO | Clave primaria |
| orden_id | INTEGER | - | NO | - | FK a core_orden |
| numero_despacho | INTEGER | - | NO | 1 | Número secuencial |
| repartidor_id | INTEGER | - | YES | NULL | FK a UsuarioProfile |
| estado | VARCHAR | 20 | NO | 'despacho' | Estado: despacho, re_despacho |
| resultado | VARCHAR | 20 | YES | NULL | Resultado: entregado, no_disponible, error |
| foto_entrega | VARCHAR | 100 | YES | NULL | Ruta de la foto |
| observaciones | TEXT | - | YES | NULL | Observaciones |
| coordenadas_lat | DECIMAL | 9,6 | YES | NULL | Latitud GPS |
| coordenadas_lng | DECIMAL | 9,6 | YES | NULL | Longitud GPS |
| fecha | TIMESTAMP | - | NO | NOW() | Fecha del despacho |

**Índices:**
- PRIMARY KEY: id
- UNIQUE: (orden_id, numero_despacho)
- INDEX: orden_id
- INDEX: repartidor_id
- INDEX: fecha
- FOREIGN KEY: orden_id → core_orden(id) ON DELETE CASCADE
- FOREIGN KEY: repartidor_id → core_usuarioprofile(id) ON DELETE SET NULL

### Tabla: core_ordenmovimiento

| Campo | Tipo | Longitud | Null | Default | Descripción |
|-------|------|----------|------|---------|-------------|
| id | INTEGER | - | NO | AUTO | Clave primaria |
| orden_id | INTEGER | - | NO | - | FK a core_orden |
| estado | VARCHAR | 20 | NO | - | Estado registrado |
| descripcion | TEXT | - | YES | NULL | Descripción del movimiento |
| repartidor_id | INTEGER | - | YES | NULL | FK a UsuarioProfile |
| despacho_id | INTEGER | - | YES | NULL | FK a core_despacho |
| timestamp | TIMESTAMP | - | NO | NOW() | Fecha y hora |

**Índices:**
- PRIMARY KEY: id
- INDEX: orden_id
- INDEX: timestamp
- INDEX: estado
- FOREIGN KEY: orden_id → core_orden(id) ON DELETE CASCADE
- FOREIGN KEY: repartidor_id → core_usuarioprofile(id) ON DELETE SET NULL
- FOREIGN KEY: despacho_id → core_despacho(id) ON DELETE SET NULL

### Tabla: core_ruta

| Campo | Tipo | Longitud | Null | Default | Descripción |
|-------|------|----------|------|---------|-------------|
| id | INTEGER | - | NO | AUTO | Clave primaria |
| nombre | VARCHAR | 200 | NO | - | Nombre de la ruta |
| descripcion | TEXT | - | YES | NULL | Descripción |
| zona | VARCHAR | 100 | NO | - | Zona geográfica |
| vehiculo | VARCHAR | 100 | YES | NULL | Identificación del vehículo |
| repartidor_id | INTEGER | - | YES | NULL | FK a UsuarioProfile |
| activa | BOOLEAN | - | NO | TRUE | Estado activo |
| fecha_creacion | TIMESTAMP | - | NO | NOW() | Fecha de creación |

**Índices:**
- PRIMARY KEY: id
- INDEX: repartidor_id
- INDEX: activa
- INDEX: fecha_creacion
- FOREIGN KEY: repartidor_id → core_usuarioprofile(id) ON DELETE SET NULL

### Tabla: core_ruta_ordenes (ManyToMany)

| Campo | Tipo | Longitud | Null | Default | Descripción |
|-------|------|----------|------|---------|-------------|
| id | INTEGER | - | NO | AUTO | Clave primaria |
| ruta_id | INTEGER | - | NO | - | FK a core_ruta |
| orden_id | INTEGER | - | NO | - | FK a core_orden |

**Índices:**
- PRIMARY KEY: id
- UNIQUE: (ruta_id, orden_id)
- FOREIGN KEY: ruta_id → core_ruta(id) ON DELETE CASCADE
- FOREIGN KEY: orden_id → core_orden(id) ON DELETE CASCADE

### Tabla: core_reporte

| Campo | Tipo | Longitud | Null | Default | Descripción |
|-------|------|----------|------|---------|-------------|
| id | INTEGER | - | NO | AUTO | Clave primaria |
| fecha | DATE | - | NO | - | Fecha del reporte (única) |
| entregas_totales | INTEGER | - | NO | 0 | Total de entregas |
| entregas_exitosas | INTEGER | - | NO | 0 | Entregas exitosas |
| entregas_fallidas | INTEGER | - | NO | 0 | Entregas fallidas |
| tiempo_promedio | INTERVAL | - | YES | NULL | Tiempo promedio |
| ingresos_dia | DECIMAL | 10,2 | NO | 0.00 | Ingresos del día |
| observaciones | TEXT | - | YES | NULL | Observaciones |
| fecha_creacion | TIMESTAMP | - | NO | NOW() | Fecha de creación |

**Índices:**
- PRIMARY KEY: id
- UNIQUE: fecha

---

## 4. Normalización

### Nivel de Normalización: 3NF (Tercera Forma Normal)

**Justificación:**
- ✅ **1NF:** Todos los atributos son atómicos
- ✅ **2NF:** No hay dependencias parciales (todas las claves primarias son simples)
- ✅ **3NF:** No hay dependencias transitivas

**Ejemplo de Normalización:**

**ANTES (No Normalizado):**
```
Orden (
    id, cliente, direccion, telefono_cliente,
    medicamento1_codigo, medicamento1_nombre, medicamento1_cantidad,
    medicamento2_codigo, medicamento2_nombre, medicamento2_cantidad,
    ...
)
```

**DESPUÉS (Normalizado):**
```
Orden (
    id, cliente, direccion, telefono_cliente, ...
)

Medicamento (
    id, orden_id, codigo, nombre, cantidad
)
```

### Optimizaciones Aplicadas

1. **Índices en Claves Foráneas:** Mejoran el rendimiento de JOINs
2. **Índices en Campos de Búsqueda Frecuente:** estado, fecha_creacion, rol
3. **Campos Únicos:** Evitan duplicados (patente, username, fecha en reporte)
4. **Cascadas Apropiadas:** Mantienen integridad referencial
5. **Campos Calculados:** Propiedades en lugar de campos redundantes (tasa_exito en Reporte)

---

## 5. Integridad Referencial

### Restricciones de Integridad

1. **CASCADE:** Eliminar usuario elimina su perfil
2. **SET NULL:** Eliminar moto no elimina el perfil, solo desasigna
3. **CASCADE:** Eliminar orden elimina medicamentos y movimientos
4. **SET NULL:** Eliminar repartidor no elimina despachos, solo desasigna

### Reglas de Negocio Implementadas

1. Un usuario solo puede tener un perfil
2. Una moto solo puede estar asignada a un repartidor
3. Un repartidor solo puede tener una moto asignada
4. Una orden puede tener múltiples despachos (reintentos)
5. Cada despacho de una orden tiene un número secuencial único
6. Los movimientos de orden son inmutables (solo lectura después de creados)

---

## 6. Consideraciones de Rendimiento

### Índices Estratégicos

1. **core_orden:** fecha_creacion, estado_actual, responsable_id
2. **core_despacho:** fecha, orden_id, repartidor_id
3. **core_usuarioprofile:** rol, activo
4. **core_moto:** estado, activa

### Consultas Optimizadas

- Uso de `select_related()` para JOINs eficientes
- Uso de `prefetch_related()` para relaciones ManyToMany
- Paginación en listados (20 elementos por página)
- Filtros en base de datos en lugar de Python

---

## 7. Diagrama ER (Entidad-Relación)

```
┌─────────────┐
│    User     │
│  (Django)   │
└──────┬──────┘
       │ 1
       │
       │ 1
┌──────▼──────────────┐
│  UsuarioProfile     │
│  - rut              │
│  - telefono         │
│  - rol              │
│  - estado_turno     │
└───┬────────────┬────┘
    │ 1          │ 1
    │            │
    │ N          │ 1
┌───▼────┐  ┌───▼──────┐
│ Orden  │  │   Moto   │
│        │  │          │
└───┬────┘  └──────────┘
    │ 1
    │
    │ N
┌───▼──────────┐
│ Medicamento  │
└──────────────┘

┌──────────────┐
│   Orden      │
└───┬──────────┘
    │ 1
    │
    │ N
┌───▼──────────┐      ┌──────────────┐
│  Despacho    │──────│ OrdenMovim.  │
└───┬──────────┘ 1 N  └──────────────┘
    │ N
    │
    │ 1
┌───▼──────────────┐
│ UsuarioProfile   │
└──────────────────┘

┌──────────────┐      ┌──────────────┐
│    Ruta      │──────│    Orden     │
└───┬──────────┘ M N  └──────────────┘
    │ 1
    │
    │ N
┌───▼──────────────┐
│ UsuarioProfile   │
└──────────────────┘
```

---

## 8. Conclusión

La estructura de base de datos está diseñada siguiendo las mejores prácticas:
- ✅ Normalización 3NF
- ✅ Integridad referencial
- ✅ Índices optimizados
- ✅ Relaciones bien definidas
- ✅ Sin redundancias
- ✅ Escalable y mantenible

