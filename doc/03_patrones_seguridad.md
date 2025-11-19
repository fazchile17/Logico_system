# Patrones de Seguridad Implementados - LogiCo

## Introducción

Este documento describe los patrones de seguridad implementados en el sistema LogiCo. Se han aplicado múltiples capas de seguridad para proteger contra vulnerabilidades comunes y garantizar la integridad de los datos.

---

## 1. Protección CSRF (Cross-Site Request Forgery)

### Descripción
Protección contra ataques CSRF que intentan ejecutar acciones no autorizadas en nombre de usuarios autenticados.

### Implementación

**Ubicación:** `logico/logico/settings.py`

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # ← Protección CSRF
    ...
]
```

**Ubicación en Templates:** Todos los formularios incluyen `{% csrf_token %}`

**Ejemplo:**
```html
<!-- logico/core/templates/core/orden_form.html -->
<form method="post">
    {% csrf_token %}
    ...
</form>
```

**Evidencia:**
- Middleware activo en `settings.py`
- Token CSRF en todos los formularios HTML
- Validación automática en todas las peticiones POST

**Protección:** Previene que sitios maliciosos ejecuten acciones en nombre de usuarios autenticados.

---

## 2. Autenticación Requerida (Authentication Required)

### Descripción
Garantiza que solo usuarios autenticados puedan acceder a las vistas protegidas.

### Implementación

**Ubicación:** `logico/core/views.py`

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Dashboard principal con estadísticas"""
    ...
```

**Ubicación API:** `logico/core/api_views.py`

```python
from rest_framework.permissions import IsAuthenticated

class OrdenViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    ...
```

**Configuración Global:** `logico/logico/settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    ...
}
```

**Evidencia:**
- Decorador `@login_required` en todas las vistas web
- `IsAuthenticated` en todos los ViewSets de la API
- Redirección automática a `/login/` si no está autenticado

**Protección:** Previene acceso no autorizado a funcionalidades del sistema.

---

## 3. Control de Acceso Basado en Roles (RBAC)

### Descripción
Sistema de permisos que restringe acciones según el rol del usuario (admin, coordinador, repartidor).

### Implementación

**Ubicación:** `logico/core/views.py`

```python
@login_required
def usuario_create(request):
    """Crear nuevo usuario - Solo admin"""
    user_profile, _ = UsuarioProfile.objects.get_or_create(...)
    
    # Solo admin puede crear usuarios
    if user_profile.rol != 'admin':
        messages.error(request, 'No tienes permisos para crear usuarios.')
        return redirect('usuario_list')
    ...
```

**Ejemplo de Validación por Rol:**

```python
# Solo coordinador o admin pueden asignar repartidores
if user_profile.rol == 'repartidor':
    messages.error(request, 'No tienes permisos para asignar repartidores.')
    return redirect('orden_detail', pk=pk)
```

**En Templates:** `logico/core/templates/base.html`

```html
{% if user.profile and user.profile.rol == 'admin' or user.profile and user.profile.rol == 'coordinador' %}
    <a href="{% url 'moto_create' %}" class="btn btn-primary">Nueva Moto</a>
{% endif %}
```

**Evidencia:**
- Validaciones de rol en todas las vistas críticas
- Ocultación de botones según permisos en templates
- Mensajes de error claros cuando se intenta acceder sin permisos

**Protección:** Previene que usuarios realicen acciones fuera de su alcance de responsabilidad.

---

## 4. Validación de Contraseñas

### Descripción
Validación robusta de contraseñas para garantizar seguridad mínima.

### Implementación

**Ubicación:** `logico/logico/settings.py`

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # Evita contraseñas similares al username
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Longitud mínima de 8 caracteres
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # Evita contraseñas comunes
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # Evita contraseñas completamente numéricas
    },
]
```

**En Formularios:** `logico/core/forms.py`

```python
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
    )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # Encriptación automática
        ...
```

**Evidencia:**
- 4 validadores de contraseña activos
- Encriptación automática con algoritmo PBKDF2
- Validación en formularios de creación/edición

**Protección:** Previene contraseñas débiles y garantiza encriptación segura.

---

## 5. Prevención de SQL Injection

### Descripción
Uso del ORM de Django para prevenir inyección SQL mediante consultas parametrizadas.

### Implementación

**Ubicación:** Todo el código que accede a la base de datos

**Ejemplo Seguro:**
```python
# ✅ CORRECTO - Usa ORM (protección automática)
ordenes = Orden.objects.filter(
    estado_actual='despacho',
    responsable=user_profile
)

# ❌ INCORRECTO - Nunca se usa SQL directo sin parámetros
# cursor.execute(f"SELECT * FROM core_orden WHERE estado = '{estado}'")
```

**Ejemplo con Filtros Seguros:**
```python
# logico/core/views.py
despachos = Despacho.objects.filter(
    estado=estado,  # Parámetro seguro
    resultado=resultado  # Parámetro seguro
)
```

**Evidencia:**
- Uso exclusivo del ORM de Django
- No hay consultas SQL directas en el código
- Filtros siempre parametrizados

**Protección:** Previene inyección SQL mediante consultas parametrizadas automáticas.

---

## 6. Protección XSS (Cross-Site Scripting)

### Descripción
Auto-escaping de Django previene la ejecución de scripts maliciosos en templates.

### Implementación

**Ubicación:** Todos los templates HTML

**Ejemplo:**
```html
<!-- logico/core/templates/core/orden_detail.html -->
<h1>Orden #{{ orden.id }}</h1>
<p>{{ orden.cliente }}</p>  <!-- Auto-escaped automáticamente -->
```

**Para Contenido Seguro:**
```html
{{ orden.descripcion|safe }}  <!-- Solo cuando es necesario y confiable -->
```

**Configuración:** `logico/logico/settings.py`

```python
TEMPLATES = [{
    'OPTIONS': {
        'autoescape': True,  # Activado por defecto
    }
}]
```

**Evidencia:**
- Auto-escaping activo en todos los templates
- Uso de `|escapejs` para JavaScript
- Validación de entrada en formularios

**Protección:** Previene ejecución de scripts maliciosos en el navegador del usuario.

---

## 7. Seguridad de Sesiones

### Descripción
Gestión segura de sesiones con protección contra secuestro de sesión.

### Implementación

**Ubicación:** `logico/logico/settings.py`

```python
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gestión de sesiones
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticación
    ...
]

SESSION_COOKIE_HTTPONLY = True  # Previene acceso JavaScript a cookies
SESSION_COOKIE_SECURE = False  # True en producción con HTTPS
SESSION_COOKIE_SAMESITE = 'Lax'  # Protección CSRF adicional
```

**Evidencia:**
- Cookies de sesión con flag HttpOnly
- Timeout de sesión configurado
- Regeneración de ID de sesión en login

**Protección:** Previene secuestro de sesión y acceso no autorizado.

---

## 8. Autenticación por Token (API)

### Descripción
Autenticación mediante tokens para acceso seguro a la API REST.

### Implementación

**Ubicación:** `logico/logico/settings.py`

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',  # ← Token Auth
    ],
    ...
}
```

**Uso en API:**
```python
# Obtener token
POST /api/token/
{
    "username": "admin",
    "password": "admin123"
}

# Usar token
GET /api/ordenes/
Headers: Authorization: Token <token_value>
```

**Evidencia:**
- TokenAuthentication configurado
- Tokens únicos por usuario
- Expiración y renovación de tokens

**Protección:** Permite acceso seguro a la API sin exponer credenciales.

---

## 9. Validación de Entrada (Input Validation)

### Descripción
Validación exhaustiva de datos de entrada en formularios y API.

### Implementación

**Ubicación:** `logico/core/forms.py`

```python
class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'direccion', ...]
    
    def clean(self):
        cleaned_data = super().clean()
        # Validaciones personalizadas
        ...
        return cleaned_data
```

**Validación en Modelos:**
```python
# logico/core/models.py
class Moto(models.Model):
    año = models.IntegerField(validators=[MinValueValidator(1900)])
    cilindrada = models.IntegerField(validators=[MinValueValidator(0)])
```

**Evidencia:**
- Validación en formularios Django
- Validadores en modelos
- Sanitización de entrada

**Protección:** Previene datos inválidos y maliciosos en la base de datos.

---

## 10. Protección Clickjacking

### Descripción
Previene que el sitio sea embebido en iframes maliciosos.

### Implementación

**Ubicación:** `logico/logico/settings.py`

```python
MIDDLEWARE = [
    ...
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # ← Protección
]

X_FRAME_OPTIONS = 'DENY'  # Previene embedding en iframes
```

**Evidencia:**
- Middleware XFrameOptions activo
- Header X-Frame-Options en todas las respuestas

**Protección:** Previene ataques de clickjacking.

---

## 11. Filtrado de Datos por Usuario

### Descripción
Los usuarios solo pueden acceder a sus propios datos según su rol.

### Implementación

**Ubicación:** `logico/core/views.py`

```python
@login_required
def orden_list(request):
    user_profile, _ = UsuarioProfile.objects.get_or_create(...)
    
    # Filtros según rol
    if user_profile.rol == 'repartidor':
        ordenes = ordenes.filter(responsable=user_profile)  # Solo sus órdenes
    ...
```

**En API:** `logico/core/api_views.py`

```python
def get_queryset(self):
    user_profile, _ = UsuarioProfile.objects.get_or_create(...)
    if user_profile.rol == 'repartidor':
        return Orden.objects.filter(responsable=user_profile)
    return Orden.objects.all()
```

**Evidencia:**
- Filtrado automático según rol
- Validación de propiedad de recursos
- Prevención de acceso horizontal

**Protección:** Previene que usuarios accedan a datos de otros usuarios.

---

## 12. Exclusión de Administradores como Repartidores

### Descripción
Validación que previene asignar usuarios administradores como repartidores.

### Implementación

**Ubicación:** `logico/core/views.py`

```python
@login_required
def asignar_repartidor(request, pk):
    repartidor = get_object_or_404(UsuarioProfile, pk=repartidor_id, rol='repartidor')
    
    # Validar que no sea admin
    if repartidor.user.is_superuser:
        messages.error(request, 'No se puede asignar un administrador como repartidor.')
        return redirect('orden_detail', pk=pk)
    ...
```

**En Formularios:** `logico/core/forms.py`

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Excluir admin de la lista de repartidores
    self.fields['responsable'].queryset = UsuarioProfile.objects.filter(
        rol='repartidor', 
        activo=True
    ).exclude(user__is_superuser=True)
```

**Evidencia:**
- Validación en vistas
- Filtrado en formularios
- Mensajes de error claros

**Protección:** Mantiene separación de roles y previene conflictos de permisos.

---

## Resumen de Patrones Implementados

| # | Patrón | Ubicación | Estado |
|---|--------|-----------|--------|
| 1 | CSRF Protection | Middleware + Templates | ✅ Implementado |
| 2 | Authentication Required | Views + API | ✅ Implementado |
| 3 | Role-Based Access Control | Views + Templates | ✅ Implementado |
| 4 | Password Validation | Settings + Forms | ✅ Implementado |
| 5 | SQL Injection Prevention | ORM Django | ✅ Implementado |
| 6 | XSS Protection | Auto-escaping | ✅ Implementado |
| 7 | Session Security | Settings | ✅ Implementado |
| 8 | Token Authentication | API | ✅ Implementado |
| 9 | Input Validation | Forms + Models | ✅ Implementado |
| 10 | Clickjacking Protection | Middleware | ✅ Implementado |
| 11 | Data Filtering by User | Views + API | ✅ Implementado |
| 12 | Admin Exclusion | Views + Forms | ✅ Implementado |

---

## Recomendaciones Adicionales para Producción

1. **HTTPS:** Activar `SESSION_COOKIE_SECURE = True` y `CSRF_COOKIE_SECURE = True`
2. **SECRET_KEY:** Usar variable de entorno, nunca en código
3. **DEBUG:** Desactivar en producción (`DEBUG = False`)
4. **ALLOWED_HOSTS:** Configurar dominios específicos
5. **Rate Limiting:** Implementar límites de peticiones por IP
6. **Logging:** Registrar intentos de acceso no autorizados
7. **Backup:** Implementar respaldos automáticos de la base de datos

---

## Conclusión

El sistema LogiCo implementa **12 patrones de seguridad** fundamentales que protegen contra las vulnerabilidades más comunes en aplicaciones web. La combinación de estas medidas proporciona múltiples capas de defensa, siguiendo el principio de "defensa en profundidad".

