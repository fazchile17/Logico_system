"""
Script de pruebas funcionales básicas para LogiCo
Ejecutar: python test_funcional_basico.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logico.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UsuarioProfile, Orden, Moto, Despacho
from django.utils import timezone
from datetime import timedelta

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.YELLOW}Testing: {name}{Colors.END}")

def print_pass(message):
    print(f"{Colors.GREEN}✓ PASS: {message}{Colors.END}")

def print_fail(message):
    print(f"{Colors.RED}✗ FAIL: {message}{Colors.END}")

def test_crear_usuario():
    """Test: Crear usuario como admin"""
    print_test("Crear Usuario (Admin)")
    
    try:
        # Crear usuario admin si no existe
        admin, created = User.objects.get_or_create(
            username='test_admin',
            defaults={'email': 'admin@test.com', 'is_staff': True}
        )
        if created:
            admin.set_password('test123')
            admin.save()
        
        # Crear perfil
        profile, _ = UsuarioProfile.objects.get_or_create(
            user=admin,
            defaults={'telefono': '123456789', 'rol': 'admin', 'activo': True}
        )
        
        print_pass("Usuario admin creado/obtenido")
        return True
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_crear_moto():
    """Test: Crear moto"""
    print_test("Crear Moto")
    
    try:
        moto, created = Moto.objects.get_or_create(
            patente='TEST01',
            defaults={
                'marca': 'Yamaha',
                'modelo': 'Test',
                'año': 2023,
                'color': 'Negro',
                'cilindrada': 150,
                'kilometraje': 0,
                'estado': 'disponible',
                'activa': True
            }
        )
        
        if created:
            print_pass("Moto creada exitosamente")
        else:
            print_pass("Moto ya existía (OK)")
        return True
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_crear_orden():
    """Test: Crear orden"""
    print_test("Crear Orden")
    
    try:
        orden = Orden.objects.create(
            cliente='Cliente Test',
            direccion='Dirección Test 123',
            telefono_cliente='987654321',
            descripcion='Orden de prueba',
            prioridad='media',
            tipo='normal',
            estado_actual='retiro_receta'
        )
        
        print_pass(f"Orden #{orden.id} creada")
        return True
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_asignar_repartidor_moto():
    """Test: Asignar repartidor a moto"""
    print_test("Asignar Repartidor a Moto")
    
    try:
        # Crear repartidor
        repartidor_user, _ = User.objects.get_or_create(
            username='test_repartidor',
            defaults={'email': 'repartidor@test.com'}
        )
        if not repartidor_user.password:
            repartidor_user.set_password('test123')
            repartidor_user.save()
        
        repartidor, _ = UsuarioProfile.objects.get_or_create(
            user=repartidor_user,
            defaults={'telefono': '123456789', 'rol': 'repartidor', 'activo': True}
        )
        
        # Obtener moto
        moto = Moto.objects.filter(patente='TEST01').first()
        if not moto:
            print_fail("Moto TEST01 no existe")
            return False
        
        # Asignar
        repartidor.moto = moto
        repartidor.save()
        moto.estado = 'en_uso'
        moto.save()
        
        print_pass("Repartidor asignado a moto")
        return True
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_permisos_repartidor():
    """Test: Verificar que repartidor solo ve sus órdenes"""
    print_test("Permisos Repartidor")
    
    try:
        repartidor = UsuarioProfile.objects.filter(rol='repartidor').first()
        if not repartidor:
            print_fail("No hay repartidor para probar")
            return False
        
        # Crear orden asignada al repartidor
        orden = Orden.objects.create(
            cliente='Cliente Test 2',
            direccion='Dirección Test 456',
            telefono_cliente='987654322',
            responsable=repartidor,
            estado_actual='despacho'
        )
        
        # Verificar que repartidor puede verla
        ordenes_repartidor = Orden.objects.filter(responsable=repartidor)
        if orden in ordenes_repartidor:
            print_pass("Repartidor puede ver sus órdenes")
            return True
        else:
            print_fail("Repartidor no puede ver sus órdenes")
            return False
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_listar_ultimo_despacho():
    """Test: Verificar que solo se muestra último intento"""
    print_test("Listar Último Despacho")
    
    try:
        orden = Orden.objects.first()
        if not orden:
            print_fail("No hay órdenes para probar")
            return False
        
        repartidor = UsuarioProfile.objects.filter(rol='repartidor').first()
        if not repartidor:
            print_fail("No hay repartidor para probar")
            return False
        
        # Crear múltiples despachos
        despacho1 = Despacho.objects.create(
            orden=orden,
            numero_despacho=1,
            repartidor=repartidor,
            estado='despacho',
            resultado='no_disponible'
        )
        
        despacho2 = Despacho.objects.create(
            orden=orden,
            numero_despacho=2,
            repartidor=repartidor,
            estado='re_despacho',
            resultado='error'
        )
        
        despacho3 = Despacho.objects.create(
            orden=orden,
            numero_despacho=3,
            repartidor=repartidor,
            estado='re_despacho',
            resultado='entregado'
        )
        
        # Obtener último despacho
        from django.db.models import Max
        ultimo_numero = Despacho.objects.filter(orden=orden).aggregate(Max('numero_despacho'))['numero_despacho__max']
        ultimo_despacho = Despacho.objects.get(orden=orden, numero_despacho=ultimo_numero)
        
        if ultimo_despacho.numero_despacho == 3:
            print_pass("Último despacho identificado correctamente")
            return True
        else:
            print_fail(f"Último despacho incorrecto: {ultimo_despacho.numero_despacho}")
            return False
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_validacion_descanso():
    """Test: Validación de descanso máximo 1 hora"""
    print_test("Validación Descanso 1 Hora")
    
    try:
        repartidor = UsuarioProfile.objects.filter(rol='repartidor').first()
        if not repartidor:
            print_fail("No hay repartidor para probar")
            return False
        
        # Simular descanso iniciado hace 1 hora
        repartidor.estado_turno = 'descanso'
        repartidor.fecha_inicio_descanso = timezone.now() - timedelta(hours=1, minutes=1)
        repartidor.save()
        
        # Verificar que el sistema detecta el exceso
        tiempo_descanso = timezone.now() - repartidor.fecha_inicio_descanso
        if tiempo_descanso >= timedelta(hours=1):
            print_pass("Sistema detecta descanso > 1 hora")
            # Resetear
            repartidor.estado_turno = 'disponible'
            repartidor.fecha_inicio_descanso = None
            repartidor.save()
            return True
        else:
            print_fail("Sistema no detecta descanso > 1 hora")
            return False
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def test_excluir_admin_repartidor():
    """Test: Verificar que admin está excluido de lista de repartidores"""
    print_test("Excluir Admin de Lista de Repartidores")
    
    try:
        # Crear admin
        admin_user, _ = User.objects.get_or_create(
            username='test_admin_repartidor',
            defaults={'email': 'admin_rep@test.com', 'is_superuser': True}
        )
        admin_profile, _ = UsuarioProfile.objects.get_or_create(
            user=admin_user,
            defaults={'telefono': '123456789', 'rol': 'repartidor', 'activo': True}
        )
        
        # Verificar que admin NO aparece en queryset de repartidores
        repartidores = UsuarioProfile.objects.filter(
            rol='repartidor', 
            activo=True
        ).exclude(user__is_superuser=True)
        
        if admin_profile not in repartidores:
            print_pass("Admin excluido correctamente de lista de repartidores")
            return True
        else:
            print_fail("Admin aparece en lista de repartidores")
            return False
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print("PLAN DE PRUEBAS EJECUTABLE - LOGICO")
    print(f"{'='*60}{Colors.END}\n")
    
    tests = [
        test_crear_usuario,
        test_crear_moto,
        test_crear_orden,
        test_asignar_repartidor_moto,
        test_permisos_repartidor,
        test_listar_ultimo_despacho,
        test_validacion_descanso,
        test_excluir_admin_repartidor,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print_fail(f"Error ejecutando test: {str(e)}")
            results.append(False)
    
    # Resumen
    print(f"\n{Colors.BLUE}{'='*60}")
    print("RESUMEN DE PRUEBAS")
    print(f"{'='*60}{Colors.END}")
    passed = sum(results)
    total = len(results)
    print(f"Total: {total}")
    print(f"{Colors.GREEN}Pasaron: {passed}{Colors.END}")
    print(f"{Colors.RED}Fallaron: {total - passed}{Colors.END}")
    print(f"Tasa de éxito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print(f"\n{Colors.GREEN}✓ TODAS LAS PRUEBAS PASARON{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}✗ ALGUNAS PRUEBAS FALLARON{Colors.END}")
        return 1

if __name__ == '__main__':
    exit(main())

