"""
Pruebas de Rendimiento para LogiCo
Ejecutar: python test_rendimiento.py

Mide tiempos de respuesta de diferentes operaciones
"""

import os
import sys
import django
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logico.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import UsuarioProfile, Orden, Moto, Despacho
from django.db import connection
from django.db.models import Count

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def medir_tiempo(func):
    """Decorador para medir tiempo de ejecución"""
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        return fin - inicio, resultado
    return wrapper

@medir_tiempo
def test_consulta_simple():
    """Test: Consulta simple de órdenes"""
    ordenes = list(Orden.objects.all()[:10])
    return len(ordenes)

@medir_tiempo
def test_consulta_con_join():
    """Test: Consulta con JOIN (select_related)"""
    ordenes = list(Orden.objects.select_related('responsable', 'responsable__user').all()[:10])
    return len(ordenes)

@medir_tiempo
def test_consulta_con_agregacion():
    """Test: Consulta con agregación"""
    resultado = Orden.objects.aggregate(
        total=Count('id'),
        por_estado=Count('estado_actual')
    )
    return resultado

@medir_tiempo
def test_consulta_compleja():
    """Test: Consulta compleja con filtros y ordenamiento"""
    ordenes = list(Orden.objects.filter(
        estado_actual='despacho'
    ).select_related('responsable').order_by('-fecha_creacion')[:20])
    return len(ordenes)

@medir_tiempo
def test_crear_orden():
    """Test: Crear una orden"""
    orden = Orden.objects.create(
        cliente=f'Cliente Perf {time.time()}',
        direccion='Dirección Test',
        telefono_cliente='987654321',
        tipo='normal',
        prioridad='media'
    )
    return orden.id

@medir_tiempo
def test_actualizar_orden():
    """Test: Actualizar una orden"""
    orden = Orden.objects.first()
    if orden:
        orden.descripcion = 'Actualización de prueba'
        orden.save()
        return orden.id
    return None

@medir_tiempo
def test_consulta_despachos_agrupados():
    """Test: Consulta de despachos agrupados (último intento)"""
    from django.db.models import Max, OuterRef, Subquery
    
    despachos = Despacho.objects.filter(
        numero_despacho=Subquery(
            Despacho.objects.filter(
                orden=OuterRef('orden')
            ).values('orden').annotate(
                max_num=Max('numero_despacho')
            ).values('max_num')[:1]
        )
    )[:20]
    return list(despachos)

@medir_tiempo
def test_dashboard_stats():
    """Test: Calcular estadísticas del dashboard"""
    total_ordenes = Orden.objects.count()
    ordenes_por_estado = Orden.objects.values('estado_actual').annotate(
        count=Count('id')
    )
    total_despachos = Despacho.objects.count()
    entregas_exitosas = Despacho.objects.filter(resultado='entregado').count()
    
    return {
        'total_ordenes': total_ordenes,
        'ordenes_por_estado': list(ordenes_por_estado),
        'total_despachos': total_despachos,
        'entregas_exitosas': entregas_exitosas
    }

def ejecutar_multiple_veces(func, veces=10):
    """Ejecutar una función múltiples veces y calcular estadísticas"""
    tiempos = []
    for _ in range(veces):
        tiempo, _ = func()
        tiempos.append(tiempo * 1000)  # Convertir a milisegundos
    
    return {
        'promedio': statistics.mean(tiempos),
        'mediana': statistics.median(tiempos),
        'min': min(tiempos),
        'max': max(tiempos),
        'desviacion': statistics.stdev(tiempos) if len(tiempos) > 1 else 0
    }

def test_concurrencia(func, usuarios=10):
    """Test de concurrencia - múltiples usuarios simultáneos"""
    def ejecutar():
        tiempo, _ = func()
        return tiempo * 1000
    
    tiempos = []
    with ThreadPoolExecutor(max_workers=usuarios) as executor:
        futures = [executor.submit(ejecutar) for _ in range(usuarios)]
        for future in as_completed(futures):
            tiempos.append(future.result())
    
    return {
        'promedio': statistics.mean(tiempos),
        'min': min(tiempos),
        'max': max(tiempos),
        'total': sum(tiempos)
    }

def test_consultas_db():
    """Test: Contar número de consultas a la base de datos"""
    from django.test.utils import override_settings
    from django.db import connection
    
    connection.queries_log.clear()
    
    # Ejecutar operación
    ordenes = list(Orden.objects.select_related('responsable').all()[:10])
    
    num_queries = len(connection.queries)
    return num_queries

def main():
    """Ejecutar todas las pruebas de rendimiento"""
    print(f"\n{Colors.BLUE}{'='*70}")
    print("PRUEBAS DE RENDIMIENTO - LOGICO")
    print(f"{'='*70}{Colors.END}\n")
    
    # Resetear contador de queries
    connection.queries_log.clear()
    
    pruebas = [
        ("Consulta Simple (10 órdenes)", test_consulta_simple, 20),
        ("Consulta con JOIN (select_related)", test_consulta_con_join, 20),
        ("Consulta con Agregación", test_consulta_con_agregacion, 20),
        ("Consulta Compleja (filtros + orden)", test_consulta_compleja, 20),
        ("Crear Orden", test_crear_orden, 10),
        ("Actualizar Orden", test_actualizar_orden, 10),
        ("Consulta Despachos Agrupados", test_consulta_despachos_agrupados, 10),
        ("Dashboard Stats", test_dashboard_stats, 10),
    ]
    
    resultados = []
    
    for nombre, funcion, veces in pruebas:
        print(f"{Colors.YELLOW}Probando: {nombre}{Colors.END}")
        try:
            stats = ejecutar_multiple_veces(funcion, veces)
            resultados.append((nombre, stats))
            
            print(f"  Promedio: {Colors.GREEN}{stats['promedio']:.2f}ms{Colors.END}")
            print(f"  Mediana: {stats['mediana']:.2f}ms")
            print(f"  Min: {stats['min']:.2f}ms | Max: {stats['max']:.2f}ms")
            print(f"  Desviación: {stats['desviacion']:.2f}ms")
            
            # Evaluar rendimiento
            if stats['promedio'] < 100:
                print(f"  {Colors.GREEN}✓ Excelente rendimiento{Colors.END}")
            elif stats['promedio'] < 500:
                print(f"  {Colors.GREEN}✓ Buen rendimiento{Colors.END}")
            elif stats['promedio'] < 1000:
                print(f"  {Colors.YELLOW}⚠ Rendimiento aceptable{Colors.END}")
            else:
                print(f"  {Colors.RED}✗ Rendimiento lento{Colors.END}")
                
        except Exception as e:
            print(f"  {Colors.RED}✗ Error: {str(e)}{Colors.END}")
            resultados.append((nombre, None))
        print()
    
    # Pruebas de concurrencia
    print(f"{Colors.YELLOW}Pruebas de Concurrencia (10 usuarios simultáneos){Colors.END}")
    try:
        concurrencia = test_concurrencia(test_consulta_simple, usuarios=10)
        print(f"  Promedio: {Colors.GREEN}{concurrencia['promedio']:.2f}ms{Colors.END}")
        print(f"  Min: {concurrencia['min']:.2f}ms | Max: {concurrencia['max']:.2f}ms")
        print(f"  Tiempo total: {concurrencia['total']:.2f}ms")
    except Exception as e:
        print(f"  {Colors.RED}✗ Error: {str(e)}{Colors.END}")
    print()
    
    # Test de consultas a BD
    print(f"{Colors.YELLOW}Optimización de Consultas{Colors.END}")
    try:
        num_queries = test_consultas_db()
        print(f"  Número de queries: {num_queries}")
        if num_queries <= 2:
            print(f"  {Colors.GREEN}✓ Optimizado (select_related funciona){Colors.END}")
        elif num_queries <= 5:
            print(f"  {Colors.YELLOW}⚠ Aceptable{Colors.END}")
        else:
            print(f"  {Colors.RED}✗ Posible problema N+1 queries{Colors.END}")
    except Exception as e:
        print(f"  {Colors.RED}✗ Error: {str(e)}{Colors.END}")
    print()
    
    # Resumen
    print(f"{Colors.BLUE}{'='*70}")
    print("RESUMEN DE RENDIMIENTO")
    print(f"{'='*70}{Colors.END}\n")
    
    print(f"{'Operación':<40} {'Promedio (ms)':<15} {'Estado':<15}")
    print("-" * 70)
    
    for nombre, stats in resultados:
        if stats:
            estado = "✓ OK" if stats['promedio'] < 500 else "⚠ Lento" if stats['promedio'] < 1000 else "✗ Muy Lento"
            color = Colors.GREEN if stats['promedio'] < 500 else Colors.YELLOW if stats['promedio'] < 1000 else Colors.RED
            print(f"{nombre:<40} {stats['promedio']:<15.2f} {color}{estado}{Colors.END}")
        else:
            print(f"{nombre:<40} {'ERROR':<15} {Colors.RED}✗ FALLÓ{Colors.END}")
    
    print()

if __name__ == '__main__':
    main()

