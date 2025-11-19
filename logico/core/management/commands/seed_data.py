from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from core.models import (
    UsuarioProfile, Moto, Orden, Medicamento,
    Despacho, OrdenMovimiento, Ruta, Reporte, Farmacia
)
import random


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema LogiCo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando creación de datos de prueba...'))
        
        # Crear Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@logico.cl',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            admin_profile, _ = UsuarioProfile.objects.get_or_create(
                user=admin_user,
                defaults={
                    'telefono': '+56912345678',
                    'rol': 'admin',
                    'estado_turno': 'disponible',
                }
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Admin creado: {admin_user.username}'))
        
        # Crear Coordinadores
        coordinadores_data = [
            {'username': 'coordinador1', 'first_name': 'María', 'last_name': 'González', 'email': 'maria@logico.cl'},
            {'username': 'coordinador2', 'first_name': 'Carlos', 'last_name': 'Rodríguez', 'email': 'carlos@logico.cl'},
        ]
        
        for coord_data in coordinadores_data:
            user, created = User.objects.get_or_create(
                username=coord_data['username'],
                defaults={
                    'email': coord_data['email'],
                    'first_name': coord_data['first_name'],
                    'last_name': coord_data['last_name'],
                }
            )
            if created:
                user.set_password('coordinador123')
                user.save()
            profile, _ = UsuarioProfile.objects.get_or_create(
                user=user,
                defaults={
                    'telefono': f'+569{random.randint(10000000, 99999999)}',
                    'rol': 'coordinador',
                    'estado_turno': 'disponible',
                }
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Coordinador creado: {user.get_full_name()}'))
        
        # Crear Repartidores
        repartidores_data = [
            {'username': 'repartidor1', 'first_name': 'Juan', 'last_name': 'Pérez', 'email': 'juan@logico.cl'},
            {'username': 'repartidor2', 'first_name': 'Pedro', 'last_name': 'Sánchez', 'email': 'pedro@logico.cl'},
            {'username': 'repartidor3', 'first_name': 'Diego', 'last_name': 'Muñoz', 'email': 'diego@logico.cl'},
        ]
        
        repartidores = []
        for rep_data in repartidores_data:
            user, created = User.objects.get_or_create(
                username=rep_data['username'],
                defaults={
                    'email': rep_data['email'],
                    'first_name': rep_data['first_name'],
                    'last_name': rep_data['last_name'],
                }
            )
            if created:
                user.set_password('repartidor123')
                user.save()
            profile, _ = UsuarioProfile.objects.get_or_create(
                user=user,
                defaults={
                    'telefono': f'+569{random.randint(10000000, 99999999)}',
                    'rol': 'repartidor',
                    'estado_turno': 'disponible',
                }
            )
            repartidores.append(profile)
            self.stdout.write(self.style.SUCCESS(f'[OK] Repartidor creado: {user.get_full_name()}'))
        
        # Crear Farmacias
        farmacias_data = [
            {'nombre': 'Farmacia Central', 'direccion': 'Av. Providencia 1234', 'telefono': '+56223456789', 'ciudad': 'Santiago'},
            {'nombre': 'Farmacia Norte', 'direccion': 'Av. Las Condes 5678', 'telefono': '+56223456790', 'ciudad': 'Santiago'},
            {'nombre': 'Farmacia Sur', 'direccion': 'Av. La Florida 9012', 'telefono': '+56223456791', 'ciudad': 'Santiago'},
        ]
        
        farmacias = []
        for farmacia_data in farmacias_data:
            farmacia, created = Farmacia.objects.get_or_create(
                nombre=farmacia_data['nombre'],
                defaults={
                    'direccion': farmacia_data['direccion'],
                    'telefono': farmacia_data['telefono'],
                    'ciudad': farmacia_data['ciudad'],
                    'activa': True,
                }
            )
            farmacias.append(farmacia)
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Farmacia creada: {farmacia.nombre}'))
        
        # Crear Motos
        motos_data = [
            {'patente': 'ABCD12', 'marca': 'Yamaha', 'modelo': 'FZ16', 'año': 2020, 'color': 'Negro', 'cilindrada': 160},
            {'patente': 'EFGH34', 'marca': 'Honda', 'modelo': 'CB125F', 'año': 2021, 'color': 'Rojo', 'cilindrada': 125},
            {'patente': 'IJKL56', 'marca': 'Suzuki', 'modelo': 'GN125', 'año': 2019, 'color': 'Azul', 'cilindrada': 125},
            {'patente': 'MNOP78', 'marca': 'Yamaha', 'modelo': 'MT-03', 'año': 2022, 'color': 'Blanco', 'cilindrada': 321},
            {'patente': 'QRST90', 'marca': 'Honda', 'modelo': 'XR150L', 'año': 2020, 'color': 'Verde', 'cilindrada': 150},
        ]
        
        motos = []
        for moto_data in motos_data:
            moto, created = Moto.objects.get_or_create(
                patente=moto_data['patente'],
                defaults={
                    'marca': moto_data['marca'],
                    'modelo': moto_data['modelo'],
                    'año': moto_data['año'],
                    'color': moto_data['color'],
                    'cilindrada': moto_data['cilindrada'],
                    'kilometraje': random.randint(1000, 50000),
                    'estado': 'disponible',
                    'activa': True,
                }
            )
            motos.append(moto)
            self.stdout.write(self.style.SUCCESS(f'[OK] Moto creada: {moto.patente}'))
        
        # Asignar motos a repartidores
        for i, repartidor in enumerate(repartidores[:3]):
            if i < len(motos):
                repartidor.moto = motos[i]
                repartidor.save()
                motos[i].estado = 'en_uso'
                motos[i].save()
                self.stdout.write(self.style.SUCCESS(f'[OK] Moto {motos[i].patente} asignada a {repartidor.user.get_full_name()}'))
        
        # Crear Órdenes
        clientes = [
            {'nombre': 'Ana Martínez', 'direccion': 'Av. Providencia 123, Santiago', 'telefono': '+56911111111'},
            {'nombre': 'Luis Fernández', 'direccion': 'Calle Las Condes 456, Las Condes', 'telefono': '+56922222222'},
            {'nombre': 'Carmen Silva', 'direccion': 'Av. Vitacura 789, Vitacura', 'telefono': '+56933333333'},
            {'nombre': 'Roberto Vargas', 'direccion': 'Calle Nueva Providencia 321, Providencia', 'telefono': '+56944444444'},
            {'nombre': 'Patricia Morales', 'direccion': 'Av. Apoquindo 654, Las Condes', 'telefono': '+56955555555'},
            {'nombre': 'Fernando Torres', 'direccion': 'Calle El Bosque 987, La Reina', 'telefono': '+56966666666'},
            {'nombre': 'Isabel Ramírez', 'direccion': 'Av. Tobalaba 147, Providencia', 'telefono': '+56977777777'},
            {'nombre': 'Miguel Herrera', 'direccion': 'Calle Los Leones 258, Providencia', 'telefono': '+56988888888'},
            {'nombre': 'Sofía Contreras', 'direccion': 'Av. Kennedy 369, Las Condes', 'telefono': '+56999999999'},
            {'nombre': 'Andrés Jiménez', 'direccion': 'Calle Manquehue 741, Las Condes', 'telefono': '+56910101010'},
        ]
        
        medicamentos_nombres = [
            {'codigo': 'MED001', 'nombre': 'Paracetamol 500mg', 'cantidad': 20},
            {'codigo': 'MED002', 'nombre': 'Ibuprofeno 400mg', 'cantidad': 15},
            {'codigo': 'MED003', 'nombre': 'Amoxicilina 500mg', 'cantidad': 14},
            {'codigo': 'MED004', 'nombre': 'Omeprazol 20mg', 'cantidad': 30},
            {'codigo': 'MED005', 'nombre': 'Loratadina 10mg', 'cantidad': 10},
            {'codigo': 'MED006', 'nombre': 'Metformina 500mg', 'cantidad': 60},
            {'codigo': 'MED007', 'nombre': 'Atorvastatina 20mg', 'cantidad': 30},
            {'codigo': 'MED008', 'nombre': 'Losartán 50mg', 'cantidad': 30},
        ]
        
        estados = ['retiro_receta', 'traslado', 'despacho', 're_despacho']
        prioridades = ['alta', 'media', 'baja']
        tipos = ['receta_detendida', 'normal']
        
        ordenes = []
        for i, cliente in enumerate(clientes):
            tipo = random.choice(tipos)
            prioridad = 'alta' if tipo == 'receta_detendida' else random.choice(prioridades)
            estado = random.choice(estados)
            
            # Si el estado es traslado, asignar farmacias
            farmacia_origen = None
            farmacia_destino = None
            if estado == 'traslado' and len(farmacias) >= 2:
                farmacias_seleccionadas = random.sample(farmacias, 2)
                farmacia_origen = farmacias_seleccionadas[0]
                farmacia_destino = farmacias_seleccionadas[1]
            
            orden = Orden.objects.create(
                cliente=cliente['nombre'],
                direccion=cliente['direccion'],
                telefono_cliente=cliente['telefono'],
                descripcion=f'Orden de prueba #{i+1}',
                prioridad=prioridad,
                tipo=tipo,
                estado_actual=estado,
                farmacia_origen=farmacia_origen,
                farmacia_destino=farmacia_destino,
                responsable=random.choice(repartidores) if random.choice([True, False]) else None,
                fecha_creacion=timezone.now() - timedelta(days=random.randint(0, 30)),
            )
            ordenes.append(orden)
            
            # Agregar medicamentos
            num_meds = random.randint(1, 3)
            meds_selected = random.sample(medicamentos_nombres, num_meds)
            for med in meds_selected:
                Medicamento.objects.create(
                    orden=orden,
                    codigo=med['codigo'],
                    nombre=med['nombre'],
                    cantidad=med['cantidad'],
                    observaciones='',
                )
            
            # Crear movimiento inicial
            OrdenMovimiento.objects.create(
                orden=orden,
                estado=orden.estado_actual,
                descripcion='Orden creada',
                repartidor=orden.responsable,
            )
            
            self.stdout.write(self.style.SUCCESS(f'[OK] Orden creada: #{orden.id} - {orden.cliente}'))
        
        # Crear Despachos
        resultados = ['entregado', 'no_disponible', 'error', None]
        for orden in ordenes[:7]:
            num_despachos = random.randint(1, 3)
            for i in range(num_despachos):
                resultado = random.choice(resultados) if i == num_despachos - 1 else None
                despacho = Despacho.objects.create(
                    orden=orden,
                    numero_despacho=i + 1,
                    repartidor=orden.responsable or random.choice(repartidores),
                    estado='re_despacho' if i > 0 else 'despacho',
                    resultado=resultado,
                    observaciones=f'Despacho #{i+1}',
                    fecha=timezone.now() - timedelta(days=random.randint(0, 10)),
                )
                
                if resultado:
                    OrdenMovimiento.objects.create(
                        orden=orden,
                        estado=orden.estado_actual,
                        descripcion=f'Despacho #{despacho.numero_despacho} - {despacho.get_resultado_display()}',
                        repartidor=despacho.repartidor,
                        despacho=despacho,
                    )
                
                self.stdout.write(self.style.SUCCESS(f'[OK] Despacho creado: #{despacho.numero_despacho} para Orden #{orden.id}'))
        
        # Crear Rutas
        rutas_data = [
            {'nombre': 'Ruta Centro', 'zona': 'Santiago Centro', 'vehiculo': 'Moto'},
            {'nombre': 'Ruta Las Condes', 'zona': 'Las Condes', 'vehiculo': 'Moto'},
            {'nombre': 'Ruta Providencia', 'zona': 'Providencia', 'vehiculo': 'Moto'},
        ]
        
        for ruta_data in rutas_data:
            ruta = Ruta.objects.create(
                nombre=ruta_data['nombre'],
                descripcion=f"Ruta para {ruta_data['zona']}",
                zona=ruta_data['zona'],
                vehiculo=ruta_data['vehiculo'],
                repartidor=random.choice(repartidores),
                activa=True,
            )
            # Asignar algunas órdenes a la ruta
            ordenes_ruta = random.sample(ordenes, min(3, len(ordenes)))
            ruta.ordenes.set(ordenes_ruta)
            self.stdout.write(self.style.SUCCESS(f'[OK] Ruta creada: {ruta.nombre}'))
        
        # Crear Reportes
        for i in range(7):
            fecha = timezone.now().date() - timedelta(days=i)
            entregas_totales = random.randint(10, 50)
            entregas_exitosas = random.randint(8, entregas_totales - 2)
            entregas_fallidas = entregas_totales - entregas_exitosas
            
            reporte, created = Reporte.objects.get_or_create(
                fecha=fecha,
                defaults={
                    'entregas_totales': entregas_totales,
                    'entregas_exitosas': entregas_exitosas,
                    'entregas_fallidas': entregas_fallidas,
                    'tiempo_promedio': timedelta(minutes=random.randint(15, 45)),
                    'ingresos_dia': random.randint(50000, 200000),
                    'observaciones': f'Reporte del día {fecha}',
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Reporte creado: {reporte.fecha}'))
            else:
                self.stdout.write(self.style.WARNING(f'[SKIP] Reporte ya existe: {reporte.fecha}'))
        
        self.stdout.write(self.style.SUCCESS('\n[OK] Datos de prueba creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS('\nUsuarios de prueba:'))
        self.stdout.write(self.style.SUCCESS('  Admin: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('  Coordinador: coordinador1 / coordinador123'))
        self.stdout.write(self.style.SUCCESS('  Repartidor: repartidor1 / repartidor123'))

