Quiero que generes un proyecto completo llamado LogiCo, un sistema de logística farmacéutica para retiro de recetas, traslado de medicamentos, despacho y re-despacho.
El proyecto debe usar solo Django + PostgreSQL + Bootstrap 5 + Django REST Framework, sin Docker ni React.

🔧 1. Tecnologías obligatorias

Python 3.10+

Django 4.2+

Django REST Framework

Django Filter

PostgreSQL

Bootstrap 5 (CDN)

Chart.js para dashboard

Swagger + Redoc para documentación API

Autenticación: Session + Token

🗂 2. Estructura general del proyecto
logico/
  manage.py
  logico/ (settings, urls)
  core/
    models.py
    views.py
    urls.py
    serializers.py
    forms.py
    admin.py
    templates/
      base.html
      registration/login.html
      core/*.html
    static/core/css/custom.css
  media/
  staticfiles/

🧩 3. Modelos requeridos

Debes incluir estos modelos con las relaciones exactas:

3.1 Usuario (extiende User)

UsuarioProfile

user (OneToOneField)

rut (opcional)

telefono

rol (admin, coordinador, repartidor)

foto (opcional)

moto (OneToOne hacia Moto, opcional)

estado_turno (disponible / ocupado / descanso)

fecha_creacion

activo (bool)

3.2 Moto

patente (única)

marca

modelo

año

color

cilindrada

kilometraje

estado (disponible / en_uso / mantenimiento / fuera_servicio)

fecha_ingreso

fecha_ultimo_mantenimiento

proximo_mantenimiento

observaciones

activa (bool)

Propiedades:

repartidor_asignado

dias_sin_mantenimiento

3.3 Orden

Representa la orden del paciente:

id

cliente

direccion

telefono_cliente

descripcion

prioridad (alta / media / baja)

tipo (receta_detendida, normal)

estado_actual (retiro_receta / traslado / despacho / re_despacho)

responsable (FK a UsuarioProfile, opcional)

fecha_creacion

fecha_actualizacion

Reglas:

La prioridad es automática por defecto según:

receta detenida → alta

remedio normal → media

sin tags → baja

Puede ser editada manualmente.

3.4 Medicamento

Cada orden puede incluir varios medicamentos:

orden (FK)

codigo

nombre

cantidad

observaciones

3.5 Despacho (Intentos de entrega)

Cada intento de entrega genera un despacho independiente.

id

orden (FK)

numero_despacho (incremental por orden)

repartidor (FK)

estado (despacho / re_despacho)

resultado (entregado / no_disponible / error)

foto_entrega (opcional)

observaciones

coordenadas_lat (opcional)

coordenadas_lng (opcional)

fecha

Regla fundamental:

El ID de la orden nunca cambia.

Solo incrementa el id del despacho
(1, 2, 3… hasta que se entregue).

3.6 OrdenMovimiento (Historial de estados)

Cada cambio de estado de la orden genera un registro aquí:

orden (FK)

estado (retiro_receta / traslado / despacho / re_despacho)

descripcion

repartidor (FK)

despacho (FK opcional)

timestamp

Esto permite trazabilidad completa.

3.7 Ruta

Rutas opcionales para optimización:

nombre

descripcion

zona

vehiculo

repartidor (FK)

activa (bool)

ordenes (ManyToMany)

Debe generar link de Google Maps con múltiples destinos.

3.8 Reporte

Para dashboard y PDF/CSV:

fecha

entregas_totales

entregas_exitosas

entregas_fallidas

tiempo_promedio

ingresos_dia

observaciones

Propiedad:

tasa_exito

Generación: automática todos los días (management command).

🧠 4. Estados obligatorios

Los estados del sistema son EXACTAMENTE estos 4:

RETIRO DE RECETA → retiro_receta

TRASLADO → traslado

DESPACHO → despacho

RE-DESPACHO → re_despacho

Regla:
Cada cambio → un registro en OrdenMovimiento.

🔐 5. Permisos (Roles)
Admin:

Acceso total

Coordinador:

Gestiona órdenes, rutas, motos, reportes

Repartidor:

Ve solo sus órdenes

Registra despachos y re-despachos

Puede cargar fotos

Marca estados

🌐 6. API REST (DRF)

Crear ViewSets para:

UsuarioViewSet

OrdenViewSet (acción: cambiar_estado, asignar_repartidor)

MedicamentoViewSet

DespachoViewSet (acción: registrar_resultado)

MovimientoViewSet (solo lectura)

MotoViewSet (acciones: asignar, desasignar, mantenimiento)

RutaViewSet (multi-destino Google Maps)

ReporteViewSet (dashboard, export CSV)

Incluir:

Swagger

Redoc

🎨 7. Templates con Bootstrap 5

Usar sidebar estilo AdminLTE, pero solo con Bootstrap (sin AdminLTE real).

Templates obligatorios:

base.html

login.html

dashboard.html

orden_list.html

orden_form.html

orden_detail.html

despacho_list.html

despacho_form.html

moto_list.html

moto_form.html

reporte_list.html

Componentes:

cards

tablas con paginación

badges de estado

modals

alerts

filtros

DataTables opcional

📊 8. Dashboard con Chart.js

Mostrar:

Total órdenes

Órdenes por estado

Intentos de despacho

Tasa de éxito

Repartidores activos

Motos activas

Gráfico línea → entregas por día

Gráfico doughnut → resultados de despacho

📍 9. Funcionalidades especiales
9.1 Generar link automático Google Maps

Con múltiples destinos:

https://www.google.com/maps/dir/?api=1&destination=<destino>&waypoints=<waypoints>

9.2 Carga de fotos

Foto de entrega

Foto opcional del repartidor

Foto de la moto

9.3 Validaciones complejas

No asignar orden a repartidor sin moto

No asignar moto en mantenimiento

Control de kilometraje

Repartidor no puede tener 2 turnos activos

Cada despacho crea un id único incremental por orden

9.4 Auditoría

Registrar:

quién creó

quién editó

quién cambió estado

desde qué IP (opcional)

cuándo

📦 10. Semillas iniciales

Crear datos falsos:

3 repartidores chilenos

2 coordinadores

1 admin

5 motos

10 órdenes

medicamentos asociados

Nombres deben ser chilenos por defecto.

🧭 11. Incluir instrucciones para ejecutar

crear entorno

instalar requirements

configurar PostgreSQL

migrar

crear superusuario

ejecutar servidor

🏁 OBJETIVO FINAL DEL PROMPT

Con toda esta información, quiero que generes:

Modelos completos

Serializers

ViewSets

Forms

Templates Bootstrap

URLs

Dashboard

Permisos

Historial de movimientos

Módulo de despachos con reintentos

Ruta con Google Maps

Reportes PDF y CSV

Seed de datos

Swagger + Redoc

Todo funcionando

El resultado final debe ser un proyecto LISTO PARA USAR, totalmente funcional y coherente.