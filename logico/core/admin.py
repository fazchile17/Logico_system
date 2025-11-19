from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UsuarioProfile, Moto, Orden, Medicamento,
    Despacho, OrdenMovimiento, Ruta, Reporte, Farmacia
)


class UsuarioProfileInline(admin.StackedInline):
    model = UsuarioProfile
    can_delete = False
    verbose_name_plural = 'Perfil'


class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UsuarioProfile)
class UsuarioProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'telefono', 'estado_turno', 'activo']
    list_filter = ['rol', 'estado_turno', 'activo']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'rut']


@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ['patente', 'marca', 'modelo', 'estado', 'activa']
    list_filter = ['estado', 'activa', 'marca']
    search_fields = ['patente', 'marca', 'modelo']


class MedicamentoInline(admin.TabularInline):
    model = Medicamento
    extra = 1


@admin.register(Farmacia)
class FarmaciaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'telefono', 'activa']
    list_filter = ['activa', 'ciudad']
    search_fields = ['nombre', 'direccion', 'ciudad']


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'estado_actual', 'prioridad', 'farmacia_origen', 'farmacia_destino', 'responsable', 'fecha_creacion']
    list_filter = ['estado_actual', 'prioridad', 'tipo', 'fecha_creacion', 'farmacia_origen', 'farmacia_destino']
    search_fields = ['cliente', 'direccion', 'telefono_cliente']
    inlines = [MedicamentoInline]


@admin.register(Despacho)
class DespachoAdmin(admin.ModelAdmin):
    list_display = ['id', 'orden', 'numero_despacho', 'repartidor', 'estado', 'resultado', 'fecha']
    list_filter = ['estado', 'resultado', 'fecha']
    search_fields = ['orden__cliente', 'repartidor__user__username']


@admin.register(OrdenMovimiento)
class OrdenMovimientoAdmin(admin.ModelAdmin):
    list_display = ['orden', 'estado', 'repartidor', 'timestamp']
    list_filter = ['estado', 'timestamp']
    search_fields = ['orden__cliente']


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'zona', 'repartidor', 'activa']
    list_filter = ['activa', 'zona']
    search_fields = ['nombre', 'zona']
    filter_horizontal = ['ordenes']


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'entregas_totales', 'entregas_exitosas', 'entregas_fallidas', 'tasa_exito']
    list_filter = ['fecha']
    readonly_fields = ['tasa_exito']

