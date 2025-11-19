from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
from core.models import Despacho, Reporte


class Command(BaseCommand):
    help = 'Genera reporte diario automático'

    def handle(self, *args, **options):
        fecha = timezone.now().date()
        
        # Verificar si ya existe un reporte para hoy
        if Reporte.objects.filter(fecha=fecha).exists():
            self.stdout.write(self.style.WARNING(f'Ya existe un reporte para la fecha {fecha}'))
            return
        
        # Obtener despachos del día
        despachos_dia = Despacho.objects.filter(fecha__date=fecha)
        
        entregas_totales = despachos_dia.count()
        entregas_exitosas = despachos_dia.filter(resultado='entregado').count()
        entregas_fallidas = despachos_dia.filter(
            Q(resultado='no_disponible') | Q(resultado='error')
        ).count()
        
        # Calcular tiempo promedio (simplificado)
        tiempo_promedio = timedelta(minutes=30)  # Valor por defecto
        
        # Crear reporte
        reporte = Reporte.objects.create(
            fecha=fecha,
            entregas_totales=entregas_totales,
            entregas_exitosas=entregas_exitosas,
            entregas_fallidas=entregas_fallidas,
            tiempo_promedio=tiempo_promedio,
            ingresos_dia=0,  # Se puede calcular según lógica de negocio
            observaciones=f'Reporte automático generado el {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}',
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Reporte creado para {fecha}'))
        self.stdout.write(self.style.SUCCESS(f'  Entregas totales: {entregas_totales}'))
        self.stdout.write(self.style.SUCCESS(f'  Entregas exitosas: {entregas_exitosas}'))
        self.stdout.write(self.style.SUCCESS(f'  Entregas fallidas: {entregas_fallidas}'))
        self.stdout.write(self.style.SUCCESS(f'  Tasa de éxito: {reporte.tasa_exito:.2f}%'))

