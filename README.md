# LogiCo - Sistema de Logística Farmacéutica

Sistema completo de logística farmacéutica para retiro de recetas, traslado de medicamentos, despacho y re-despacho.

## 🚀 Tecnologías

- **Python 3.10+**
- **Django 4.2+**
- **Django REST Framework**
- **PostgreSQL**
- **Bootstrap 5** (CDN)
- **Chart.js** para dashboard
- **Swagger + Redoc** para documentación API

## 📋 Requisitos Previos

- Python 3.10 o superior
- PostgreSQL instalado y ejecutándose
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd logico
```

### 2. Crear entorno virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

Crear una base de datos en PostgreSQL:

```sql
CREATE DATABASE logico_db;
CREATE USER logico_user WITH PASSWORD 'tu_password';
ALTER ROLE logico_user SET client_encoding TO 'utf8';
ALTER ROLE logico_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE logico_user SET timezone TO 'America/Santiago';
GRANT ALL PRIVILEGES ON DATABASE logico_db TO logico_user;
```

### 5. Configurar variables de entorno (opcional)

Puedes configurar las variables de entorno o modificar directamente `logico/settings.py`:

**Windows (PowerShell):**
```powershell
$env:DB_NAME="logico_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="123"
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
```

**Linux/Mac:**
```bash
export DB_NAME=logico_db
export DB_USER=postgres
export DB_PASSWORD=123
export DB_HOST=localhost
export DB_PORT=5432
```

O modifica directamente en `logico/logico/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'logico_db',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Ejecutar migraciones

```bash
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

### 8. Cargar datos de prueba (opcional)

```bash
python manage.py seed_data
```

Esto creará:
- 1 administrador (admin / admin123)
- 2 coordinadores (coordinador1 / coordinador123)
- 3 repartidores (repartidor1 / repartidor123)
- 5 motos
- 10 órdenes con medicamentos
- Despachos de prueba
- Rutas
- Reportes

### 9. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

El sistema estará disponible en: http://127.0.0.1:8000/

## 📚 Documentación API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/

## 👥 Usuarios de Prueba

Si ejecutaste el comando `seed_data`, puedes usar:

- **Admin**: usuario: `admin` / contraseña: `admin123`
- **Coordinador**: usuario: `coordinador1` / contraseña: `coordinador123`
- **Repartidor**: usuario: `repartidor1` / contraseña: `repartidor123`

## 🎯 Funcionalidades Principales

### Roles y Permisos

- **Admin**: Acceso total al sistema
- **Coordinador**: Gestiona órdenes, rutas, motos y reportes
- **Repartidor**: Ve solo sus órdenes, registra despachos y re-despachos

### Módulos

1. **Dashboard**: Estadísticas y gráficos con Chart.js
2. **Órdenes**: Gestión completa de órdenes de medicamentos
3. **Despachos**: Registro de intentos de entrega con re-despachos
4. **Motos**: Gestión de flota de motos
5. **Reportes**: Reportes diarios con exportación CSV
6. **Rutas**: Optimización de rutas con Google Maps

### Estados del Sistema

- **RETIRO DE RECETA** → `retiro_receta`
- **TRASLADO** → `traslado`
- **DESPACHO** → `despacho`
- **RE-DESPACHO** → `re_despacho`

## 🔌 API REST

El sistema incluye una API REST completa con los siguientes endpoints:

- `/api/usuarios/` - Gestión de usuarios
- `/api/motos/` - Gestión de motos
- `/api/ordenes/` - Gestión de órdenes
- `/api/medicamentos/` - Gestión de medicamentos
- `/api/despachos/` - Gestión de despachos
- `/api/movimientos/` - Historial de movimientos (solo lectura)
- `/api/rutas/` - Gestión de rutas
- `/api/reportes/` - Gestión de reportes

### Autenticación API

La API soporta dos métodos de autenticación:
- **Session Authentication**: Para uso desde el navegador
- **Token Authentication**: Para uso desde aplicaciones externas

Para obtener un token:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

## 📁 Estructura del Proyecto

```
logico/
├── manage.py
├── logico/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas web
│   ├── api_views.py       # ViewSets para API
│   ├── serializers.py     # Serializers DRF
│   ├── forms.py           # Formularios
│   ├── admin.py           # Configuración admin
│   ├── urls.py            # URLs web
│   ├── api_urls.py        # URLs API
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py  # Comando para datos de prueba
│   ├── templates/         # Templates HTML
│   └── static/            # Archivos estáticos
├── media/                 # Archivos subidos
├── staticfiles/           # Archivos estáticos recopilados
└── requirements.txt
```

## 🛠️ Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba
python manage.py seed_data

# Recopilar archivos estáticos
python manage.py collectstatic

# Acceder al shell de Django
python manage.py shell
```

## 📝 Notas

- El sistema está configurado para usar PostgreSQL. Asegúrate de tenerlo instalado y configurado.
- Los archivos de medios (fotos) se guardan en la carpeta `media/`.
- Los archivos estáticos se recopilan en `staticfiles/` cuando se ejecuta `collectstatic`.

## 🐛 Solución de Problemas

### Error de conexión a PostgreSQL

Verifica que PostgreSQL esté ejecutándose y que las credenciales en `settings.py` sean correctas.

### Error de migraciones

Si hay problemas con las migraciones, puedes eliminarlas y recrearlas:

```bash
python manage.py makemigrations core
python manage.py migrate
```

### Error de archivos estáticos

Asegúrate de ejecutar:

```bash
python manage.py collectstatic
```

## 📄 Licencia

Este proyecto es de uso educativo.

## 👨‍💻 Autor

Proyecto desarrollado para el curso de Proyecto Integrado.

---

¡Disfruta usando LogiCo! 🚀

