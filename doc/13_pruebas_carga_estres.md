# Pruebas de Carga, Estrés y Rendimiento - LogiCo

## 1. Introducción

Este documento describe las pruebas de carga, estrés y rendimiento implementadas para el sistema LogiCo. Estas pruebas permiten evaluar el comportamiento del sistema bajo diferentes condiciones de uso.

---

## 2. Tipos de Pruebas Implementadas

### 2.1. Pruebas de Carga
**Objetivo:** Evaluar el comportamiento del sistema bajo carga normal esperada.

**Archivo:** `logico/test_carga.py`

**Características:**
- Simula usuarios reales navegando el sistema
- Operaciones típicas: ver dashboard, listar órdenes, crear órdenes
- Tiempo de espera realista entre operaciones (1-3 segundos)

### 2.2. Pruebas de Estrés
**Objetivo:** Evaluar el comportamiento del sistema bajo carga extrema.

**Archivo:** `logico/test_estres.py`

**Características:**
- Muchos usuarios simultáneos (100+)
- Operaciones intensivas y rápidas
- Tiempo de espera mínimo (0.1-0.5 segundos)
- Múltiples operaciones de escritura

### 2.3. Pruebas de Rendimiento
**Objetivo:** Medir tiempos de respuesta de operaciones específicas.

**Archivo:** `logico/test_rendimiento.py`

**Características:**
- Mide tiempos de consultas a base de datos
- Evalúa optimizaciones (select_related, prefetch_related)
- Detecta problemas N+1 queries
- Pruebas de concurrencia

### 2.4. Pruebas de Integración Completa
**Objetivo:** Validar flujos completos end-to-end.

**Archivo:** `logico/test_integracion_completo.py`

**Características:**
- Flujos completos de negocio
- Validación de integridad de datos
- Pruebas de permisos y roles

---

## 3. Instalación de Dependencias

### 3.1. Instalar Locust (para pruebas de carga y estrés)

```bash
pip install locust
```

### 3.2. Verificar Instalación

```bash
locust --version
```

---

## 4. Ejecución de Pruebas

### 4.1. Pruebas de Carga

**Comando básico:**
```bash
cd logico
locust -f test_carga.py --host=http://127.0.0.1:8000
```

**Acceder a interfaz web:**
- Abrir navegador en: http://localhost:8089
- Configurar:
  - Number of users: 50
  - Spawn rate: 5 (usuarios por segundo)
  - Host: http://127.0.0.1:8000

**Comando sin interfaz web (headless):**
```bash
locust -f test_carga.py --host=http://127.0.0.1:8000 --users=50 --spawn-rate=5 --run-time=5m --headless
```

**Parámetros:**
- `--users`: Número total de usuarios simultáneos
- `--spawn-rate`: Usuarios creados por segundo
- `--run-time`: Duración de la prueba (ej: 5m, 1h)
- `--headless`: Ejecutar sin interfaz web

### 4.2. Pruebas de Estrés

**Comando básico:**
```bash
locust -f test_estres.py --host=http://127.0.0.1:8000 --users=100 --spawn-rate=10
```

**Prueba extrema:**
```bash
locust -f test_estres.py --host=http://127.0.0.1:8000 --users=200 --spawn-rate=20 --run-time=10m --headless
```

**Monitoreo:**
- Observar uso de CPU y memoria
- Monitorear base de datos
- Revisar logs del servidor

### 4.3. Pruebas de Rendimiento

**Ejecutar:**
```bash
cd logico
python test_rendimiento.py
```

**Salida esperada:**
- Tiempos promedio de cada operación
- Estadísticas (min, max, mediana, desviación)
- Evaluación de rendimiento
- Detección de problemas N+1 queries

### 4.4. Pruebas de Integración Completa

**Ejecutar:**
```bash
cd logico
python test_integracion_completo.py
```

**Valida:**
- Flujos completos de negocio
- Integridad de datos
- Permisos y roles
- Validaciones de negocio

---

## 5. Escenarios de Prueba

### 5.1. Escenario 1: Carga Normal

**Configuración:**
- Usuarios: 20-50
- Spawn rate: 2-5 usuarios/segundo
- Duración: 10 minutos

**Objetivo:**
- Simular uso normal del sistema
- Validar que todos los usuarios pueden trabajar simultáneamente
- Verificar tiempos de respuesta aceptables

**Métricas Esperadas:**
- Tiempo de respuesta promedio < 1 segundo
- Tasa de errores < 1%
- CPU < 70%
- Memoria estable

### 5.2. Escenario 2: Carga Alta

**Configuración:**
- Usuarios: 100-200
- Spawn rate: 10 usuarios/segundo
- Duración: 15 minutos

**Objetivo:**
- Evaluar comportamiento bajo carga alta
- Identificar cuellos de botella
- Validar escalabilidad

**Métricas Esperadas:**
- Tiempo de respuesta promedio < 2 segundos
- Tasa de errores < 5%
- Sistema estable sin crashes

### 5.3. Escenario 3: Estrés Extremo

**Configuración:**
- Usuarios: 500+
- Spawn rate: 50 usuarios/segundo
- Duración: 5 minutos

**Objetivo:**
- Encontrar límites del sistema
- Identificar puntos de falla
- Validar manejo de errores

**Métricas a Observar:**
- Punto de saturación
- Comportamiento de degradación
- Recuperación después del estrés

---

## 6. Métricas y Análisis

### 6.1. Métricas de Rendimiento

**Tiempos de Respuesta:**
- **Excelente:** < 100ms
- **Bueno:** 100-500ms
- **Aceptable:** 500-1000ms
- **Lento:** > 1000ms

**Throughput:**
- Requests por segundo (RPS)
- Operaciones completadas por minuto

**Errores:**
- Tasa de errores (%)
- Tipos de errores
- Distribución de errores

### 6.2. Métricas de Recursos

**CPU:**
- Uso promedio
- Picos de uso
- Distribución por proceso

**Memoria:**
- Uso de RAM
- Memory leaks
- Picos de memoria

**Base de Datos:**
- Conexiones activas
- Queries por segundo
- Tiempo de respuesta de queries

### 6.3. Análisis de Resultados

**Gráficos Generados por Locust:**
1. **Requests per second:** Velocidad de procesamiento
2. **Response times:** Tiempos de respuesta
3. **Number of users:** Usuarios activos
4. **Failures:** Errores por tipo

**Interpretación:**
- Si los tiempos aumentan linealmente con usuarios → Buen escalado
- Si los tiempos aumentan exponencialmente → Problema de escalabilidad
- Si hay muchos errores 500 → Problema en servidor
- Si hay muchos errores 503 → Problema de capacidad

---

## 7. Optimizaciones Identificadas

### 7.1. Optimizaciones de Base de Datos

**Implementadas:**
- ✅ Uso de `select_related()` para JOINs
- ✅ Uso de `prefetch_related()` para ManyToMany
- ✅ Índices en campos de búsqueda frecuente
- ✅ Paginación en listados

**Recomendaciones:**
- Implementar caché para consultas frecuentes
- Optimizar consultas complejas
- Considerar read replicas para lectura

### 7.2. Optimizaciones de Aplicación

**Implementadas:**
- ✅ Consultas optimizadas
- ✅ Paginación en API
- ✅ Filtrado en base de datos

**Recomendaciones:**
- Implementar caché de sesión
- Optimizar serialización JSON
- Considerar CDN para archivos estáticos

---

## 8. Resultados Esperados

### 8.1. Pruebas de Carga (50 usuarios)

| Operación | Tiempo Promedio | Tiempo P95 | Tiempo P99 | Errores |
|-----------|----------------|------------|------------|---------|
| Dashboard | < 500ms | < 800ms | < 1200ms | < 1% |
| Listar Órdenes | < 300ms | < 500ms | < 800ms | < 1% |
| Crear Orden | < 400ms | < 600ms | < 1000ms | < 1% |
| API GET | < 200ms | < 400ms | < 600ms | < 1% |
| API POST | < 300ms | < 500ms | < 800ms | < 1% |

### 8.2. Pruebas de Estrés (200 usuarios)

| Métrica | Valor Esperado |
|---------|----------------|
| Tiempo promedio | < 2s |
| Tasa de errores | < 5% |
| Throughput | > 100 RPS |
| CPU máximo | < 90% |
| Memoria estable | Sin leaks |

---

## 9. Checklist de Pruebas

### 9.1. Antes de Ejecutar

- [ ] Servidor Django corriendo
- [ ] Base de datos con datos de prueba
- [ ] Locust instalado
- [ ] Usuarios de prueba creados
- [ ] Monitoreo de recursos configurado

### 9.2. Durante la Ejecución

- [ ] Monitorear CPU y memoria
- [ ] Revisar logs del servidor
- [ ] Observar métricas de base de datos
- [ ] Verificar que no hay errores críticos

### 9.3. Después de Ejecutar

- [ ] Analizar resultados
- [ ] Identificar cuellos de botella
- [ ] Documentar hallazgos
- [ ] Proponer optimizaciones

---

## 10. Comandos Rápidos

### 10.1. Pruebas Básicas

```bash
# Carga normal
locust -f test_carga.py --host=http://127.0.0.1:8000 --users=50 --spawn-rate=5 --run-time=5m --headless

# Estrés
locust -f test_estres.py --host=http://127.0.0.1:8000 --users=100 --spawn-rate=10 --run-time=10m --headless

# Rendimiento
python test_rendimiento.py

# Integración
python test_integracion_completo.py
```

### 10.2. Exportar Resultados

```bash
# Exportar a CSV
locust -f test_carga.py --host=http://127.0.0.1:8000 --users=50 --spawn-rate=5 --run-time=5m --headless --csv=resultados_carga

# Esto genera:
# - resultados_carga_stats.csv
# - resultados_carga_failures.csv
# - resultados_carga_exceptions.csv
```

---

## 11. Interpretación de Resultados

### 11.1. Tiempos de Respuesta

**Distribución Normal:**
- La mayoría de requests en tiempo promedio
- Pocos outliers
- ✅ Sistema estable

**Distribución con Cola Larga:**
- Muchos requests lentos
- ⚠️ Posible problema de rendimiento
- Revisar optimizaciones

### 11.2. Tasa de Errores

**< 1%:** ✅ Excelente
**1-5%:** ⚠️ Aceptable, revisar
**> 5%:** ❌ Problema, investigar

### 11.3. Throughput

**Aumenta con usuarios:** ✅ Buen escalado
**Se estabiliza:** ⚠️ Límite de capacidad
**Disminuye:** ❌ Problema de rendimiento

---

## 12. Recomendaciones

### 12.1. Para Producción

1. **Monitoreo Continuo:**
   - Implementar APM (Application Performance Monitoring)
   - Alertas de rendimiento
   - Dashboards en tiempo real

2. **Escalabilidad:**
   - Considerar load balancer
   - Múltiples instancias de aplicación
   - Read replicas de base de datos

3. **Optimizaciones:**
   - Caché de consultas frecuentes
   - CDN para archivos estáticos
   - Compresión de respuestas

### 12.2. Para Desarrollo

1. **Testing Continuo:**
   - Ejecutar pruebas de carga regularmente
   - Integrar en CI/CD
   - Comparar resultados entre versiones

2. **Profiling:**
   - Identificar código lento
   - Optimizar hot paths
   - Revisar queries N+1

---

## 13. Conclusión

Las pruebas de carga, estrés y rendimiento proporcionan información valiosa sobre el comportamiento del sistema bajo diferentes condiciones. Es importante ejecutarlas regularmente y usar los resultados para guiar las optimizaciones.

**Próximos Pasos:**
1. Ejecutar pruebas de carga regularmente
2. Monitorear métricas en producción
3. Implementar optimizaciones identificadas
4. Documentar resultados y mejoras

---

**Nota:** Asegúrate de ejecutar estas pruebas en un ambiente de pruebas, no en producción, ya que pueden generar carga significativa en el sistema.

