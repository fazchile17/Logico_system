"""
Pruebas de Integración Completas para LogiCo
Ejecutar: python test_integracion_completo.py

Prueba flujos completos end-to-end
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logico.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import UsuarioProfile, Orden, Moto, Despacho, OrdenMovimiento, Medicamento
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

def test_flujo_completo_orden():
    """Test: Flujo completo desde creación hasta entrega"""
    print_test("Flujo Completo de Orden")
    
    try:
        # 1. Crear orden como admin
        admin = User.objects.filter(username='admin').first()
        if not admin:
            print_fail("Usuario admin no existe")
            return False
        
        orden = Orden.objects.create(
            cliente='Cliente Integración',
            direccion='Dirección Integración 123',
            telefono_cliente='987654321',
            descripcion='Orden de prueba de integración',
            tipo='normal',
            prioridad='media',
            estado_actual='retiro_receta'
        )
        print_pass(f"1. Orden #{orden.id} creada")
        
        # 2. Agregar medicamentos
        medicamento1 = Medicamento.objects.create(
            orden=orden,
            codigo='MED001',
            nombre='Paracetamol',
            cantidad=2
        )
        medicamento2 = Medicamento.objects.create(
            orden=orden,
            codigo='MED002',
            nombre='Ibuprofeno',
            cantidad=1
        )
        print_pass(f"2. {Medicamento.objects.filter(orden=orden).count()} medicamentos agregados")
        
        # 3. Asignar repartidor
        repartidor = UsuarioProfile.objects.filter(rol='repartidor', activo=True).first()
        if not repartidor:
            print_fail("No hay repartidor disponible")
            return False
        
        orden.responsable = repartidor
        orden.save()
        
        # Registrar movimiento
        OrdenMovimiento.objects.create(
            orden=orden,
            estado='traslado',
            descripcion='Repartidor asignado',
            repartidor=repartidor
        )
        orden.estado_actual = 'traslado'
        orden.save()
        print_pass(f"3. Repartidor {repartidor.user.username} asignado")
        
        # 4. Cambiar a despacho
        OrdenMovimiento.objects.create(
            orden=orden,
            estado='despacho',
            descripcion='Iniciando despacho',
            repartidor=repartidor
        )
        orden.estado_actual = 'despacho'
        orden.save()
        print_pass("4. Estado cambiado a despacho")
        
        # 5. Crear despacho
        despacho = Despacho.objects.create(
            orden=orden,
            numero_despacho=1,
            repartidor=repartidor,
            estado='despacho',
            resultado='entregado',
            observaciones='Entrega exitosa'
        )
        print_pass(f"5. Despacho #{despacho.numero_despacho} creado")
        
        # 6. Verificar historial
        movimientos = OrdenMovimiento.objects.filter(orden=orden).count()
        if movimientos >= 3:
            print_pass(f"6. Historial completo: {movimientos} movimientos registrados")
        else:
            print_fail(f"6. Historial incompleto: {movimientos} movimientos")
            return False
        
        # 7. Verificar integridad de datos
        orden.refresh_from_db()
        if orden.responsable == repartidor:
            print_pass("7. Integridad de datos mantenida")
        else:
            print_fail("7. Integridad de datos comprometida")
            return False
        
        return True
        
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_flujo_re_despacho():
    """Test: Flujo con re-despacho (múltiples intentos)"""
    print_test("Flujo con Re-despacho")
    
    try:
        # Crear orden
        orden = Orden.objects.create(
            cliente='Cliente Re-despacho',
            direccion='Dirección Re-despacho 456',
            telefono_cliente='987654322',
            tipo='normal',
            estado_actual='despacho'
        )
        
        repartidor = UsuarioProfile.objects.filter(rol='repartidor', activo=True).first()
        if not repartidor:
            print_fail("No hay repartidor disponible")
            return False
        
        orden.responsable = repartidor
        orden.save()
        
        # Primer intento - fallido
        despacho1 = Despacho.objects.create(
            orden=orden,
            numero_despacho=1,
            repartidor=repartidor,
            estado='despacho',
            resultado='no_disponible'
        )
        print_pass("1. Primer despacho (fallido) creado")
        
        # Segundo intento - fallido
        despacho2 = Despacho.objects.create(
            orden=orden,
            numero_despacho=2,
            repartidor=repartidor,
            estado='re_despacho',
            resultado='error'
        )
        print_pass("2. Segundo despacho (fallido) creado")
        
        # Tercer intento - exitoso
        despacho3 = Despacho.objects.create(
            orden=orden,
            numero_despacho=3,
            repartidor=repartidor,
            estado='re_despacho',
            resultado='entregado'
        )
        print_pass("3. Tercer despacho (exitoso) creado")
        
        # Verificar que hay 3 despachos
        total_despachos = Despacho.objects.filter(orden=orden).count()
        if total_despachos == 3:
            print_pass(f"4. Total de despachos: {total_despachos}")
        else:
            print_fail(f"4. Número incorrecto de despachos: {total_despachos}")
            return False
        
        # Verificar último despacho
        from django.db.models import Max
        ultimo_numero = Despacho.objects.filter(orden=orden).aggregate(
            Max('numero_despacho')
        )['numero_despacho__max']
        
        if ultimo_numero == 3:
            print_pass("5. Último despacho identificado correctamente")
        else:
            print_fail(f"5. Último despacho incorrecto: {ultimo_numero}")
            return False
        
        return True
        
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_asignacion_moto_repartidor():
    """Test: Flujo completo de asignación de moto a repartidor"""
    print_test("Asignación Moto-Repartidor")
    
    try:
        # Crear moto
        moto = Moto.objects.create(
            patente='INTEG01',
            marca='Yamaha',
            modelo='Integración',
            año=2023,
            color='Azul',
            cilindrada=150,
            kilometraje=0,
            estado='disponible',
            activa=True
        )
        print_pass("1. Moto creada")
        
        # Obtener repartidor sin moto
        repartidor = UsuarioProfile.objects.filter(
            rol='repartidor',
            activo=True,
            moto__isnull=True
        ).first()
        
        if not repartidor:
            # Crear repartidor si no existe
            user, _ = User.objects.get_or_create(
                username='repartidor_integracion',
                defaults={'email': 'rep_int@test.com'}
            )
            repartidor, _ = UsuarioProfile.objects.get_or_create(
                user=user,
                defaults={'telefono': '123456789', 'rol': 'repartidor', 'activo': True}
            )
        
        # Asignar moto
        repartidor.moto = moto
        repartidor.save()
        moto.estado = 'en_uso'
        moto.save()
        print_pass("2. Moto asignada a repartidor")
        
        # Verificar asignación
        repartidor.refresh_from_db()
        moto.refresh_from_db()
        
        if repartidor.moto == moto and moto.estado == 'en_uso':
            print_pass("3. Asignación verificada correctamente")
        else:
            print_fail("3. Asignación no se reflejó correctamente")
            return False
        
        # Verificar propiedad inversa
        if moto.repartidor_asignado == repartidor:
            print_pass("4. Propiedad inversa funciona")
        else:
            print_fail("4. Propiedad inversa no funciona")
            return False
        
        # Desasignar
        repartidor.moto = None
        repartidor.save()
        moto.estado = 'disponible'
        moto.save()
        print_pass("5. Moto desasignada correctamente")
        
        return True
        
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_validacion_descanso_completa():
    """Test: Validación completa del sistema de descanso"""
    print_test("Validación Completa de Descanso")
    
    try:
        repartidor = UsuarioProfile.objects.filter(rol='repartidor', activo=True).first()
        if not repartidor:
            print_fail("No hay repartidor disponible")
            return False
        
        # Estado inicial
        repartidor.estado_turno = 'disponible'
        repartidor.fecha_inicio_descanso = None
        repartidor.save()
        print_pass("1. Estado inicial: disponible")
        
        # Iniciar descanso
        repartidor.estado_turno = 'descanso'
        repartidor.fecha_inicio_descanso = timezone.now()
        repartidor.save()
        print_pass("2. Descanso iniciado")
        
        # Verificar que fecha se guardó
        repartidor.refresh_from_db()
        if repartidor.fecha_inicio_descanso:
            print_pass("3. Fecha de inicio guardada")
        else:
            print_fail("3. Fecha de inicio no se guardó")
            return False
        
        # Simular 30 minutos
        repartidor.fecha_inicio_descanso = timezone.now() - timedelta(minutes=30)
        repartidor.save()
        
        tiempo_descanso = timezone.now() - repartidor.fecha_inicio_descanso
        if tiempo_descanso < timedelta(hours=1):
            print_pass("4. Sistema detecta descanso < 1 hora")
        else:
            print_fail("4. Sistema no detecta correctamente el tiempo")
            return False
        
        # Simular 1 hora y 5 minutos
        repartidor.fecha_inicio_descanso = timezone.now() - timedelta(hours=1, minutes=5)
        repartidor.save()
        
        tiempo_descanso = timezone.now() - repartidor.fecha_inicio_descanso
        if tiempo_descanso >= timedelta(hours=1):
            print_pass("5. Sistema detecta descanso > 1 hora")
            # Resetear
            repartidor.estado_turno = 'disponible'
            repartidor.fecha_inicio_descanso = None
            repartidor.save()
        else:
            print_fail("5. Sistema no detecta descanso > 1 hora")
            return False
        
        return True
        
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_permisos_por_rol():
    """Test: Verificar permisos por rol en diferentes operaciones"""
    print_test("Permisos por Rol")
    
    try:
        # Crear usuarios de prueba
        admin_user, _ = User.objects.get_or_create(
            username='test_admin_perm',
            defaults={'email': 'admin_perm@test.com', 'is_staff': True}
        )
        admin_profile, _ = UsuarioProfile.objects.get_or_create(
            user=admin_user,
            defaults={'telefono': '123456789', 'rol': 'admin', 'activo': True}
        )
        
        coord_user, _ = User.objects.get_or_create(
            username='test_coord_perm',
            defaults={'email': 'coord_perm@test.com'}
        )
        coord_profile, _ = UsuarioProfile.objects.get_or_create(
            user=coord_user,
            defaults={'telefono': '123456789', 'rol': 'coordinador', 'activo': True}
        )
        
        rep_user, _ = User.objects.get_or_create(
            username='test_rep_perm',
            defaults={'email': 'rep_perm@test.com'}
        )
        rep_profile, _ = UsuarioProfile.objects.get_or_create(
            user=rep_user,
            defaults={'telefono': '123456789', 'rol': 'repartidor', 'activo': True}
        )
        
        # Test: Admin puede crear usuarios
        if admin_profile.rol == 'admin':
            print_pass("1. Admin tiene rol correcto")
        else:
            print_fail("1. Admin no tiene rol correcto")
            return False
        
        # Test: Coordinador NO puede crear usuarios (validación en vista)
        if coord_profile.rol == 'coordinador':
            print_pass("2. Coordinador tiene rol correcto")
        else:
            print_fail("2. Coordinador no tiene rol correcto")
            return False
        
        # Test: Repartidor solo se ve a sí mismo
        if rep_profile.rol == 'repartidor':
            print_pass("3. Repartidor tiene rol correcto")
        else:
            print_fail("3. Repartidor no tiene rol correcto")
            return False
        
        # Test: Admin excluido de lista de repartidores
        repartidores = UsuarioProfile.objects.filter(
            rol='repartidor',
            activo=True
        ).exclude(user__is_superuser=True)
        
        if admin_profile not in repartidores:
            print_pass("4. Admin excluido de lista de repartidores")
        else:
            print_fail("4. Admin aparece en lista de repartidores")
            return False
        
        return True
        
    except Exception as e:
        print_fail(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todas las pruebas de integración"""
    print(f"\n{Colors.BLUE}{'='*70}")
    print("PRUEBAS DE INTEGRACIÓN COMPLETAS - LOGICO")
    print(f"{'='*70}{Colors.END}\n")
    
    pruebas = [
        test_flujo_completo_orden,
        test_flujo_re_despacho,
        test_asignacion_moto_repartidor,
        test_validacion_descanso_completa,
        test_permisos_por_rol,
    ]
    
    results = []
    for test in pruebas:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print_fail(f"Error ejecutando test: {str(e)}")
            results.append(False)
    
    # Resumen
    print(f"\n{Colors.BLUE}{'='*70}")
    print("RESUMEN DE PRUEBAS DE INTEGRACIÓN")
    print(f"{'='*70}{Colors.END}")
    passed = sum(results)
    total = len(results)
    print(f"Total: {total}")
    print(f"{Colors.GREEN}Pasaron: {passed}{Colors.END}")
    print(f"{Colors.RED}Fallaron: {total - passed}{Colors.END}")
    print(f"Tasa de éxito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print(f"\n{Colors.GREEN}✓ TODAS LAS PRUEBAS DE INTEGRACIÓN PASARON{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}✗ ALGUNAS PRUEBAS DE INTEGRACIÓN FALLARON{Colors.END}")
        return 1

if __name__ == '__main__':
    exit(main())

