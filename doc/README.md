# Documentación del Proyecto LogiCo

Este directorio contiene toda la documentación técnica del sistema LogiCo.

## 📚 Índice de Documentos

### 1. Estructura y Base de Datos
- **[01_estructura_bd.md](01_estructura_bd.md)** - Modelo conceptual, lógico, diccionario de datos e índices

### 2. Normalización y SQL
- **[02_normalizacion_scripts_sql.md](02_normalizacion_scripts_sql.md)** - Análisis de normalización y scripts SQL separados

### 3. Seguridad
- **[03_patrones_seguridad.md](03_patrones_seguridad.md)** - Documentación de 12 patrones de seguridad implementados

### 4. Documentación de Código
- **[04_documentacion_codigo.md](04_documentacion_codigo.md)** - Mejores prácticas y documentación del código

### 5. Colaboración
- **[05_colaboracion.md](05_colaboracion.md)** - Metodología de trabajo en equipo y colaboración

### 6. Control de Versiones
- **[06_github.md](06_github.md)** - Configuración de GitHub y flujo de trabajo con Git

### 7. Plan de Pruebas
- **[07_plan_pruebas.md](07_plan_pruebas.md)** - Plan completo de pruebas con casos de uso y requerimientos

### 8. Ejecución de Pruebas
- **[08_ejecucion_pruebas.md](08_ejecucion_pruebas.md)** - Protocolo de ejecución y resultados de pruebas

### 9. Análisis de Resultados
- **[09_analisis_resultados.md](09_analisis_resultados.md)** - Análisis detallado de resultados obtenidos

### 10. Comparación de Resultados
- **[10_comparacion_resultados.md](10_comparacion_resultados.md)** - Comparación obtenido vs esperado y métricas

### 11. Plan de Mejora
- **[11_plan_mejora.md](11_plan_mejora.md)** - Plan de mejora continua en todos los aspectos

### 12. Plan de Pruebas Ejecutable
- **[12_plan_pruebas_ejecutable.md](12_plan_pruebas_ejecutable.md)** - Scripts y procedimientos ejecutables para pruebas

### 13. Pruebas de Carga, Estrés y Rendimiento
- **[13_pruebas_carga_estres.md](13_pruebas_carga_estres.md)** - Guía completa de pruebas de carga, estrés y rendimiento

---

## 🚀 Inicio Rápido

### Para Revisar la Estructura de BD:
1. Leer `01_estructura_bd.md` para entender el modelo
2. Revisar `02_normalizacion_scripts_sql.md` para scripts SQL

### Para Entender la Seguridad:
1. Leer `03_patrones_seguridad.md` para ver todos los patrones implementados

### Para Ejecutar Pruebas:
1. **Pruebas Funcionales:** `python logico/test_funcional_basico.py`
2. **Pruebas de Integración:** `python logico/test_integracion_completo.py`
3. **Pruebas de Rendimiento:** `python logico/test_rendimiento.py`
4. **Pruebas de Carga:** `locust -f logico/test_carga.py --host=http://127.0.0.1:8000`
5. **Pruebas de Estrés:** `locust -f logico/test_estres.py --host=http://127.0.0.1:8000 --users=100`

### Para Revisar el Proceso de Pruebas:
1. `07_plan_pruebas.md` - Plan completo
2. `08_ejecucion_pruebas.md` - Resultados
3. `09_analisis_resultados.md` - Análisis
4. `10_comparacion_resultados.md` - Comparación
5. `13_pruebas_carga_estres.md` - Carga y estrés

---

## 📋 Resumen por Categoría

### Base de Datos
- ✅ Modelo conceptual y lógico documentado
- ✅ Diccionario de datos completo
- ✅ Scripts SQL separados (CREATE, DROP, FK, etc.)
- ✅ Normalización 3NF explicada

### Seguridad
- ✅ 12 patrones de seguridad documentados
- ✅ Evidencias de implementación
- ✅ Recomendaciones para producción

### Pruebas
- ✅ Plan de pruebas completo
- ✅ Casos de prueba detallados
- ✅ Scripts ejecutables (funcional, integración, rendimiento)
- ✅ Pruebas de carga y estrés (Locust)
- ✅ Análisis de resultados
- ✅ Comparación obtenido vs esperado

### Proceso
- ✅ Documentación de colaboración
- ✅ Guía de GitHub
- ✅ Plan de mejora continua

---

## 🧪 Scripts de Pruebas Disponibles

| Script | Tipo | Comando |
|--------|------|---------|
| `test_funcional_basico.py` | Funcional | `python logico/test_funcional_basico.py` |
| `test_integracion_completo.py` | Integración | `python logico/test_integracion_completo.py` |
| `test_rendimiento.py` | Rendimiento | `python logico/test_rendimiento.py` |
| `test_carga.py` | Carga | `locust -f logico/test_carga.py --host=http://127.0.0.1:8000` |
| `test_estres.py` | Estrés | `locust -f logico/test_estres.py --host=http://127.0.0.1:8000 --users=100` |

---

## 📝 Notas

- Todos los documentos están en formato Markdown (.md)
- Los scripts SQL están en `02_normalizacion_scripts_sql.md`
- Los scripts de pruebas están en la carpeta `logico/`
- Las pruebas de carga requieren `pip install locust`
- Los documentos pueden actualizarse según evolucione el proyecto

---

**Última actualización:** [Fecha]
**Versión:** 1.0
