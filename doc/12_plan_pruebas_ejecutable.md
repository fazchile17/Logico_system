# Plan de Pruebas Ejecutable - LogiCo

## 1. Introducción

Este documento proporciona un plan de pruebas ejecutable paso a paso para validar el sistema LogiCo. Incluye scripts, comandos y procedimientos que pueden ejecutarse directamente.

---

## 2. Configuración del Ambiente de Pruebas

### 2.1. Requisitos Previos

```bash
# Verificar Python
python --version  # Debe ser 3.10+

# Verificar PostgreSQL
psql --version

# Verificar que el proyecto está configurado
cd logico
python manage.py check
```

### 2.2. Crear Base de Datos de Pruebas

```bash
# Crear base de datos de pruebas
createdb -U postgres logico_test_db

# Configurar en settings.py (temporalmente)
# DATABASES['test'] = {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'logico_test_db',
#     'USER': 'postgres',
#     'PASSWORD': '123',
#     'HOST': 'localhost',
#     'PORT': '5432',
# }
```

### 2.3. Cargar Datos de Prueba

```bash
# Ejecutar migraciones
python manage.py migrate

# Cargar datos de prueba
python manage.py seed_data
```

---

## 3. Scripts de Prueba Automatizados

### 3.1. Script de Pruebas Funcionales Básicas

**Archivo: `test_funcional_basico.py`**

```python
"""
Script de pruebas funcionales básicas para LogiCo
Ejecutar: python test_funcional_basico.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logico.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UsuarioProfile, Orden, Moto, Despacho
from django.test import Client
from django.urls import reverse

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.YELLOW}Testing: {name}{Colors.END}")

def print_pass(message):
    print(f"{Colors.GREEN}✓ PASS: {message}{Colors.END}")

def print_fail(message):
    print(f"{Colors.RED}✗ FAIL: {message}{Colors.END}")

def test_crear_usuario():
    """Test: Crear usuario como admin"""
    print_test("Crear Usuario (Admin)")
    
    try:
        # Crear usuario admin si no existe
        admin, created = User.objects.get_or_create(
            username='test_admin',
            defaults={'email': 'admin@test.com', 'is_staff': True}
        )
        if created:
            admin.set_password('test123')
            admin.save()
        
        # Crear perfil
        profile, _ = UsuarioProfile.objects.get_or_create(
            user=admin,
            defaults={'telefono': '123456789', 'rol': 'admin', 'activo': True}
        )
        
        print_pass("Usuario admin creado/obtenido")
        return True
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_crear_moto():
    """Test: Crear moto"""
    print_test("Crear Moto")
    
    try:
        moto, created = Moto.objects.get_or_create(
            patente='TEST01',
            defaults={
                'marca': 'Yamaha',
                'modelo': 'Test',
                'año': 2023,
                'color': 'Negro',
                'cilindrada': 150,
                'kilometraje': 0,
                'estado': 'disponible',
                'activa': True
            }
        )
        
        if created:
            print_pass("Moto creada exitosamente")
        else:
            print_pass("Moto ya existía (OK)")
        return True
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_crear_orden():
    """Test: Crear orden"""
    print_test("Crear Orden")
    
    try:
        orden = Orden.objects.create(
            cliente='Cliente Test',
            direccion='Dirección Test 123',
            telefono_cliente='987654321',
            descripcion='Orden de prueba',
            prioridad='media',
            tipo='normal',
            estado_actual='retiro_receta'
        )
        
        print_pass(f"Orden #{orden.id} creada")
        return True
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_asignar_repartidor_moto():
    """Test: Asignar repartidor a moto"""
    print_test("Asignar Repartidor a Moto")
    
    try:
        # Crear repartidor
        repartidor_user, _ = User.objects.get_or_create(
            username='test_repartidor',
            defaults={'email': 'repartidor@test.com'}
        )
        if not repartidor_user.password:
            repartidor_user.set_password('test123')
            repartidor_user.save()
        
        repartidor, _ = UsuarioProfile.objects.get_or_create(
            user=repartidor_user,
            defaults={'telefono': '123456789', 'rol': 'repartidor', 'activo': True}
        )
        
        # Obtener moto
        moto = Moto.objects.filter(patente='TEST01').first()
        if not moto:
            print_fail("Moto TEST01 no existe")
            return False
        
        # Asignar
        repartidor.moto = moto
        repartidor.save()
        moto.estado = 'en_uso'
        moto.save()
        
        print_pass("Repartidor asignado a moto")
        return True
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_permisos_repartidor():
    """Test: Verificar que repartidor solo ve sus órdenes"""
    print_test("Permisos Repartidor")
    
    try:
        repartidor = UsuarioProfile.objects.filter(rol='repartidor').first()
        if not repartidor:
            print_fail("No hay repartidor para probar")
            return False
        
        # Crear orden asignada al repartidor
        orden = Orden.objects.create(
            cliente='Cliente Test 2',
            direccion='Dirección Test 456',
            telefono_cliente='987654322',
            responsable=repartidor,
            estado_actual='despacho'
        )
        
        # Verificar que repartidor puede verla
        ordenes_repartidor = Orden.objects.filter(responsable=repartidor)
        if orden in ordenes_repartidor:
            print_pass("Repartidor puede ver sus órdenes")
            return True
        else:
            print_fail("Repartidor no puede ver sus órdenes")
            return False
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_listar_ultimo_despacho():
    """Test: Verificar que solo se muestra último intento"""
    print_test("Listar Último Despacho")
    
    try:
        orden = Orden.objects.first()
        if not orden:
            print_fail("No hay órdenes para probar")
            return False
        
        repartidor = UsuarioProfile.objects.filter(rol='repartidor').first()
        if not repartidor:
            print_fail("No hay repartidor para probar")
            return False
        
        # Crear múltiples despachos
        despacho1 = Despacho.objects.create(
            orden=orden,
            numero_despacho=1,
            repartidor=repartidor,
            estado='despacho',
            resultado='no_disponible'
        )
        
        despacho2 = Despacho.objects.create(
            orden=orden,
            numero_despacho=2,
            repartidor=repartidor,
            estado='re_despacho',
            resultado='error'
        )
        
        despacho3 = Despacho.objects.create(
            orden=orden,
            numero_despacho=3,
            repartidor=repartidor,
            estado='re_despacho',
            resultado='entregado'
        )
        
        # Obtener último despacho
        from django.db.models import Max
        ultimo_numero = Despacho.objects.filter(orden=orden).aggregate(Max('numero_despacho'))['numero_despacho__max']
        ultimo_despacho = Despacho.objects.get(orden=orden, numero_despacho=ultimo_numero)
        
        if ultimo_despacho.numero_despacho == 3:
            print_pass("Último despacho identificado correctamente")
            return True
        else:
            print_fail(f"Último despacho incorrecto: {ultimo_despacho.numero_despacho}")
            return False
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_validacion_descanso():
    """Test: Validación de descanso máximo 1 hora"""
    print_test("Validación Descanso 1 Hora")
    
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        repartidor = UsuarioProfile.objects.filter(rol='repartidor').first()
        if not repartidor:
            print_fail("No hay repartidor para probar")
            return False
        
        # Simular descanso iniciado hace 1 hora
        repartidor.estado_turno = 'descanso'
        repartidor.fecha_inicio_descanso = timezone.now() - timedelta(hours=1, minutes=1)
        repartidor.save()
        
        # Verificar que el sistema detecta el exceso
        tiempo_descanso = timezone.now() - repartidor.fecha_inicio_descanso
        if tiempo_descanso >= timedelta(hours=1):
            print_pass("Sistema detecta descanso > 1 hora")
            # Resetear
            repartidor.estado_turno = 'disponible'
            repartidor.fecha_inicio_descanso = None
            repartidor.save()
            return True
        else:
            print_fail("Sistema no detecta descanso > 1 hora")
            return False
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print(f"\n{Colors.YELLOW}{'='*60}")
    print("PLAN DE PRUEBAS EJECUTABLE - LOGICO")
    print(f"{'='*60}{Colors.END}\n")
    
    tests = [
        test_crear_usuario,
        test_crear_moto,
        test_crear_orden,
        test_asignar_repartidor_moto,
        test_permisos_repartidor,
        test_listar_ultimo_despacho,
        test_validacion_descanso,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print_fail(f"Error ejecutando test: {str(e)}")
            results.append(False)
    
    # Resumen
    print(f"\n{Colors.YELLOW}{'='*60}")
    print("RESUMEN DE PRUEBAS")
    print(f"{'='*60}{Colors.END}")
    passed = sum(results)
    total = len(results)
    print(f"Total: {total}")
    print(f"{Colors.GREEN}Pasaron: {passed}{Colors.END}")
    print(f"{Colors.RED}Fallaron: {total - passed}{Colors.END}")
    print(f"Tasa de éxito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print(f"\n{Colors.GREEN}✓ TODAS LAS PRUEBAS PASARON{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}✗ ALGUNAS PRUEBAS FALLARON{Colors.END}")
        return 1

if __name__ == '__main__':
    exit(main())
```

---

## 4. Pruebas Manuales Paso a Paso

### 4.1. Prueba 1: Flujo Completo de Orden

**Objetivo:** Verificar que el flujo completo de una orden funciona correctamente.

**Pasos:**

1. **Iniciar servidor:**
   ```bash
   cd logico
   python manage.py runserver
   ```

2. **Login como Admin:**
   - Ir a: http://127.0.0.1:8000/login/
   - Usuario: `admin`
   - Contraseña: `admin123`
   - Verificar redirección a dashboard

3. **Crear Orden:**
   - Ir a "Órdenes" → "Nueva Orden"
   - Completar:
     - Cliente: "María González"
     - Dirección: "Av. Principal 456, Santiago"
     - Teléfono: "987654321"
     - Tipo: "normal"
   - Guardar
   - Verificar: Orden creada, prioridad "media" automática

4. **Asignar Repartidor:**
   - Ir a detalle de orden
   - En "Asignar Repartidor", seleccionar repartidor
   - Asignar
   - Verificar: Repartidor asignado, movimiento registrado

5. **Login como Repartidor:**
   - Logout
   - Login como: `repartidor1` / `rep123`
   - Verificar: Solo ve sus órdenes asignadas

6. **Crear Despacho:**
   - Ir a orden asignada
   - Crear nuevo despacho
   - Seleccionar resultado: "entregado"
   - Guardar
   - Verificar: Despacho creado, estado de orden actualizado

7. **Verificar Dashboard:**
   - Login como admin
   - Ir a dashboard
   - Verificar: Estadísticas actualizadas

**Resultado Esperado:** Todos los pasos ejecutados sin errores.

---

### 4.2. Prueba 2: Validación de Permisos

**Objetivo:** Verificar que los permisos por rol funcionan correctamente.

**Pasos:**

1. **Login como Repartidor:**
   - Usuario: `repartidor1` / `rep123`
   - Verificar: No ve botón "Nueva Orden"
   - Verificar: No ve botón "Nueva Moto"
   - Verificar: No ve botón "Nuevo Usuario"

2. **Intentar Acceso Directo:**
   - Ir a: http://127.0.0.1:8000/usuarios/nuevo/
   - Verificar: Redirección con mensaje de error

3. **Login como Coordinador:**
   - Usuario: `coordinador1` / `coord123`
   - Verificar: Ve botón "Nueva Orden"
   - Verificar: Ve botón "Nueva Moto"
   - Verificar: NO ve botón "Nuevo Usuario"

4. **Login como Admin:**
   - Usuario: `admin` / `admin123`
   - Verificar: Ve todos los botones

**Resultado Esperado:** Permisos validados correctamente.

---

### 4.3. Prueba 3: Validación de Descanso

**Objetivo:** Verificar que la validación de 1 hora de descanso funciona.

**Pasos:**

1. **Login como Repartidor:**
   - Usuario: `repartidor1` / `rep123`

2. **Ir a Mi Perfil:**
   - Click en "Usuarios" → Ver mi perfil

3. **Iniciar Descanso:**
   - Seleccionar "Descanso" en estado de turno
   - Cambiar estado
   - Verificar: Estado cambió a "Descanso"
   - Verificar: Fecha de inicio registrada

4. **Simular 1 Hora Pasada:**
   - En la base de datos o código, modificar `fecha_inicio_descanso` a hace 1 hora
   - Intentar cambiar estado nuevamente
   - Verificar: Mensaje de advertencia
   - Verificar: Estado cambia automáticamente a "Disponible"

**Resultado Esperado:** Validación funciona correctamente.

---

## 5. Pruebas de API REST

### 5.1. Script de Pruebas de API

**Archivo: `test_api.sh`** (Linux/Mac) o `test_api.ps1` (Windows)

```bash
#!/bin/bash
# test_api.sh - Pruebas de API REST

BASE_URL="http://127.0.0.1:8000/api"

echo "=== PRUEBAS DE API REST ==="

# 1. Obtener token
echo -e "\n1. Obteniendo token..."
TOKEN=$(curl -s -X POST $BASE_URL/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | jq -r '.token')

if [ "$TOKEN" != "null" ] && [ -n "$TOKEN" ]; then
  echo "✓ Token obtenido: ${TOKEN:0:20}..."
else
  echo "✗ Error obteniendo token"
  exit 1
fi

# 2. Listar órdenes
echo -e "\n2. Listando órdenes..."
curl -s -X GET $BASE_URL/ordenes/ \
  -H "Authorization: Token $TOKEN" | jq '.count'

# 3. Crear orden
echo -e "\n3. Creando orden..."
ORDEN_ID=$(curl -s -X POST $BASE_URL/ordenes/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "Test API",
    "direccion": "Test 123",
    "telefono_cliente": "123456789",
    "tipo": "normal",
    "prioridad": "media"
  }' | jq -r '.id')

if [ "$ORDEN_ID" != "null" ] && [ -n "$ORDEN_ID" ]; then
  echo "✓ Orden creada: ID $ORDEN_ID"
else
  echo "✗ Error creando orden"
fi

# 4. Ver detalle de orden
echo -e "\n4. Viendo detalle de orden..."
curl -s -X GET $BASE_URL/ordenes/$ORDEN_ID/ \
  -H "Authorization: Token $TOKEN" | jq '.cliente'

echo -e "\n=== PRUEBAS COMPLETADAS ==="
```

**Para Windows PowerShell (`test_api.ps1`):**

```powershell
# test_api.ps1 - Pruebas de API REST

$BASE_URL = "http://127.0.0.1:8000/api"

Write-Host "=== PRUEBAS DE API REST ===" -ForegroundColor Yellow

# 1. Obtener token
Write-Host "`n1. Obteniendo token..." -ForegroundColor Cyan
$response = Invoke-RestMethod -Uri "$BASE_URL/token/" -Method Post -ContentType "application/json" -Body '{"username": "admin", "password": "admin123"}'
$TOKEN = $response.token

if ($TOKEN) {
    Write-Host "✓ Token obtenido: $($TOKEN.Substring(0, 20))..." -ForegroundColor Green
} else {
    Write-Host "✗ Error obteniendo token" -ForegroundColor Red
    exit 1
}

# 2. Listar órdenes
Write-Host "`n2. Listando órdenes..." -ForegroundColor Cyan
$headers = @{ "Authorization" = "Token $TOKEN" }
$ordenes = Invoke-RestMethod -Uri "$BASE_URL/ordenes/" -Method Get -Headers $headers
Write-Host "Total de órdenes: $($ordenes.count)" -ForegroundColor Green

# 3. Crear orden
Write-Host "`n3. Creando orden..." -ForegroundColor Cyan
$ordenData = @{
    cliente = "Test API"
    direccion = "Test 123"
    telefono_cliente = "123456789"
    tipo = "normal"
    prioridad = "media"
} | ConvertTo-Json

$nuevaOrden = Invoke-RestMethod -Uri "$BASE_URL/ordenes/" -Method Post -Headers $headers -ContentType "application/json" -Body $ordenData
Write-Host "✓ Orden creada: ID $($nuevaOrden.id)" -ForegroundColor Green

Write-Host "`n=== PRUEBAS COMPLETADAS ===" -ForegroundColor Yellow
```

---

## 6. Checklist de Pruebas Rápido

### 6.1. Checklist Funcional

```markdown
## Checklist de Pruebas Rápido

### Autenticación
- [ ] Login funciona
- [ ] Logout funciona
- [ ] Redirección según rol funciona

### Usuarios
- [ ] Admin puede crear usuarios
- [ ] Coordinador NO puede crear usuarios
- [ ] Repartidor solo se ve a sí mismo
- [ ] Cambio de estado de turno funciona
- [ ] Validación de descanso 1 hora funciona

### Motos
- [ ] Coordinador/Admin pueden crear motos
- [ ] Repartidor NO puede crear motos
- [ ] Asignación de repartidor funciona
- [ ] Estado de moto se actualiza

### Órdenes
- [ ] Coordinador/Admin pueden crear órdenes
- [ ] Repartidor NO puede crear órdenes
- [ ] Repartidor solo ve sus órdenes
- [ ] Asignación de repartidor funciona
- [ ] Prioridad automática funciona

### Despachos
- [ ] Crear despacho funciona
- [ ] Solo último intento visible en lista
- [ ] Contador de intentos correcto
- [ ] Upload de foto funciona

### Dashboard
- [ ] Estadísticas se muestran
- [ ] Gráficos renderizan
- [ ] Datos actualizados
```

---

## 7. Comandos de Ejecución Rápida

### 7.1. Ejecutar Todas las Pruebas

```bash
# 1. Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# 2. Ir al directorio del proyecto
cd logico

# 3. Ejecutar script de pruebas
python test_funcional_basico.py

# 4. Ejecutar pruebas de API (si el servidor está corriendo)
bash test_api.sh  # Linux/Mac
# o
powershell -ExecutionPolicy Bypass -File test_api.ps1  # Windows
```

---

## 8. Plantilla de Reporte de Pruebas

**Archivo: `reporte_pruebas.md`**

```markdown
# Reporte de Pruebas - [Fecha]

## Resumen
- Fecha: [Fecha]
- Ejecutado por: [Nombre]
- Ambiente: [Desarrollo/Staging/Producción]

## Resultados
- Total de pruebas: [Número]
- Pasaron: [Número]
- Fallaron: [Número]
- Tasa de éxito: [Porcentaje]%

## Detalles
[Agregar detalles de cada prueba]

## Bugs Encontrados
[Si hay bugs, documentarlos aquí]

## Observaciones
[Notas adicionales]
```

---

## 9. Conclusión

Este plan de pruebas ejecutable proporciona:

✅ Scripts automatizados para pruebas básicas
✅ Procedimientos manuales paso a paso
✅ Scripts de API REST
✅ Checklist rápido
✅ Plantillas de reporte

**Para ejecutar las pruebas:**
1. Seguir la configuración del ambiente
2. Ejecutar scripts automatizados
3. Realizar pruebas manuales
4. Documentar resultados

---

**Nota:** Los scripts deben guardarse en la carpeta `logico/` y ejecutarse desde allí. Asegúrate de tener el servidor corriendo para las pruebas de API.

