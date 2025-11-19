# Guía de Ejecución de Pruebas - LogiCo

## 1. Instalación de Dependencias

### 1.1. Instalar Locust (para pruebas de carga y estrés)

```bash
pip install locust
```

O instalar todas las dependencias:

```bash
pip install -r requirements.txt
```

---

## 2. Preparación del Ambiente

### 2.1. Configurar Base de Datos

```bash
cd logico

# Ejecutar migraciones
python manage.py migrate

# Cargar datos de prueba
python manage.py seed_data
```

### 2.2. Iniciar Servidor (para pruebas de carga/estrés)

```bash
# En una terminal
python manage.py runserver
```

---

## 3. Tipos de Pruebas Disponibles

### 3.1. Pruebas Funcionales Básicas

**Archivo:** `logico/test_funcional_basico.py`

**Descripción:** Pruebas unitarias básicas de funcionalidades principales.

**Ejecutar:**
```bash
cd logico
python test_funcional_basico.py
```

**Pruebas Incluidas:**
- ✅ Crear usuario
- ✅ Crear moto
- ✅ Crear orden
- ✅ Asignar repartidor a moto
- ✅ Permisos de repartidor
- ✅ Listar último despacho
- ✅ Validación de descanso
- ✅ Excluir admin de repartidores

**Salida Esperada:**
```
PLAN DE PRUEBAS EJECUTABLE - LOGICO
============================================================

Testing: Crear Usuario (Admin)
✓ PASS: Usuario admin creado/obtenido
...
RESUMEN DE PRUEBAS
Total: 8
Pasaron: 8
Fallaron: 0
Tasa de éxito: 100.0%
```

---

### 3.2. Pruebas de Integración Completa

**Archivo:** `logico/test_integracion_completo.py`

**Descripción:** Pruebas end-to-end de flujos completos de negocio.

**Ejecutar:**
```bash
cd logico
python test_integracion_completo.py
```

**Pruebas Incluidas:**
- ✅ Flujo completo de orden (creación → asignación → despacho → entrega)
- ✅ Flujo con re-despacho (múltiples intentos)
- ✅ Asignación moto-repartidor completa
- ✅ Validación completa de descanso
- ✅ Permisos por rol

**Salida Esperada:**
```
PRUEBAS DE INTEGRACIÓN COMPLETAS - LOGICO
======================================================================

Testing: Flujo Completo de Orden
✓ PASS: 1. Orden #X creada
✓ PASS: 2. 2 medicamentos agregados
...
```

---

### 3.3. Pruebas de Rendimiento

**Archivo:** `logico/test_rendimiento.py`

**Descripción:** Mide tiempos de respuesta y optimizaciones de consultas.

**Ejecutar:**
```bash
cd logico
python test_rendimiento.py
```

**Métricas Medidas:**
- Tiempos de consultas simples
- Tiempos de consultas con JOINs
- Tiempos de consultas con agregaciones
- Tiempos de creación/actualización
- Detección de problemas N+1 queries
- Pruebas de concurrencia

**Salida Esperada:**
```
PRUEBAS DE RENDIMIENTO - LOGICO
======================================================================

Probando: Consulta Simple (10 órdenes)
  Promedio: 15.23ms
  Mediana: 14.50ms
  Min: 12.00ms | Max: 25.00ms
  ✓ Excelente rendimiento
...
```

---

### 3.4. Pruebas de Carga

**Archivo:** `logico/test_carga.py`

**Descripción:** Simula usuarios reales navegando el sistema.

**Ejecutar con Interfaz Web:**
```bash
cd logico
locust -f test_carga.py --host=http://127.0.0.1:8000
```

Luego abrir navegador en: http://localhost:8089

**Ejecutar sin Interfaz (Headless):**
```bash
locust -f test_carga.py --host=http://127.0.0.1:8000 --users=50 --spawn-rate=5 --run-time=5m --headless
```

**Parámetros:**
- `--users=50`: Número de usuarios simultáneos
- `--spawn-rate=5`: Usuarios creados por segundo
- `--run-time=5m`: Duración (5 minutos)
- `--headless`: Sin interfaz web

**Escenarios:**
- **Carga Normal:** 20-50 usuarios, spawn-rate 2-5
- **Carga Alta:** 100-200 usuarios, spawn-rate 10

---

### 3.5. Pruebas de Estrés

**Archivo:** `logico/test_estres.py`

**Descripción:** Evalúa el sistema bajo carga extrema.

**Ejecutar:**
```bash
cd logico
locust -f test_estres.py --host=http://127.0.0.1:8000 --users=100 --spawn-rate=10 --run-time=10m --headless
```

**Parámetros Recomendados:**
- **Estrés Moderado:** `--users=100 --spawn-rate=10`
- **Estrés Alto:** `--users=200 --spawn-rate=20`
- **Estrés Extremo:** `--users=500 --spawn-rate=50`

**⚠️ Advertencia:** Estas pruebas generan carga significativa. Ejecutar solo en ambiente de pruebas.

---

## 4. Ejecución Completa de Todas las Pruebas

### 4.1. Script de Ejecución Completa

**Crear archivo:** `ejecutar_todas_pruebas.sh` (Linux/Mac) o `ejecutar_todas_pruebas.bat` (Windows)

**Linux/Mac:**
```bash
#!/bin/bash
# ejecutar_todas_pruebas.sh

echo "=== EJECUTANDO TODAS LAS PRUEBAS ==="

cd logico

echo -e "\n1. Pruebas Funcionales Básicas..."
python test_funcional_basico.py

echo -e "\n2. Pruebas de Integración..."
python test_integracion_completo.py

echo -e "\n3. Pruebas de Rendimiento..."
python test_rendimiento.py

echo -e "\n=== PRUEBAS COMPLETADAS ==="
```

**Windows:**
```batch
@echo off
REM ejecutar_todas_pruebas.bat

echo === EJECUTANDO TODAS LAS PRUEBAS ===

cd logico

echo.
echo 1. Pruebas Funcionales Básicas...
python test_funcional_basico.py

echo.
echo 2. Pruebas de Integración...
python test_integracion_completo.py

echo.
echo 3. Pruebas de Rendimiento...
python test_rendimiento.py

echo.
echo === PRUEBAS COMPLETADAS ===
pause
```

---

## 5. Interpretación de Resultados

### 5.1. Pruebas Funcionales e Integración

**✅ Éxito:**
- Todas las pruebas pasan
- Tasa de éxito: 100%
- Sin errores

**⚠️ Advertencia:**
- Algunas pruebas fallan
- Revisar mensajes de error
- Corregir problemas identificados

### 5.2. Pruebas de Rendimiento

**Excelente:** < 100ms promedio
**Bueno:** 100-500ms promedio
**Aceptable:** 500-1000ms promedio
**Lento:** > 1000ms promedio

**Problemas Detectados:**
- N+1 queries: Revisar uso de select_related/prefetch_related
- Consultas lentas: Revisar índices y optimizaciones
- Alto uso de memoria: Revisar leaks

### 5.3. Pruebas de Carga/Estrés

**Métricas Clave:**
- **Tiempo de respuesta promedio:** Debe estar dentro de límites
- **Tasa de errores:** Debe ser < 5%
- **Throughput:** Requests por segundo
- **CPU/Memoria:** Monitorear uso de recursos

**Gráficos en Locust:**
- Requests per second
- Response times (percentiles)
- Number of users
- Failures

---

## 6. Comandos Rápidos de Referencia

### 6.1. Pruebas Básicas

```bash
# Funcional
python logico/test_funcional_basico.py

# Integración
python logico/test_integracion_completo.py

# Rendimiento
python logico/test_rendimiento.py
```

### 6.2. Pruebas de Carga

```bash
# Interfaz web
locust -f logico/test_carga.py --host=http://127.0.0.1:8000

# Headless (50 usuarios, 5 por segundo, 5 minutos)
locust -f logico/test_carga.py --host=http://127.0.0.1:8000 --users=50 --spawn-rate=5 --run-time=5m --headless
```

### 6.3. Pruebas de Estrés

```bash
# Estrés moderado
locust -f logico/test_estres.py --host=http://127.0.0.1:8000 --users=100 --spawn-rate=10 --run-time=10m --headless

# Estrés extremo
locust -f logico/test_estres.py --host=http://127.0.0.1:8000 --users=500 --spawn-rate=50 --run-time=5m --headless
```

### 6.4. Exportar Resultados

```bash
# Exportar a CSV
locust -f logico/test_carga.py --host=http://127.0.0.1:8000 --users=50 --spawn-rate=5 --run-time=5m --headless --csv=resultados

# Genera:
# - resultados_stats.csv
# - resultados_failures.csv
# - resultados_exceptions.csv
```

---

## 7. Troubleshooting

### 7.1. Error: "ModuleNotFoundError: No module named 'locust'"

**Solución:**
```bash
pip install locust
```

### 7.2. Error: "Connection refused" en pruebas de carga

**Solución:**
- Verificar que el servidor Django está corriendo
- Verificar que el host es correcto (http://127.0.0.1:8000)

### 7.3. Error: "Database locked" o "Connection pool exhausted"

**Solución:**
- Reducir número de usuarios simultáneos
- Aumentar conexiones en PostgreSQL
- Revisar configuración de base de datos

### 7.4. Pruebas muy lentas

**Solución:**
- Revisar índices en base de datos
- Optimizar consultas
- Revisar uso de select_related/prefetch_related
- Verificar que no hay N+1 queries

---

## 8. Mejores Prácticas

### 8.1. Orden de Ejecución Recomendado

1. **Pruebas Funcionales** - Verificar funcionalidad básica
2. **Pruebas de Integración** - Verificar flujos completos
3. **Pruebas de Rendimiento** - Identificar problemas de performance
4. **Pruebas de Carga** - Validar bajo carga normal
5. **Pruebas de Estrés** - Encontrar límites del sistema

### 8.2. Frecuencia Recomendada

- **Pruebas Funcionales/Integración:** Antes de cada commit
- **Pruebas de Rendimiento:** Semanalmente
- **Pruebas de Carga:** Antes de releases importantes
- **Pruebas de Estrés:** Mensualmente o antes de cambios mayores

### 8.3. Ambiente de Pruebas

- ✅ Usar base de datos separada para pruebas
- ✅ Datos de prueba realistas pero controlados
- ✅ Monitorear recursos durante pruebas
- ✅ Documentar resultados

---

## 9. Métricas de Éxito

### 9.1. Pruebas Funcionales/Integración

- ✅ Tasa de éxito: 100%
- ✅ Sin errores críticos
- ✅ Todos los flujos funcionan

### 9.2. Pruebas de Rendimiento

- ✅ Tiempo promedio < 500ms
- ✅ Sin problemas N+1 queries
- ✅ Consultas optimizadas

### 9.3. Pruebas de Carga

- ✅ Tiempo promedio < 1s (50 usuarios)
- ✅ Tasa de errores < 1%
- ✅ Throughput estable

### 9.4. Pruebas de Estrés

- ✅ Sistema no crashea
- ✅ Tasa de errores < 5%
- ✅ Recuperación después del estrés

---

## 10. Reportes y Documentación

### 10.1. Generar Reporte de Pruebas

Después de ejecutar las pruebas, documentar:

1. **Fecha y hora de ejecución**
2. **Ambiente (desarrollo/staging)**
3. **Resultados de cada tipo de prueba**
4. **Métricas obtenidas**
5. **Problemas encontrados**
6. **Recomendaciones**

### 10.2. Plantilla de Reporte

```markdown
# Reporte de Pruebas - [Fecha]

## Resumen
- Fecha: [Fecha]
- Ambiente: [Desarrollo/Staging]
- Ejecutado por: [Nombre]

## Resultados

### Pruebas Funcionales
- Total: [N]
- Pasaron: [N]
- Fallaron: [N]
- Tasa de éxito: [%]

### Pruebas de Rendimiento
- Operación más lenta: [Nombre] - [Tiempo]ms
- Operación más rápida: [Nombre] - [Tiempo]ms
- Problemas detectados: [Lista]

### Pruebas de Carga
- Usuarios: [N]
- Duración: [Tiempo]
- Tiempo promedio: [Tiempo]ms
- Tasa de errores: [%]
- Throughput: [RPS]

## Problemas Encontrados
[Detalles de problemas]

## Recomendaciones
[Recomendaciones de mejora]
```

---

## 11. Conclusión

Esta guía proporciona todas las herramientas necesarias para ejecutar pruebas completas del sistema LogiCo. La ejecución regular de estas pruebas garantiza la calidad y rendimiento del sistema.

**Próximos Pasos:**
1. Instalar dependencias
2. Ejecutar pruebas funcionales básicas
3. Ejecutar pruebas de integración
4. Ejecutar pruebas de rendimiento
5. Ejecutar pruebas de carga (opcional)
6. Documentar resultados

---

**Nota:** Las pruebas de carga y estrés generan carga significativa. Siempre ejecutarlas en ambiente de pruebas, nunca en producción.

