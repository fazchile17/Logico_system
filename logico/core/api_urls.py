from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    UsuarioViewSet, MotoViewSet, OrdenViewSet, MedicamentoViewSet,
    DespachoViewSet, MovimientoViewSet, RutaViewSet, ReporteViewSet, FarmaciaViewSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'motos', MotoViewSet, basename='moto')
router.register(r'ordenes', OrdenViewSet, basename='orden')
router.register(r'medicamentos', MedicamentoViewSet, basename='medicamento')
router.register(r'despachos', DespachoViewSet, basename='despacho')
router.register(r'movimientos', MovimientoViewSet, basename='movimiento')
router.register(r'rutas', RutaViewSet, basename='ruta')
router.register(r'reportes', ReporteViewSet, basename='reporte')
router.register(r'farmacias', FarmaciaViewSet, basename='farmacia')

urlpatterns = [
    path('', include(router.urls)),
]

