from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UsuarioProfile, Moto, Orden, Medicamento, 
    Despacho, OrdenMovimiento, Ruta, Reporte, Farmacia
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UsuarioProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    moto_patente = serializers.CharField(source='moto.patente', read_only=True)
    
    class Meta:
        model = UsuarioProfile
        fields = [
            'id', 'user', 'rut', 'telefono', 'rol', 'foto', 
            'moto', 'moto_patente', 'estado_turno', 
            'fecha_creacion', 'activo'
        ]
        read_only_fields = ['fecha_creacion']


class MotoSerializer(serializers.ModelSerializer):
    repartidor_nombre = serializers.CharField(source='repartidor_asignado.user.get_full_name', read_only=True)
    dias_sin_mantenimiento = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Moto
        fields = [
            'id', 'patente', 'marca', 'modelo', 'año', 'color', 
            'cilindrada', 'kilometraje', 'estado', 'fecha_ingreso',
            'fecha_ultimo_mantenimiento', 'proximo_mantenimiento',
            'observaciones', 'activa', 'repartidor_nombre', 
            'dias_sin_mantenimiento'
        ]
        read_only_fields = ['fecha_ingreso']


class FarmaciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmacia
        fields = ['id', 'nombre', 'direccion', 'telefono', 'ciudad', 'activa']


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ['id', 'orden', 'codigo', 'nombre', 'cantidad', 'observaciones']


class OrdenSerializer(serializers.ModelSerializer):
    medicamentos = MedicamentoSerializer(many=True, read_only=True)
    responsable_nombre = serializers.CharField(source='responsable.user.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_actual_display', read_only=True)
    farmacia_origen_nombre = serializers.CharField(source='farmacia_origen.nombre', read_only=True)
    farmacia_destino_nombre = serializers.CharField(source='farmacia_destino.nombre', read_only=True)
    
    class Meta:
        model = Orden
        fields = [
            'id', 'cliente', 'direccion', 'telefono_cliente', 'descripcion',
            'prioridad', 'tipo', 'estado_actual', 'estado_display',
            'farmacia_origen', 'farmacia_origen_nombre',
            'farmacia_destino', 'farmacia_destino_nombre',
            'responsable', 'responsable_nombre', 'fecha_creacion',
            'fecha_actualizacion', 'medicamentos'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']


class DespachoSerializer(serializers.ModelSerializer):
    orden_cliente = serializers.CharField(source='orden.cliente', read_only=True)
    orden_direccion = serializers.CharField(source='orden.direccion', read_only=True)
    repartidor_nombre = serializers.CharField(source='repartidor.user.get_full_name', read_only=True)
    
    class Meta:
        model = Despacho
        fields = [
            'id', 'orden', 'orden_cliente', 'orden_direccion',
            'numero_despacho', 'repartidor', 'repartidor_nombre',
            'estado', 'resultado', 'foto_entrega', 'observaciones',
            'coordenadas_lat', 'coordenadas_lng', 'fecha'
        ]
        read_only_fields = ['fecha', 'numero_despacho']


class OrdenMovimientoSerializer(serializers.ModelSerializer):
    orden_cliente = serializers.CharField(source='orden.cliente', read_only=True)
    repartidor_nombre = serializers.CharField(source='repartidor.user.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = OrdenMovimiento
        fields = [
            'id', 'orden', 'orden_cliente', 'estado', 'estado_display',
            'descripcion', 'repartidor', 'repartidor_nombre',
            'despacho', 'timestamp'
        ]
        read_only_fields = ['timestamp']


class RutaSerializer(serializers.ModelSerializer):
    repartidor_nombre = serializers.CharField(source='repartidor.user.get_full_name', read_only=True)
    ordenes_count = serializers.IntegerField(source='ordenes.count', read_only=True)
    google_maps_url = serializers.CharField(source='get_google_maps_url', read_only=True)
    ordenes = OrdenSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ruta
        fields = [
            'id', 'nombre', 'descripcion', 'zona', 'vehiculo',
            'repartidor', 'repartidor_nombre', 'activa',
            'ordenes', 'ordenes_count', 'google_maps_url', 'fecha_creacion'
        ]
        read_only_fields = ['fecha_creacion']


class ReporteSerializer(serializers.ModelSerializer):
    tasa_exito = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Reporte
        fields = [
            'id', 'fecha', 'entregas_totales', 'entregas_exitosas',
            'entregas_fallidas', 'tiempo_promedio', 'ingresos_dia',
            'tasa_exito', 'observaciones', 'fecha_creacion'
        ]
        read_only_fields = ['fecha_creacion']

