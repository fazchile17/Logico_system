from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import (
    UsuarioProfile, Moto, Orden, Medicamento, 
    Despacho, OrdenMovimiento, Ruta, Reporte, Farmacia
)
from .serializers import (
    UsuarioProfileSerializer, MotoSerializer, OrdenSerializer,
    MedicamentoSerializer, DespachoSerializer, OrdenMovimientoSerializer,
    RutaSerializer, ReporteSerializer, FarmaciaSerializer
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = UsuarioProfile.objects.all()
    serializer_class = UsuarioProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rol', 'estado_turno', 'activo']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'rut']
    ordering_fields = ['fecha_creacion', 'user__username']
    
    def get_queryset(self):
        user_profile, _ = UsuarioProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'telefono': '',
                'rol': 'repartidor',
                'estado_turno': 'disponible',
                'activo': True,
            }
        )
        if user_profile.rol == 'repartidor':
            return UsuarioProfile.objects.filter(pk=user_profile.pk)
        return UsuarioProfile.objects.all()


class MotoViewSet(viewsets.ModelViewSet):
    queryset = Moto.objects.all()
    serializer_class = MotoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado', 'activa', 'marca']
    search_fields = ['patente', 'marca', 'modelo']
    ordering_fields = ['patente', 'fecha_ingreso']
    
    @action(detail=True, methods=['post'])
    def asignar(self, request, pk=None):
        """Asignar moto a repartidor - Solo coordinador o admin"""
        moto = self.get_object()
        user_profile, _ = UsuarioProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'telefono': '',
                'rol': 'repartidor',
                'estado_turno': 'disponible',
                'activo': True,
            }
        )
        
        # Solo coordinador o admin pueden asignar motos
        if user_profile.rol == 'repartidor':
            return Response({'error': 'No tienes permisos para asignar motos'}, status=status.HTTP_403_FORBIDDEN)
        
        repartidor_id = request.data.get('repartidor_id')
        
        if not repartidor_id:
            return Response({'error': 'repartidor_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            repartidor = UsuarioProfile.objects.get(pk=repartidor_id, rol='repartidor')
        except UsuarioProfile.DoesNotExist:
            return Response({'error': 'Repartidor no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Validar que no sea admin
        if repartidor.user.is_superuser:
            return Response({'error': 'No se puede asignar una moto a un administrador'}, status=status.HTTP_400_BAD_REQUEST)
        
        if moto.estado not in ['disponible', 'en_uso']:
            return Response({'error': 'La moto no está disponible'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Desasignar moto anterior
        if repartidor.moto and repartidor.moto != moto:
            repartidor.moto.estado = 'disponible'
            repartidor.moto.save()
        
        # Desasignar repartidor anterior de esta moto
        if moto.repartidor_asignado and moto.repartidor_asignado != repartidor:
            moto.repartidor_asignado.moto = None
            moto.repartidor_asignado.save()
        
        # Asignar nueva moto
        repartidor.moto = moto
        repartidor.save()
        moto.estado = 'en_uso'
        moto.save()
        
        return Response({'message': f'Moto {moto.patente} asignada a {repartidor.user.get_full_name()}'})
    
    @action(detail=True, methods=['post'])
    def desasignar(self, request, pk=None):
        """Desasignar moto de repartidor - Solo coordinador o admin"""
        moto = self.get_object()
        user_profile, _ = UsuarioProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'telefono': '',
                'rol': 'repartidor',
                'estado_turno': 'disponible',
                'activo': True,
            }
        )
        
        # Solo coordinador o admin pueden desasignar motos
        if user_profile.rol == 'repartidor':
            return Response({'error': 'No tienes permisos para desasignar motos'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            repartidor = moto.repartidor_asignado
            if repartidor:
                repartidor.moto = None
                repartidor.save()
                moto.estado = 'disponible'
                moto.save()
                return Response({'message': f'Moto {moto.patente} desasignada'})
            else:
                return Response({'error': 'La moto no tiene repartidor asignado'}, status=status.HTTP_400_BAD_REQUEST)
        except UsuarioProfile.DoesNotExist:
            return Response({'error': 'Repartidor no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def mantenimiento(self, request, pk=None):
        """Marcar moto en mantenimiento - Solo coordinador o admin"""
        moto = self.get_object()
        user_profile, _ = UsuarioProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'telefono': '',
                'rol': 'repartidor',
                'estado_turno': 'disponible',
                'activo': True,
            }
        )
        
        # Solo coordinador o admin pueden marcar motos en mantenimiento
        if user_profile.rol == 'repartidor':
            return Response({'error': 'No tienes permisos para marcar motos en mantenimiento'}, status=status.HTTP_403_FORBIDDEN)
        
        moto.estado = 'mantenimiento'
        moto.fecha_ultimo_mantenimiento = request.data.get('fecha_ultimo_mantenimiento')
        moto.proximo_mantenimiento = request.data.get('proximo_mantenimiento')
        moto.observaciones = request.data.get('observaciones', '')
        moto.save()
        
        return Response({'message': f'Moto {moto.patente} en mantenimiento'})


class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['estado_actual', 'prioridad', 'tipo', 'responsable']
    search_fields = ['cliente', 'direccion', 'telefono_cliente']
    ordering_fields = ['fecha_creacion', 'prioridad']
    
    def get_queryset(self):
        user_profile, _ = UsuarioProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'telefono': '',
                'rol': 'repartidor',
                'estado_turno': 'disponible',
                'activo': True,
            }
        )
        if user_profile.rol == 'repartidor':
            return Orden.objects.filter(responsable=user_profile)
        return Orden.objects.all()
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """Cambiar estado de orden"""
        orden = self.get_object()
        user_profile, _ = UsuarioProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'telefono': '',
                'rol': 'repartidor',
                'estado_turno': 'disponible',
                'activo': True,
            }
        )
        
        nuevo_estado = request.data.get('estado')
        descripcion = request.data.get('descripcion', '')
        
        if nuevo_estado not in dict(Orden.ESTADO_CHOICES):
            return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        estado_anterior = orden.estado_actual
        orden.estado_actual = nuevo_estado
        orden.save()
        
        # Registrar movimiento
        OrdenMovimiento.objects.create(
            orden=orden,
            estado=nuevo_estado,
            descripcion=descripcion or f'Estado cambiado de {estado_anterior} a {nuevo_estado}',
            repartidor=UsuarioProfile.objects.filter(user=request.user).first(),
        )
        
        return Response({'message': f'Estado cambiado a {nuevo_estado}'})
    
    @action(detail=True, methods=['post'])
    def asignar_repartidor(self, request, pk=None):
        """Asignar repartidor a orden - Solo coordinador o admin"""
        orden = self.get_object()
        user_profile, _ = UsuarioProfile.objects.get_or_create(
            user=request.user,
            defaults={
                'telefono': '',
                'rol': 'repartidor',
                'estado_turno': 'disponible',
                'activo': True,
            }
        )
        
        # Solo coordinador o admin pueden asignar repartidores
        if user_profile.rol == 'repartidor':
            return Response({'error': 'No tienes permisos para asignar repartidores'}, status=status.HTTP_403_FORBIDDEN)
        
        repartidor_id = request.data.get('repartidor_id')
        
        if not repartidor_id:
            return Response({'error': 'repartidor_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            repartidor = UsuarioProfile.objects.get(pk=repartidor_id, rol='repartidor')
        except UsuarioProfile.DoesNotExist:
            return Response({'error': 'Repartidor no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Validar que no sea admin
        if repartidor.user.is_superuser:
            return Response({'error': 'No se puede asignar un administrador como repartidor'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que tenga moto
        if not repartidor.moto:
            return Response({'error': 'El repartidor debe tener una moto asignada'}, status=status.HTTP_400_BAD_REQUEST)
        
        orden.responsable = repartidor
        orden.save()
        
        # Registrar movimiento
        OrdenMovimiento.objects.create(
            orden=orden,
            estado=orden.estado_actual,
            descripcion=f'Repartidor asignado: {repartidor.user.get_full_name()}',
            repartidor=repartidor,
        )
        
        return Response({'message': f'Repartidor {repartidor.user.get_full_name()} asignado'})


class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['orden']
    search_fields = ['nombre', 'codigo']


class DespachoViewSet(viewsets.ModelViewSet):
    queryset = Despacho.objects.all()
    serializer_class = DespachoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['orden', 'estado', 'resultado', 'repartidor']
    ordering_fields = ['fecha', 'numero_despacho']
    
    def get_queryset(self):
        user_profile, _ = UsuarioProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'telefono': '',
                'rol': 'repartidor',
                'estado_turno': 'disponible',
                'activo': True,
            }
        )
        if user_profile.rol == 'repartidor':
            return Despacho.objects.filter(repartidor=user_profile)
        return Despacho.objects.all()
    
    @action(detail=True, methods=['post'])
    def registrar_resultado(self, request, pk=None):
        """Registrar resultado de despacho"""
        despacho = self.get_object()
        resultado = request.data.get('resultado')
        observaciones = request.data.get('observaciones', '')
        foto_entrega = request.FILES.get('foto_entrega')
        coordenadas_lat = request.data.get('coordenadas_lat')
        coordenadas_lng = request.data.get('coordenadas_lng')
        
        if resultado not in dict(Despacho.RESULTADO_CHOICES):
            return Response({'error': 'Resultado inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        despacho.resultado = resultado
        despacho.observaciones = observaciones
        if foto_entrega:
            despacho.foto_entrega = foto_entrega
        if coordenadas_lat:
            despacho.coordenadas_lat = coordenadas_lat
        if coordenadas_lng:
            despacho.coordenadas_lng = coordenadas_lng
        despacho.save()
        
        # Actualizar estado de orden
        orden = despacho.orden
        if resultado == 'entregado':
            orden.estado_actual = 'despacho'
        else:
            orden.estado_actual = 're_despacho'
        orden.save()
        
        # Registrar movimiento
        OrdenMovimiento.objects.create(
            orden=orden,
            estado=orden.estado_actual,
            descripcion=f'Despacho #{despacho.numero_despacho} - {despacho.get_resultado_display()}',
            repartidor=despacho.repartidor,
            despacho=despacho,
        )
        
        return Response({'message': f'Resultado registrado: {resultado}'})


class MovimientoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrdenMovimiento.objects.all()
    serializer_class = OrdenMovimientoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['orden', 'estado', 'repartidor']
    ordering_fields = ['timestamp']


class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activa', 'zona', 'repartidor']
    search_fields = ['nombre', 'zona']
    ordering_fields = ['fecha_creacion', 'nombre']
    
    @action(detail=True, methods=['get'])
    def google_maps(self, request, pk=None):
        """Obtener URL de Google Maps para la ruta"""
        ruta = self.get_object()
        url = ruta.get_google_maps_url()
        if url:
            return Response({'url': url})
        return Response({'error': 'La ruta no tiene órdenes'}, status=status.HTTP_400_BAD_REQUEST)


class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['fecha']
    ordering_fields = ['fecha']
    
    @action(detail=True, methods=['get'])
    def export_csv(self, request, pk=None):
        """Exportar reporte a CSV"""
        import csv
        from django.http import HttpResponse
        
        reporte = self.get_object()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="reporte_{reporte.fecha}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Fecha', reporte.fecha])
        writer.writerow(['Entregas Totales', reporte.entregas_totales])
        writer.writerow(['Entregas Exitosas', reporte.entregas_exitosas])
        writer.writerow(['Entregas Fallidas', reporte.entregas_fallidas])
        writer.writerow(['Tasa de Éxito', f'{reporte.tasa_exito:.2f}%'])
        writer.writerow(['Ingresos del Día', reporte.ingresos_dia])
        writer.writerow(['Observaciones', reporte.observaciones])
        
        return response


class FarmaciaViewSet(viewsets.ModelViewSet):
    queryset = Farmacia.objects.filter(activa=True)
    serializer_class = FarmaciaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activa', 'ciudad']
    search_fields = ['nombre', 'direccion', 'ciudad']
    ordering_fields = ['nombre', 'ciudad']

