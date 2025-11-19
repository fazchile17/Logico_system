# Configuración de GitHub y Control de Versiones - LogiCo

## 1. Configuración del Repositorio

### 1.1. Creación del Repositorio

**Pasos Realizados:**

1. **Crear repositorio en GitHub:**
   - Nombre: `logico-sistema-logistica`
   - Visibilidad: Privado (o Público según requerimientos)
   - Descripción: "Sistema de logística farmacéutica - Django + PostgreSQL"

2. **Inicializar repositorio local:**
   ```bash
   git init
   git remote add origin https://github.com/usuario/logico-sistema-logistica.git
   ```

3. **Configuración inicial:**
   ```bash
   git config user.name "Tu Nombre"
   git config user.email "tu.email@ejemplo.com"
   ```

---

## 2. Estructura del Repositorio

### 2.1. Archivos de Configuración

**`.gitignore`** - Archivos excluidos del control de versiones:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
/media
/staticfiles
/static

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
```

**`README.md`** - Documentación principal del proyecto

**`requirements.txt`** - Dependencias del proyecto

---

## 3. Flujo de Trabajo con Git

### 3.1. Estrategia de Branching

**Rama Principal:**
- `main` o `master`: Código estable y en producción

**Ramas de Desarrollo:**
- `develop`: Integración de features
- `feature/nombre-funcionalidad`: Nuevas funcionalidades
- `fix/nombre-bug`: Correcciones
- `hotfix/nombre-urgente`: Correcciones urgentes

### 3.2. Comandos Básicos

#### Configuración Inicial
```bash
# Clonar repositorio
git clone https://github.com/usuario/logico-sistema-logistica.git
cd logico-sistema-logistica

# Configurar usuario
git config user.name "Tu Nombre"
git config user.email "tu.email@ejemplo.com"
```

#### Trabajo Diario
```bash
# Ver estado
git status

# Agregar cambios
git add archivo.py
git add .  # Todos los archivos

# Hacer commit
git commit -m "feat: Agregar gestión de usuarios"

# Subir cambios
git push origin nombre-rama

# Actualizar desde remoto
git pull origin nombre-rama
```

#### Crear y Trabajar con Branches
```bash
# Crear nueva rama
git checkout -b feature/gestión-usuarios

# Cambiar de rama
git checkout main

# Ver ramas
git branch

# Merge de rama
git checkout main
git merge feature/gestión-usuarios
```

---

## 4. Convenciones de Commits

### 4.1. Formato de Mensajes

**Estructura:**
```
tipo: descripción breve

Descripción detallada (opcional)

- Punto 1
- Punto 2
```

**Tipos de Commits:**
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, punto y coma, etc. (sin cambios de código)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Tareas de mantenimiento

**Ejemplos:**
```bash
git commit -m "feat: Agregar sistema de roles y permisos"
git commit -m "fix: Corregir validación de descanso de repartidor"
git commit -m "docs: Actualizar README con instrucciones de instalación"
git commit -m "refactor: Optimizar consultas de base de datos"
```

---

## 5. Pull Requests (PR)

### 5.1. Proceso de Pull Request

**Pasos:**

1. **Crear branch para la funcionalidad:**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Desarrollar y hacer commits:**
   ```bash
   git add .
   git commit -m "feat: Implementar nueva funcionalidad"
   git push origin feature/nueva-funcionalidad
   ```

3. **Crear Pull Request en GitHub:**
   - Ir a GitHub → Pull Requests → New Pull Request
   - Seleccionar branch origen y destino
   - Agregar descripción detallada

4. **Template de Pull Request:**
   ```markdown
   ## Descripción
   Breve descripción de los cambios realizados.

   ## Tipo de Cambio
   - [ ] Nueva funcionalidad
   - [ ] Corrección de bug
   - [ ] Mejora de rendimiento
   - [ ] Documentación

   ## Cambios Realizados
   - Cambio 1
   - Cambio 2
   - Cambio 3

   ## Testing
   - [ ] Tests unitarios pasando
   - [ ] Tests de integración pasando
   - [ ] Probado manualmente

   ## Screenshots (si aplica)
   [Agregar capturas de pantalla]

   ## Checklist
   - [ ] Código sigue las convenciones del proyecto
   - [ ] Documentación actualizada
   - [ ] Sin conflictos de merge
   - [ ] Revisado por al menos un miembro del equipo
   ```

5. **Revisión y Aprobación:**
   - Revisores asignados revisan el código
   - Comentarios y sugerencias
   - Aprobación y merge

---

## 6. Configuración de GitHub

### 6.1. Configuración del Repositorio

**Settings → General:**
- Description: "Sistema de logística farmacéutica"
- Topics: django, postgresql, logistics, pharmaceutical
- Visibility: Según requerimientos

**Settings → Branches:**
- Branch protection rules para `main`:
  - Require pull request reviews
  - Require status checks to pass
  - Require branches to be up to date

**Settings → Collaborators:**
- Agregar miembros del equipo
- Permisos: Write o Admin según rol

### 6.2. GitHub Actions (CI/CD) - Opcional

**`.github/workflows/django.yml`:**
```yaml
name: Django CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test
      env:
        DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db
```

---

## 7. Evidencias de Uso Colaborativo

### 7.1. Historial de Commits

**Ejemplo de Historial:**
```
* a1b2c3d (HEAD -> main) feat: Agregar gestión de usuarios
* e4f5g6h fix: Corregir validación de descanso
* i7j8k9l docs: Actualizar documentación API
* m1n2o3p refactor: Optimizar consultas de despachos
* q4r5s6t feat: Implementar sistema de roles
```

### 7.2. Pull Requests Creados

**Ejemplos:**
1. PR #1: "feat: Sistema de autenticación y roles"
2. PR #2: "feat: Gestión de órdenes y despachos"
3. PR #3: "fix: Corrección de validaciones"
4. PR #4: "docs: Documentación de API"

### 7.3. Issues y Discusiones

**Ejemplos de Issues:**
- Issue #1: "Implementar sistema de roles"
- Issue #2: "Bug: Validación de descanso no funciona"
- Issue #3: "Mejora: Optimizar consultas de base de datos"

---

## 8. Guía Paso a Paso para Nuevos Colaboradores

### 8.1. Configuración Inicial

```bash
# 1. Clonar repositorio
git clone https://github.com/usuario/logico-sistema-logistica.git
cd logico-sistema-logistica

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
# (Seguir instrucciones del README.md)

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Ejecutar servidor
python manage.py runserver
```

### 8.2. Flujo de Trabajo Diario

```bash
# 1. Actualizar desde remoto
git checkout main
git pull origin main

# 2. Crear branch para nueva funcionalidad
git checkout -b feature/mi-funcionalidad

# 3. Desarrollar y hacer commits
git add .
git commit -m "feat: Descripción de cambios"

# 4. Subir cambios
git push origin feature/mi-funcionalidad

# 5. Crear Pull Request en GitHub
# (Ir a GitHub y crear PR)

# 6. Esperar revisión y aprobación
# 7. Merge a main después de aprobación
```

---

## 9. Mejores Prácticas

### 9.1. Commits

✅ **Hacer:**
- Commits pequeños y frecuentes
- Mensajes descriptivos
- Un commit por funcionalidad lógica

❌ **Evitar:**
- Commits masivos con múltiples cambios
- Mensajes vagos como "fix" o "update"
- Commits con código comentado o de prueba

### 9.2. Branches

✅ **Hacer:**
- Crear branch por cada funcionalidad
- Nombres descriptivos
- Merge frecuente a develop

❌ **Evitar:**
- Trabajar directamente en main
- Branches muy largos sin merge
- Branches sin propósito claro

### 9.3. Pull Requests

✅ **Hacer:**
- Descripciones detalladas
- Revisar tu propio código antes de PR
- Responder a comentarios de revisión

❌ **Evitar:**
- PRs sin descripción
- PRs con código sin probar
- Ignorar feedback de revisores

---

## 10. Troubleshooting

### 10.1. Problemas Comunes

**Conflicto de Merge:**
```bash
# Actualizar branch local
git checkout main
git pull origin main

# Volver a tu branch y merge
git checkout feature/mi-branch
git merge main

# Resolver conflictos manualmente
# Luego:
git add .
git commit -m "fix: Resolver conflictos de merge"
```

**Deshacer último commit (sin push):**
```bash
git reset --soft HEAD~1  # Mantiene cambios
git reset --hard HEAD~1  # Elimina cambios
```

**Cambiar mensaje de último commit:**
```bash
git commit --amend -m "Nuevo mensaje"
```

---

## 11. Enlaces y Recursos

### 11.1. Documentación Oficial
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

### 11.2. Herramientas Útiles
- **GitHub Desktop:** Interfaz gráfica para Git
- **SourceTree:** Cliente Git visual
- **GitKraken:** Cliente Git con visualización de branches

---

## 12. Conclusión

El uso de GitHub y Git ha permitido:

✅ **Control de Versiones:** Historial completo de cambios
✅ **Colaboración:** Trabajo simultáneo sin conflictos
✅ **Trazabilidad:** Seguimiento de bugs y features
✅ **Documentación:** README y documentación en el repositorio
✅ **Calidad:** Code reviews y estándares de código

**Link del Repositorio:**
```
https://github.com/usuario/logico-sistema-logistica
```

**Nota:** Reemplazar `usuario` con el usuario real de GitHub del proyecto.

---

## 13. Checklist de Configuración

- [ ] Repositorio creado en GitHub
- [ ] `.gitignore` configurado
- [ ] `README.md` completo
- [ ] Branch protection rules configuradas
- [ ] Colaboradores agregados
- [ ] Template de Pull Request creado
- [ ] Template de Issues creado
- [ ] GitHub Actions configurado (opcional)
- [ ] Documentación de proceso de trabajo
- [ ] Evidencias de uso colaborativo

