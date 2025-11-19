# Normalización y Scripts SQL - LogiCo

## 1. Análisis de Normalización

### Nivel de Normalización: 3NF (Tercera Forma Normal)

#### Primera Forma Normal (1NF)
✅ **Cumplida:** Todos los atributos son atómicos (no hay campos multivaluados)

**Ejemplo:**
- ❌ No permitido: `medicamentos: "Paracetamol, Ibuprofeno, Aspirina"`
- ✅ Correcto: Tabla separada `Medicamento` con una fila por medicamento

#### Segunda Forma Normal (2NF)
✅ **Cumplida:** No hay dependencias parciales (todas las claves primarias son simples)

**Justificación:**
- Todas las tablas tienen claves primarias simples (id)
- No hay claves compuestas que generen dependencias parciales

#### Tercera Forma Normal (3NF)
✅ **Cumplida:** No hay dependencias transitivas

**Ejemplo de Eliminación de Dependencia Transitiva:**

**ANTES (No Normalizado):**
```
Orden (
    id,
    cliente,
    direccion,
    ciudad,          -- Depende de direccion
    region,          -- Depende de ciudad
    codigo_postal    -- Depende de direccion
)
```

**DESPUÉS (Normalizado):**
```
Orden (
    id,
    cliente,
    direccion        -- Atributo atómico, sin dependencias transitivas
)
```

### Optimizaciones Aplicadas

1. **Eliminación de Redundancias:**
   - No se almacena `tasa_exito` en Reporte (se calcula)
   - No se almacena `repartidor_asignado` en Moto (se obtiene por relación inversa)

2. **Separación de Responsabilidades:**
   - User (autenticación) separado de UsuarioProfile (datos de negocio)
   - OrdenMovimiento (auditoría) separado de Orden (datos actuales)

3. **Índices Estratégicos:**
   - Índices en claves foráneas para JOINs eficientes
   - Índices en campos de búsqueda frecuente

---

## 2. Scripts SQL

### 2.1. Script de Eliminación de Foreign Keys

```sql
-- Script: drop_foreign_keys.sql
-- Descripción: Elimina todas las claves foráneas de la base de datos

-- Eliminar FK de core_usuarioprofile
ALTER TABLE core_usuarioprofile 
DROP CONSTRAINT IF EXISTS core_usuarioprofile_user_id_fkey;

ALTER TABLE core_usuarioprofile 
DROP CONSTRAINT IF EXISTS core_usuarioprofile_moto_id_fkey;

-- Eliminar FK de core_orden
ALTER TABLE core_orden 
DROP CONSTRAINT IF EXISTS core_orden_responsable_id_fkey;

-- Eliminar FK de core_medicamento
ALTER TABLE core_medicamento 
DROP CONSTRAINT IF EXISTS core_medicamento_orden_id_fkey;

-- Eliminar FK de core_despacho
ALTER TABLE core_despacho 
DROP CONSTRAINT IF EXISTS core_despacho_orden_id_fkey;

ALTER TABLE core_despacho 
DROP CONSTRAINT IF EXISTS core_despacho_repartidor_id_fkey;

-- Eliminar FK de core_ordenmovimiento
ALTER TABLE core_ordenmovimiento 
DROP CONSTRAINT IF EXISTS core_ordenmovimiento_orden_id_fkey;

ALTER TABLE core_ordenmovimiento 
DROP CONSTRAINT IF EXISTS core_ordenmovimiento_repartidor_id_fkey;

ALTER TABLE core_ordenmovimiento 
DROP CONSTRAINT IF EXISTS core_ordenmovimiento_despacho_id_fkey;

-- Eliminar FK de core_ruta
ALTER TABLE core_ruta 
DROP CONSTRAINT IF EXISTS core_ruta_repartidor_id_fkey;

-- Eliminar FK de core_ruta_ordenes (ManyToMany)
ALTER TABLE core_ruta_ordenes 
DROP CONSTRAINT IF EXISTS core_ruta_ordenes_ruta_id_fkey;

ALTER TABLE core_ruta_ordenes 
DROP CONSTRAINT IF EXISTS core_ruta_ordenes_orden_id_fkey;
```

### 2.2. Script de Eliminación de Tablas

```sql
-- Script: drop_tables.sql
-- Descripción: Elimina todas las tablas en orden correcto (dependencias primero)

-- Eliminar tablas ManyToMany primero
DROP TABLE IF EXISTS core_ruta_ordenes CASCADE;

-- Eliminar tablas dependientes
DROP TABLE IF EXISTS core_ordenmovimiento CASCADE;
DROP TABLE IF EXISTS core_medicamento CASCADE;
DROP TABLE IF EXISTS core_despacho CASCADE;
DROP TABLE IF EXISTS core_ruta CASCADE;
DROP TABLE IF EXISTS core_reporte CASCADE;
DROP TABLE IF EXISTS core_orden CASCADE;
DROP TABLE IF EXISTS core_usuarioprofile CASCADE;
DROP TABLE IF EXISTS core_moto CASCADE;

-- Nota: auth_user es manejado por Django, no se elimina manualmente
```

### 2.3. Script de Creación de Tablas

```sql
-- Script: create_tables.sql
-- Descripción: Crea todas las tablas de la base de datos

-- Tabla: core_moto
CREATE TABLE core_moto (
    id SERIAL PRIMARY KEY,
    patente VARCHAR(10) NOT NULL UNIQUE,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INTEGER NOT NULL CHECK (año >= 1900),
    color VARCHAR(30) NOT NULL,
    cilindrada INTEGER NOT NULL CHECK (cilindrada >= 0),
    kilometraje INTEGER NOT NULL DEFAULT 0 CHECK (kilometraje >= 0),
    estado VARCHAR(20) NOT NULL DEFAULT 'disponible' 
        CHECK (estado IN ('disponible', 'en_uso', 'mantenimiento', 'fuera_servicio')),
    fecha_ingreso TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_ultimo_mantenimiento DATE,
    proximo_mantenimiento DATE,
    observaciones TEXT,
    activa BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabla: core_usuarioprofile
CREATE TABLE core_usuarioprofile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    rut VARCHAR(12),
    telefono VARCHAR(20) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'repartidor' 
        CHECK (rol IN ('admin', 'coordinador', 'repartidor')),
    foto VARCHAR(100),
    moto_id INTEGER UNIQUE,
    estado_turno VARCHAR(20) NOT NULL DEFAULT 'disponible' 
        CHECK (estado_turno IN ('disponible', 'ocupado', 'descanso')),
    fecha_inicio_descanso TIMESTAMP,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabla: core_orden
CREATE TABLE core_orden (
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(200) NOT NULL,
    direccion TEXT NOT NULL,
    telefono_cliente VARCHAR(20) NOT NULL,
    descripcion TEXT,
    prioridad VARCHAR(10) NOT NULL DEFAULT 'media' 
        CHECK (prioridad IN ('alta', 'media', 'baja')),
    tipo VARCHAR(20) NOT NULL DEFAULT 'normal' 
        CHECK (tipo IN ('receta_detendida', 'normal')),
    estado_actual VARCHAR(20) NOT NULL DEFAULT 'retiro_receta' 
        CHECK (estado_actual IN ('retiro_receta', 'traslado', 'despacho', 're_despacho')),
    responsable_id INTEGER,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: core_medicamento
CREATE TABLE core_medicamento (
    id SERIAL PRIMARY KEY,
    orden_id INTEGER NOT NULL,
    codigo VARCHAR(50) NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 1),
    observaciones TEXT
);

-- Tabla: core_despacho
CREATE TABLE core_despacho (
    id SERIAL PRIMARY KEY,
    orden_id INTEGER NOT NULL,
    numero_despacho INTEGER NOT NULL DEFAULT 1,
    repartidor_id INTEGER,
    estado VARCHAR(20) NOT NULL DEFAULT 'despacho' 
        CHECK (estado IN ('despacho', 're_despacho')),
    resultado VARCHAR(20) 
        CHECK (resultado IN ('entregado', 'no_disponible', 'error')),
    foto_entrega VARCHAR(100),
    observaciones TEXT,
    coordenadas_lat DECIMAL(9, 6),
    coordenadas_lng DECIMAL(9, 6),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(orden_id, numero_despacho)
);

-- Tabla: core_ordenmovimiento
CREATE TABLE core_ordenmovimiento (
    id SERIAL PRIMARY KEY,
    orden_id INTEGER NOT NULL,
    estado VARCHAR(20) NOT NULL 
        CHECK (estado IN ('retiro_receta', 'traslado', 'despacho', 're_despacho')),
    descripcion TEXT,
    repartidor_id INTEGER,
    despacho_id INTEGER,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: core_ruta
CREATE TABLE core_ruta (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    zona VARCHAR(100) NOT NULL,
    vehiculo VARCHAR(100),
    repartidor_id INTEGER,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: core_ruta_ordenes (ManyToMany)
CREATE TABLE core_ruta_ordenes (
    id SERIAL PRIMARY KEY,
    ruta_id INTEGER NOT NULL,
    orden_id INTEGER NOT NULL,
    UNIQUE(ruta_id, orden_id)
);

-- Tabla: core_reporte
CREATE TABLE core_reporte (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    entregas_totales INTEGER NOT NULL DEFAULT 0 CHECK (entregas_totales >= 0),
    entregas_exitosas INTEGER NOT NULL DEFAULT 0 CHECK (entregas_exitosas >= 0),
    entregas_fallidas INTEGER NOT NULL DEFAULT 0 CHECK (entregas_fallidas >= 0),
    tiempo_promedio INTERVAL,
    ingresos_dia DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (ingresos_dia >= 0),
    observaciones TEXT,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### 2.4. Script de Creación de Primary Keys

```sql
-- Script: create_primary_keys.sql
-- Descripción: Define las claves primarias (ya incluidas en CREATE TABLE, pero documentadas aquí)

-- Las claves primarias ya están definidas en CREATE TABLE con SERIAL PRIMARY KEY
-- Este script es solo para documentación

-- core_moto: id (PRIMARY KEY)
-- core_usuarioprofile: id (PRIMARY KEY)
-- core_orden: id (PRIMARY KEY)
-- core_medicamento: id (PRIMARY KEY)
-- core_despacho: id (PRIMARY KEY)
-- core_ordenmovimiento: id (PRIMARY KEY)
-- core_ruta: id (PRIMARY KEY)
-- core_ruta_ordenes: id (PRIMARY KEY)
-- core_reporte: id (PRIMARY KEY)
```

### 2.5. Script de Creación de Foreign Keys

```sql
-- Script: create_foreign_keys.sql
-- Descripción: Crea todas las claves foráneas con sus restricciones

-- Foreign Keys de core_usuarioprofile
ALTER TABLE core_usuarioprofile
ADD CONSTRAINT core_usuarioprofile_user_id_fkey 
FOREIGN KEY (user_id) REFERENCES auth_user(id) 
ON DELETE CASCADE;

ALTER TABLE core_usuarioprofile
ADD CONSTRAINT core_usuarioprofile_moto_id_fkey 
FOREIGN KEY (moto_id) REFERENCES core_moto(id) 
ON DELETE SET NULL;

-- Foreign Keys de core_orden
ALTER TABLE core_orden
ADD CONSTRAINT core_orden_responsable_id_fkey 
FOREIGN KEY (responsable_id) REFERENCES core_usuarioprofile(id) 
ON DELETE SET NULL;

-- Foreign Keys de core_medicamento
ALTER TABLE core_medicamento
ADD CONSTRAINT core_medicamento_orden_id_fkey 
FOREIGN KEY (orden_id) REFERENCES core_orden(id) 
ON DELETE CASCADE;

-- Foreign Keys de core_despacho
ALTER TABLE core_despacho
ADD CONSTRAINT core_despacho_orden_id_fkey 
FOREIGN KEY (orden_id) REFERENCES core_orden(id) 
ON DELETE CASCADE;

ALTER TABLE core_despacho
ADD CONSTRAINT core_despacho_repartidor_id_fkey 
FOREIGN KEY (repartidor_id) REFERENCES core_usuarioprofile(id) 
ON DELETE SET NULL;

-- Foreign Keys de core_ordenmovimiento
ALTER TABLE core_ordenmovimiento
ADD CONSTRAINT core_ordenmovimiento_orden_id_fkey 
FOREIGN KEY (orden_id) REFERENCES core_orden(id) 
ON DELETE CASCADE;

ALTER TABLE core_ordenmovimiento
ADD CONSTRAINT core_ordenmovimiento_repartidor_id_fkey 
FOREIGN KEY (repartidor_id) REFERENCES core_usuarioprofile(id) 
ON DELETE SET NULL;

ALTER TABLE core_ordenmovimiento
ADD CONSTRAINT core_ordenmovimiento_despacho_id_fkey 
FOREIGN KEY (despacho_id) REFERENCES core_despacho(id) 
ON DELETE SET NULL;

-- Foreign Keys de core_ruta
ALTER TABLE core_ruta
ADD CONSTRAINT core_ruta_repartidor_id_fkey 
FOREIGN KEY (repartidor_id) REFERENCES core_usuarioprofile(id) 
ON DELETE SET NULL;

-- Foreign Keys de core_ruta_ordenes (ManyToMany)
ALTER TABLE core_ruta_ordenes
ADD CONSTRAINT core_ruta_ordenes_ruta_id_fkey 
FOREIGN KEY (ruta_id) REFERENCES core_ruta(id) 
ON DELETE CASCADE;

ALTER TABLE core_ruta_ordenes
ADD CONSTRAINT core_ruta_ordenes_orden_id_fkey 
FOREIGN KEY (orden_id) REFERENCES core_orden(id) 
ON DELETE CASCADE;
```

### 2.6. Script de Creación de Índices

```sql
-- Script: create_indexes.sql
-- Descripción: Crea índices para optimizar consultas frecuentes

-- Índices en core_usuarioprofile
CREATE INDEX IF NOT EXISTS idx_usuarioprofile_rol ON core_usuarioprofile(rol);
CREATE INDEX IF NOT EXISTS idx_usuarioprofile_activo ON core_usuarioprofile(activo);
CREATE INDEX IF NOT EXISTS idx_usuarioprofile_estado_turno ON core_usuarioprofile(estado_turno);

-- Índices en core_moto
CREATE INDEX IF NOT EXISTS idx_moto_estado ON core_moto(estado);
CREATE INDEX IF NOT EXISTS idx_moto_activa ON core_moto(activa);

-- Índices en core_orden
CREATE INDEX IF NOT EXISTS idx_orden_responsable ON core_orden(responsable_id);
CREATE INDEX IF NOT EXISTS idx_orden_estado ON core_orden(estado_actual);
CREATE INDEX IF NOT EXISTS idx_orden_prioridad ON core_orden(prioridad);
CREATE INDEX IF NOT EXISTS idx_orden_fecha_creacion ON core_orden(fecha_creacion);

-- Índices en core_medicamento
CREATE INDEX IF NOT EXISTS idx_medicamento_orden ON core_medicamento(orden_id);
CREATE INDEX IF NOT EXISTS idx_medicamento_codigo ON core_medicamento(codigo);

-- Índices en core_despacho
CREATE INDEX IF NOT EXISTS idx_despacho_orden ON core_despacho(orden_id);
CREATE INDEX IF NOT EXISTS idx_despacho_repartidor ON core_despacho(repartidor_id);
CREATE INDEX IF NOT EXISTS idx_despacho_fecha ON core_despacho(fecha);

-- Índices en core_ordenmovimiento
CREATE INDEX IF NOT EXISTS idx_movimiento_orden ON core_ordenmovimiento(orden_id);
CREATE INDEX IF NOT EXISTS idx_movimiento_timestamp ON core_ordenmovimiento(timestamp);
CREATE INDEX IF NOT EXISTS idx_movimiento_estado ON core_ordenmovimiento(estado);

-- Índices en core_ruta
CREATE INDEX IF NOT EXISTS idx_ruta_repartidor ON core_ruta(repartidor_id);
CREATE INDEX IF NOT EXISTS idx_ruta_activa ON core_ruta(activa);
CREATE INDEX IF NOT EXISTS idx_ruta_fecha_creacion ON core_ruta(fecha_creacion);
```

### 2.7. Script de Verificación de Integridad

```sql
-- Script: verify_integrity.sql
-- Descripción: Verifica la integridad de la base de datos

-- Verificar que todas las FK existen
SELECT 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
ORDER BY tc.table_name, kcu.column_name;

-- Verificar que todos los índices existen
SELECT 
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename LIKE 'core_%'
ORDER BY tablename, indexname;

-- Verificar restricciones CHECK
SELECT 
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type,
    cc.check_clause
FROM information_schema.table_constraints tc
JOIN information_schema.check_constraints cc
  ON tc.constraint_name = cc.constraint_name
WHERE tc.table_schema = 'public'
  AND tc.table_name LIKE 'core_%'
ORDER BY tc.table_name;
```

---

## 3. Ejecución de Scripts

### Orden de Ejecución Recomendado

1. **drop_foreign_keys.sql** - Eliminar FK primero
2. **drop_tables.sql** - Eliminar tablas
3. **create_tables.sql** - Crear tablas
4. **create_foreign_keys.sql** - Crear FK
5. **create_indexes.sql** - Crear índices
6. **verify_integrity.sql** - Verificar integridad

### Comando de Ejecución

```bash
# PostgreSQL
psql -U postgres -d logico_db -f drop_foreign_keys.sql
psql -U postgres -d logico_db -f drop_tables.sql
psql -U postgres -d logico_db -f create_tables.sql
psql -U postgres -d logico_db -f create_foreign_keys.sql
psql -U postgres -d logico_db -f create_indexes.sql
psql -U postgres -d logico_db -f verify_integrity.sql
```

---

## 4. Conclusión

Los scripts SQL están organizados de forma modular y separada, permitiendo:
- ✅ Recreación completa de la base de datos
- ✅ Mantenimiento independiente de cada componente
- ✅ Verificación de integridad
- ✅ Normalización 3NF garantizada
- ✅ Optimización mediante índices estratégicos

