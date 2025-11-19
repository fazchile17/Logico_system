# Documentación del Código - LogiCo

## Introducción

Este documento describe las mejores prácticas de codificación aplicadas y la documentación presente en el código fuente del proyecto LogiCo.

---

## 1. Estructura del Proyecto

```
logico/
├── manage.py                 # Script de administración Django
├── logico/                   # Configuración del proyecto
│   ├── settings.py          # Configuración principal
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # Configuración WSGI
├── core/                     # Aplicación principal
│   ├── models.py            # Modelos de datos
│   ├── views.py             # Vistas web
│   ├── api_views.py         # ViewSets para API REST
│   ├── serializers.py       # Serializers DRF
│   ├── forms.py             # Formularios Django
│   ├── urls.py              # URLs de la aplicación
│   ├── api_urls.py          # URLs de la API
│   ├── admin.py             # Configuración admin
│   ├── signals.py           # Señales Django
│   └── management/          # Comandos de gestión
│       └── commands/
│           ├── seed_data.py
│           └── generar_reporte_diario.py
└── requirements.txt          # Dependencias del proyecto
```

---

## 2. Convenciones de Nomenclatura

### Modelos
- **PascalCase:** `UsuarioProfile`, `Orden`, `Despacho`
- **Singular:** Cada modelo representa una entidad única

### Vistas
- **snake_case:** `orden_list`, `usuario_create`, `cambiar_estado_turno`
- **Descriptivo:** Nombres que indican claramente la acción

### Variables
- **snake_case:** `user_profile`, `ordenes`, `despachos`
- **Descriptivo:** Nombres que indican el propósito

### Constantes
- **UPPER_SNAKE_CASE:** `ESTADO_CHOICES`, `ROL_CHOICES`

---

## 3. Documentación en Modelos

### Ejemplo: Modelo Orden

```python
class Orden(models.Model):
    """
    Modelo que representa una orden de medicamentos.
    
    Una orden puede pasar por diferentes estados:
    - retiro_receta: Orden creada, pendiente de retiro
    - traslado: En proceso de traslado
    - despacho: En proceso de despacho
    - re_despacho: Reintento de despacho
    
    Attributes:
        cliente: Nombre del cliente que solicita la orden
        direccion: Dirección de entrega
        prioridad: Prioridad automática según tipo de orden
        responsable: Repartidor asignado (opcional)
    """
    
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]
    
    # Campos del modelo...
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe save() para asignar prioridad automática.
        
        Reglas:
        - receta_detendida → prioridad alta
        - normal → prioridad media
        """
        if self.tipo == 'receta_detendida' and not self.prioridad:
            self.prioridad = 'alta'
        elif self.tipo == 'normal' and not self.prioridad:
            self.prioridad = 'media'
        super().save(*args, **kwargs)
```

---

## 4. Documentación en Vistas

### Ejemplo: Vista de Lista de Órdenes

```python
@login_required
def orden_list(request):
    """
    Lista de órdenes con filtros según el rol del usuario.
    
    Permisos:
    - Admin/Coordinador: Ven todas las órdenes
    - Repartidor: Solo ven sus órdenes asignadas
    
    Filtros disponibles:
    - estado: Filtra por estado actual
    - prioridad: Filtra por prioridad
    - search: Búsqueda por cliente, dirección o teléfono
    
    Args:
        request: HttpRequest con parámetros GET para filtros
        
    Returns:
        HttpResponse con template orden_list.html
    """
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Filtros según rol
    if user_profile.rol == 'repartidor':
        ordenes = Orden.objects.filter(responsable=user_profile)
    else:
        ordenes = Orden.objects.all()
    
    # Aplicar filtros adicionales...
    
    return render(request, 'core/orden_list.html', context)
```

---

## 5. Documentación en API

### Ejemplo: ViewSet de Órdenes

```python
class OrdenViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de órdenes mediante API REST.
    
    Endpoints:
    - GET /api/ordenes/ - Lista de órdenes
    - POST /api/ordenes/ - Crear orden
    - GET /api/ordenes/{id}/ - Detalle de orden
    - PUT /api/ordenes/{id}/ - Actualizar orden
    - DELETE /api/ordenes/{id}/ - Eliminar orden
    
    Acciones personalizadas:
    - POST /api/ordenes/{id}/cambiar_estado/ - Cambiar estado
    - POST /api/ordenes/{id}/asignar_repartidor/ - Asignar repartidor
    
    Permisos:
    - Requiere autenticación
    - Repartidores solo ven sus órdenes asignadas
    """
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtra el queryset según el rol del usuario.
        
        Returns:
            QuerySet filtrado de órdenes
        """
        user_profile, _ = UsuarioProfile.objects.get_or_create(...)
        if user_profile.rol == 'repartidor':
            return Orden.objects.filter(responsable=user_profile)
        return Orden.objects.all()
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """
        Cambia el estado de una orden y registra el movimiento.
        
        Parámetros esperados:
        - estado: Nuevo estado (retiro_receta, traslado, despacho, re_despacho)
        - descripcion: Descripción opcional del cambio
        
        Returns:
            Response con mensaje de confirmación
        """
        # Implementación...
```

---

## 6. Documentación en Formularios

### Ejemplo: Formulario de Orden

```python
class OrdenForm(forms.ModelForm):
    """
    Formulario para crear y editar órdenes.
    
    Campos:
    - cliente: Nombre del cliente (requerido)
    - direccion: Dirección de entrega (requerido)
    - telefono_cliente: Teléfono de contacto (requerido)
    - responsable: Repartidor asignado (opcional, solo para admin/coordinador)
    
    Validaciones:
    - Excluye administradores de la lista de repartidores
    - Prioridad se asigna automáticamente según tipo
    """
    
    class Meta:
        model = Orden
        fields = [
            'cliente', 'direccion', 'telefono_cliente', 'descripcion',
            'prioridad', 'tipo', 'estado_actual', 'responsable'
        ]
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario y configura campos según el usuario.
        
        Args:
            user: Usuario actual (opcional)
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Excluir admin de la lista de repartidores
        self.fields['responsable'].queryset = UsuarioProfile.objects.filter(
            rol='repartidor', 
            activo=True
        ).exclude(user__is_superuser=True)
```

---

## 7. Comentarios en el Código

### Buenas Prácticas Aplicadas

#### 1. Comentarios Explicativos
```python
# Obtener el último despacho de cada orden (el que tiene el numero_despacho más alto)
# Usamos una subconsulta para obtener el máximo numero_despacho por orden
from django.db.models import Max, OuterRef, Subquery

despachos = despachos_base.filter(
    numero_despacho=Subquery(...)
)
```

#### 2. Comentarios de Sección
```python
# ========== VISTAS DE USUARIOS ==========

@login_required
def usuario_list(request):
    """Lista de usuarios - Permisos según rol"""
    ...
```

#### 3. Comentarios TODO/FIXME
```python
# TODO: Implementar paginación para listas grandes
# FIXME: Validar formato de RUT chileno
```

#### 4. Comentarios de Validación
```python
# Validar que no sea admin
if repartidor.user.is_superuser:
    messages.error(request, 'No se puede asignar un administrador como repartidor.')
    return redirect('orden_detail', pk=pk)

# Validar que tenga moto
if not repartidor.moto:
    messages.error(request, 'El repartidor debe tener una moto asignada.')
    return redirect('orden_detail', pk=pk)
```

---

## 8. Mejores Prácticas Aplicadas

### 8.1. DRY (Don't Repeat Yourself)
```python
# ✅ CORRECTO - Función reutilizable
def get_user_profile(request):
    return UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={'telefono': '', 'rol': 'repartidor', ...}
    )

# ❌ INCORRECTO - Código duplicado
# Repetir get_or_create en cada vista
```

### 8.2. Separación de Responsabilidades
- **models.py:** Solo lógica de datos
- **views.py:** Solo lógica de presentación
- **forms.py:** Solo validación de formularios
- **serializers.py:** Solo serialización API

### 8.3. Uso de Propiedades
```python
@property
def repartidor_asignado(self):
    """Retorna el repartidor asignado a esta moto."""
    try:
        return UsuarioProfile.objects.get(moto=self)
    except UsuarioProfile.DoesNotExist:
        return None

@property
def tasa_exito(self):
    """Calcula la tasa de éxito de entregas."""
    if self.entregas_totales > 0:
        return (self.entregas_exitosas / self.entregas_totales) * 100
    return 0
```

### 8.4. Manejo de Errores
```python
try:
    repartidor = UsuarioProfile.objects.get(pk=repartidor_id, rol='repartidor')
except UsuarioProfile.DoesNotExist:
    return Response(
        {'error': 'Repartidor no encontrado'}, 
        status=status.HTTP_404_NOT_FOUND
    )
```

### 8.5. Consultas Optimizadas
```python
# ✅ CORRECTO - select_related para JOINs
usuarios = UsuarioProfile.objects.select_related('user', 'moto').all()

# ✅ CORRECTO - prefetch_related para ManyToMany
ordenes = Orden.objects.prefetch_related('medicamentos', 'despachos').all()

# ❌ INCORRECTO - N+1 queries
for orden in Orden.objects.all():
    print(orden.responsable.user.username)  # Query por cada orden
```

---

## 9. Estándares de Código

### 9.1. PEP 8 Compliance
- Líneas máximo 79-99 caracteres
- Indentación de 4 espacios
- Nombres descriptivos
- Espacios alrededor de operadores

### 9.2. Imports Organizados
```python
# 1. Librerías estándar
import json
import csv
from datetime import timedelta

# 2. Librerías de terceros
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# 3. Aplicaciones locales
from .models import Orden, UsuarioProfile
from .forms import OrdenForm
```

### 9.3. Configuración de Linter
Se recomienda usar:
- **flake8:** Verificación de estilo PEP 8
- **pylint:** Análisis estático de código
- **black:** Formateo automático (opcional)

---

## 10. Documentación de Funciones Complejas

### Ejemplo: Lógica de Filtrado de Despachos

```python
@login_required
def despacho_list(request):
    """
    Lista de despachos - Solo muestra el último intento por orden.
    
    Esta función implementa una lógica especial:
    1. Obtiene todos los despachos (respetando filtros de rol)
    2. Para cada orden, identifica el último despacho (mayor numero_despacho)
    3. Muestra solo esos últimos despachos
    4. Anota cada despacho con el total de intentos de su orden
    
    Esto evita mostrar múltiples filas para la misma orden cuando
    hay reintentos de despacho.
    
    Args:
        request: HttpRequest con posibles filtros GET (estado, resultado)
        
    Returns:
        HttpResponse con template despacho_list.html mostrando solo
        el último intento de cada orden con el conteo total de intentos.
    """
    # Implementación detallada...
```

---

## 11. Guía de Contribución al Código

### Al Agregar Nuevas Funcionalidades:

1. **Documentar el propósito:** Agregar docstring a funciones/clases
2. **Explicar lógica compleja:** Comentarios donde sea necesario
3. **Validar entrada:** Siempre validar datos de usuario
4. **Manejar errores:** Try/except con mensajes claros
5. **Optimizar consultas:** Usar select_related/prefetch_related
6. **Probar permisos:** Validar roles y permisos

### Ejemplo de Nueva Función Documentada:

```python
@login_required
def nueva_funcionalidad(request, pk):
    """
    Descripción clara de qué hace la función.
    
    Esta función realiza las siguientes acciones:
    1. Valida permisos del usuario
    2. Obtiene el objeto requerido
    3. Procesa la lógica de negocio
    4. Retorna la respuesta apropiada
    
    Args:
        request: HttpRequest con datos del usuario
        pk: Identificador del objeto a procesar
        
    Returns:
        HttpResponse con resultado o redirección
        
    Raises:
        Http404: Si el objeto no existe
        PermissionDenied: Si el usuario no tiene permisos
        
    Ejemplo:
        >>> response = nueva_funcionalidad(request, orden_id=1)
        >>> response.status_code
        200
    """
    # Validación de permisos
    user_profile = get_user_profile(request)
    if user_profile.rol not in ['admin', 'coordinador']:
        messages.error(request, 'No tienes permisos.')
        return redirect('home')
    
    # Lógica de negocio
    objeto = get_object_or_404(Modelo, pk=pk)
    # ... procesamiento ...
    
    return render(request, 'template.html', context)
```

---

## 12. Herramientas de Documentación

### 12.1. Docstrings
- **Formato:** Google Style o NumPy Style
- **Ubicación:** Todas las funciones públicas
- **Contenido:** Descripción, args, returns, raises

### 12.2. Type Hints (Recomendado para Futuro)
```python
from typing import Optional

def obtener_repartidor(usuario_id: int) -> Optional[UsuarioProfile]:
    """Obtiene el perfil de repartidor por ID."""
    return UsuarioProfile.objects.filter(
        pk=usuario_id, 
        rol='repartidor'
    ).first()
```

### 12.3. README.md
- Instrucciones de instalación
- Estructura del proyecto
- Ejemplos de uso
- Configuración requerida

---

## 13. Checklist de Documentación

Para cada función/clase nueva, verificar:

- [ ] Docstring con descripción clara
- [ ] Documentación de parámetros (Args)
- [ ] Documentación de retorno (Returns)
- [ ] Documentación de excepciones (Raises)
- [ ] Comentarios en lógica compleja
- [ ] Ejemplos de uso (si aplica)
- [ ] Referencias a funciones relacionadas

---

## 14. Conclusión

El código de LogiCo sigue las mejores prácticas de documentación:

✅ **Docstrings** en funciones y clases importantes
✅ **Comentarios** en lógica compleja
✅ **Nombres descriptivos** que explican el propósito
✅ **Estructura clara** y organizada
✅ **Separación de responsabilidades**
✅ **Código autodocumentado** mediante buenas prácticas

**Áreas de Mejora:**
- Agregar más docstrings en funciones privadas
- Implementar type hints
- Generar documentación automática con Sphinx
- Agregar ejemplos de uso en docstrings

