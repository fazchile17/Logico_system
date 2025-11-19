from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta
import json
from .models import (
    UsuarioProfile, Moto, Orden, Medicamento, 
    Despacho, OrdenMovimiento, Ruta, Reporte, Farmacia
)
from .forms import OrdenForm, DespachoForm, MotoForm, RutaForm, UsuarioForm, UsuarioProfileForm
from django.contrib.auth.models import User
import csv


@login_required
def dashboard(request):
    """Dashboard principal con estadísticas"""
    # Asegurar que el usuario tenga un perfil
    user_profile, created = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Filtros según rol
    if user_profile.rol == 'repartidor':
        ordenes = Orden.objects.filter(responsable=user_profile)
        despachos = Despacho.objects.filter(repartidor=user_profile)
    else:
        ordenes = Orden.objects.all()
        despachos = Despacho.objects.all()
    
    # Estadísticas generales
    total_ordenes = ordenes.count()
    ordenes_por_estado = ordenes.values('estado_actual').annotate(count=Count('id'))
    
    # Despachos
    total_despachos = despachos.count()
    entregas_exitosas = despachos.filter(resultado='entregado').count()
    entregas_fallidas = despachos.filter(resultado__in=['no_disponible', 'error']).count()
    tasa_exito = (entregas_exitosas / total_despachos * 100) if total_despachos > 0 else 0
    
    # Repartidores activos
    repartidores_activos = UsuarioProfile.objects.filter(
        rol='repartidor', 
        activo=True,
        estado_turno='disponible'
    ).count()
    
    # Motos activas
    motos_activas = Moto.objects.filter(activa=True, estado='disponible').count()
    
    # Gráfico de entregas por día (últimos 7 días)
    fecha_inicio = timezone.now().date() - timedelta(days=7)
    entregas_por_dia = Despacho.objects.filter(
        fecha__date__gte=fecha_inicio
    ).extra(
        select={'day': 'date(fecha)'}
    ).values('day').annotate(
        total=Count('id'),
        exitosas=Count('id', filter=Q(resultado='entregado'))
    ).order_by('day')
    
    # Convertir a lista de diccionarios para JSON
    entregas_por_dia_list = []
    for item in entregas_por_dia:
        entregas_por_dia_list.append({
            'day': str(item['day']),
            'total': item['total'],
            'exitosas': item['exitosas']
        })
    
    # Resultados de despacho
    resultados_despacho = despachos.values('resultado').annotate(count=Count('id'))
    resultados_despacho_list = []
    for item in resultados_despacho:
        resultados_despacho_list.append({
            'resultado': item['resultado'] or 'Sin resultado',
            'count': item['count']
        })
    
    context = {
        'total_ordenes': total_ordenes,
        'ordenes_por_estado': list(ordenes_por_estado),
        'total_despachos': total_despachos,
        'entregas_exitosas': entregas_exitosas,
        'entregas_fallidas': entregas_fallidas,
        'tasa_exito': round(tasa_exito, 2),
        'repartidores_activos': repartidores_activos,
        'motos_activas': motos_activas,
        'entregas_por_dia': json.dumps(entregas_por_dia_list),
        'resultados_despacho': json.dumps(resultados_despacho_list),
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def orden_list(request):
    """Lista de órdenes"""
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    ordenes = Orden.objects.all()
    
    # Filtros según rol
    if user_profile.rol == 'repartidor':
        ordenes = ordenes.filter(responsable=user_profile)
    
    # Filtros de búsqueda
    estado = request.GET.get('estado')
    prioridad = request.GET.get('prioridad')
    search = request.GET.get('search')
    
    if estado:
        ordenes = ordenes.filter(estado_actual=estado)
    if prioridad:
        ordenes = ordenes.filter(prioridad=prioridad)
    if search:
        ordenes = ordenes.filter(
            Q(cliente__icontains=search) |
            Q(direccion__icontains=search) |
            Q(telefono_cliente__icontains=search)
        )
    
    ordenes = ordenes.order_by('-fecha_creacion')
    
    context = {
        'ordenes': ordenes,
        'estado_actual': estado,
        'prioridad_actual': prioridad,
        'search_actual': search,
    }
    
    return render(request, 'core/orden_list.html', context)


@login_required
def orden_detail(request, pk):
    """Detalle de orden"""
    orden = get_object_or_404(Orden, pk=pk)
    movimientos = orden.movimientos.all().order_by('-timestamp')
    despachos = orden.despachos.all().order_by('-numero_despacho')
    # Excluir admin de la lista de repartidores
    repartidores = UsuarioProfile.objects.filter(
        rol='repartidor', 
        activo=True
    ).exclude(user__is_superuser=True)
    
    # Obtener farmacias activas
    farmacias = Farmacia.objects.filter(activa=True)
    
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    context = {
        'orden': orden,
        'movimientos': movimientos,
        'despachos': despachos,
        'repartidores': repartidores,
        'farmacias': farmacias,
        'user_profile': user_profile,
    }
    
    return render(request, 'core/orden_detail.html', context)


@login_required
def orden_create(request):
    """Crear nueva orden"""
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    if request.method == 'POST':
        form = OrdenForm(request.POST, user=request.user)
        if form.is_valid():
            orden = form.save()
            # Crear movimiento inicial
            OrdenMovimiento.objects.create(
                orden=orden,
                estado=orden.estado_actual,
                descripcion='Orden creada',
            )
            messages.success(request, 'Orden creada exitosamente.')
            return redirect('orden_detail', pk=orden.pk)
    else:
        form = OrdenForm(user=request.user)
        # Si es repartidor, no puede asignar responsable
        if user_profile.rol == 'repartidor':
            form.fields['responsable'].widget = forms.HiddenInput()
    
    return render(request, 'core/orden_form.html', {'form': form, 'title': 'Crear Orden'})


@login_required
def orden_edit(request, pk):
    """Editar orden - Solo coordinador o admin"""
    orden = get_object_or_404(Orden, pk=pk)
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Solo coordinador o admin pueden editar órdenes
    if user_profile.rol == 'repartidor':
        messages.error(request, 'No tienes permisos para editar órdenes.')
        return redirect('orden_detail', pk=pk)
    
    if request.method == 'POST':
        form = OrdenForm(request.POST, instance=orden, user=request.user)
        if form.is_valid():
            orden_anterior = Orden.objects.get(pk=pk)
            estado_anterior = orden_anterior.estado_actual
            
            orden = form.save()
            
            # Registrar cambio de estado si hubo
            if orden.estado_actual != estado_anterior:
                OrdenMovimiento.objects.create(
                    orden=orden,
                    estado=orden.estado_actual,
                    descripcion=f'Estado cambiado de {orden_anterior.get_estado_actual_display()} a {orden.get_estado_actual_display()}',
                    repartidor=UsuarioProfile.objects.filter(user=request.user).first(),
                )
            
            messages.success(request, 'Orden actualizada exitosamente.')
            return redirect('orden_detail', pk=orden.pk)
    else:
        form = OrdenForm(instance=orden, user=request.user)
        # Si es repartidor, no puede asignar responsable
        if user_profile.rol == 'repartidor':
            form.fields['responsable'].widget = forms.HiddenInput()
    
    return render(request, 'core/orden_form.html', {'form': form, 'orden': orden, 'title': 'Editar Orden'})


@login_required
def cambiar_estado_orden(request, pk):
    """Cambiar estado de orden"""
    orden = get_object_or_404(Orden, pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        descripcion = request.POST.get('descripcion', '')
        
        if nuevo_estado in dict(Orden.ESTADO_CHOICES):
            estado_anterior = orden.estado_actual
            orden.estado_actual = nuevo_estado
            
            # Si el nuevo estado es traslado, validar farmacias
            if nuevo_estado == 'traslado':
                farmacia_origen_id = request.POST.get('farmacia_origen')
                farmacia_destino_id = request.POST.get('farmacia_destino')
                
                if farmacia_origen_id:
                    orden.farmacia_origen = get_object_or_404(Farmacia, pk=farmacia_origen_id, activa=True)
                if farmacia_destino_id:
                    orden.farmacia_destino = get_object_or_404(Farmacia, pk=farmacia_destino_id, activa=True)
                
                # Validar que sean diferentes
                if orden.farmacia_origen and orden.farmacia_destino:
                    if orden.farmacia_origen == orden.farmacia_destino:
                        messages.error(request, 'La farmacia destino debe ser diferente de la farmacia origen.')
                        return redirect('orden_detail', pk=pk)
                
                # Validar que ambas estén seleccionadas
                if not orden.farmacia_origen or not orden.farmacia_destino:
                    messages.error(request, 'Debe seleccionar farmacia origen y destino para traslados.')
                    return redirect('orden_detail', pk=pk)
            
            orden.save()
            
            # Registrar movimiento
            OrdenMovimiento.objects.create(
                orden=orden,
                estado=nuevo_estado,
                descripcion=descripcion or f'Estado cambiado a {orden.get_estado_actual_display()}',
                repartidor=request.user.profile if hasattr(request.user, 'profile') else None,
            )
            
            messages.success(request, f'Estado cambiado a {orden.get_estado_actual_display()}.')
        else:
            messages.error(request, 'Estado inválido.')
    
    return redirect('orden_detail', pk=pk)


@login_required
def asignar_repartidor(request, pk):
    """Asignar repartidor a orden - Solo coordinador o admin"""
    orden = get_object_or_404(Orden, pk=pk)
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
        messages.error(request, 'No tienes permisos para asignar repartidores.')
        return redirect('orden_detail', pk=pk)
    
    if request.method == 'POST':
        repartidor_id = request.POST.get('repartidor')
        repartidor = get_object_or_404(
            UsuarioProfile, 
            pk=repartidor_id, 
            rol='repartidor'
        )
        
        # Validar que no sea admin
        if repartidor.user.is_superuser:
            messages.error(request, 'No se puede asignar un administrador como repartidor.')
            return redirect('orden_detail', pk=pk)
        
        # Validar que tenga moto
        if not repartidor.moto:
            messages.error(request, 'El repartidor debe tener una moto asignada.')
            return redirect('orden_detail', pk=pk)
        
        orden.responsable = repartidor
        orden.save()
        
        # Registrar movimiento
        OrdenMovimiento.objects.create(
            orden=orden,
            estado=orden.estado_actual,
            descripcion=f'Repartidor asignado: {repartidor.user.get_full_name()}',
            repartidor=repartidor,
        )
        
        messages.success(request, f'Repartidor {repartidor.user.get_full_name()} asignado.')
    
    return redirect('orden_detail', pk=pk)


@login_required
def despacho_list(request):
    """Lista de despachos - Solo muestra el último intento por orden"""
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Obtener todos los despachos base (sin filtros de estado/resultado para obtener el último de cada orden)
    despachos_todos = Despacho.objects.select_related('orden', 'repartidor__user').all()
    
    if user_profile.rol == 'repartidor':
        despachos_todos = despachos_todos.filter(repartidor=user_profile)
    
    # Obtener el último despacho de cada orden (el que tiene el numero_despacho más alto)
    from django.db.models import Max, Count
    
    # Primero, obtener los IDs de las órdenes que tienen despachos
    ordenes_con_despachos = despachos_todos.values_list('orden_id', flat=True).distinct()
    
    # Para cada orden, obtener el último despacho (mayor numero_despacho)
    ultimos_despachos_ids = []
    for orden_id in ordenes_con_despachos:
        ultimo_despacho = despachos_todos.filter(orden_id=orden_id).order_by('-numero_despacho').first()
        if ultimo_despacho:
            ultimos_despachos_ids.append(ultimo_despacho.id)
    
    # Filtrar solo los últimos despachos
    despachos = despachos_todos.filter(id__in=ultimos_despachos_ids)
    
    # Aplicar filtros de estado y resultado después de obtener los últimos despachos
    estado = request.GET.get('estado')
    resultado = request.GET.get('resultado')
    
    if estado:
        despachos = despachos.filter(estado=estado)
    if resultado:
        despachos = despachos.filter(resultado=resultado)
    
    # Anotar con el total de intentos por orden (contando todos los despachos de la orden)
    despachos = despachos.annotate(
        total_intentos=Count('orden__despachos')
    )
    
    despachos = despachos.order_by('-fecha')
    
    context = {
        'despachos': despachos,
        'estado_actual': estado,
        'resultado_actual': resultado,
    }
    
    return render(request, 'core/despacho_list.html', context)


@login_required
def despacho_detail(request, pk):
    """Detalle de despacho"""
    despacho = get_object_or_404(Despacho, pk=pk)
    
    context = {
        'despacho': despacho,
    }
    
    return render(request, 'core/despacho_detail.html', context)


@login_required
def despacho_create(request, orden_id):
    """Crear nuevo despacho para una orden"""
    orden = get_object_or_404(Orden, pk=orden_id)
    
    if request.method == 'POST':
        form = DespachoForm(request.POST, request.FILES)
        if form.is_valid():
            despacho = form.save(commit=False)
            despacho.orden = orden
            
            # Calcular número de despacho
            ultimo_despacho = Despacho.objects.filter(orden=orden).order_by('-numero_despacho').first()
            if ultimo_despacho:
                despacho.numero_despacho = ultimo_despacho.numero_despacho + 1
                despacho.estado = 're_despacho'
            else:
                despacho.numero_despacho = 1
                despacho.estado = 'despacho'
            
            despacho.save()
            
            # Actualizar estado de orden
            if despacho.resultado == 'entregado':
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
            
            messages.success(request, 'Despacho registrado exitosamente.')
            return redirect('orden_detail', pk=orden.pk)
    else:
        form = DespachoForm(initial={'repartidor': orden.responsable})
    
    return render(request, 'core/despacho_form.html', {'form': form, 'orden': orden})


@login_required
def moto_list(request):
    """Lista de motos"""
    motos = Moto.objects.all()
    
    estado = request.GET.get('estado')
    if estado:
        motos = motos.filter(estado=estado)
    
    motos = motos.order_by('patente')
    
    context = {
        'motos': motos,
        'estado_actual': estado,
    }
    
    return render(request, 'core/moto_list.html', context)


@login_required
def moto_detail(request, pk):
    """Detalle de moto"""
    moto = get_object_or_404(Moto, pk=pk)
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    # Excluir admin de la lista de repartidores
    repartidores = UsuarioProfile.objects.filter(
        rol='repartidor', 
        activo=True
    ).exclude(user__is_superuser=True)
    
    context = {
        'moto': moto,
        'repartidores': repartidores,
        'user_profile': user_profile,
    }
    
    return render(request, 'core/moto_detail.html', context)


@login_required
def moto_create(request):
    """Crear nueva moto"""
    if request.method == 'POST':
        form = MotoForm(request.POST)
        if form.is_valid():
            moto = form.save()
            messages.success(request, 'Moto creada exitosamente.')
            return redirect('moto_detail', pk=moto.pk)
    else:
        form = MotoForm()
    
    return render(request, 'core/moto_form.html', {'form': form, 'title': 'Crear Moto'})


@login_required
def moto_edit(request, pk):
    """Editar moto - Solo coordinador o admin"""
    moto = get_object_or_404(Moto, pk=pk)
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Solo coordinador o admin pueden editar motos
    if user_profile.rol == 'repartidor':
        messages.error(request, 'No tienes permisos para editar motos.')
        return redirect('moto_detail', pk=pk)
    
    if request.method == 'POST':
        form = MotoForm(request.POST, instance=moto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Moto actualizada exitosamente.')
            return redirect('moto_detail', pk=moto.pk)
    else:
        form = MotoForm(instance=moto)
    
    return render(request, 'core/moto_form.html', {'form': form, 'moto': moto, 'title': 'Editar Moto'})


@login_required
def asignar_moto_repartidor(request, moto_id):
    """Asignar moto a repartidor - Solo coordinador o admin"""
    moto = get_object_or_404(Moto, pk=moto_id)
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
        messages.error(request, 'No tienes permisos para asignar motos.')
        return redirect('moto_detail', pk=moto_id)
    
    if request.method == 'POST':
        repartidor_id = request.POST.get('repartidor')
        
        # Si repartidor_id está vacío, desasignar
        if not repartidor_id:
            if moto.repartidor_asignado:
                repartidor_anterior = moto.repartidor_asignado
                repartidor_anterior.moto = None
                repartidor_anterior.save()
                moto.estado = 'disponible'
                moto.save()
                messages.success(request, f'Repartidor desasignado de la moto {moto.patente}.')
            return redirect('moto_detail', pk=moto_id)
        
        repartidor = get_object_or_404(UsuarioProfile, pk=repartidor_id, rol='repartidor')
        
        # Validar que no sea admin
        if repartidor.user.is_superuser:
            messages.error(request, 'No se puede asignar una moto a un administrador.')
            return redirect('moto_detail', pk=moto_id)
        
        if moto.estado not in ['disponible', 'en_uso']:
            messages.error(request, 'La moto no está disponible para asignación.')
            return redirect('moto_detail', pk=moto_id)
        
        # Desasignar moto anterior del repartidor si tiene
        if repartidor.moto and repartidor.moto != moto:
            repartidor.moto.estado = 'disponible'
            repartidor.moto.save()
        
        # Desasignar repartidor anterior de esta moto si tiene
        if moto.repartidor_asignado and moto.repartidor_asignado != repartidor:
            moto.repartidor_asignado.moto = None
            moto.repartidor_asignado.save()
        
        # Asignar nueva moto
        repartidor.moto = moto
        repartidor.save()
        moto.estado = 'en_uso'
        moto.save()
        
        messages.success(request, f'Moto {moto.patente} asignada a {repartidor.user.get_full_name()}.')
    else:
        messages.error(request, 'Método no permitido.')
    
    return redirect('moto_detail', pk=moto_id)


@login_required
def reporte_list(request):
    """Lista de reportes"""
    reportes = Reporte.objects.all().order_by('-fecha')
    
    context = {
        'reportes': reportes,
    }
    
    return render(request, 'core/reporte_list.html', context)


@login_required
def reporte_export_csv(request, pk):
    """Exportar reporte a CSV"""
    reporte = get_object_or_404(Reporte, pk=pk)
    
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


# ========== VISTAS DE USUARIOS ==========

@login_required
def usuario_list(request):
    """Lista de usuarios - Permisos según rol"""
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Filtros según rol
    if user_profile.rol == 'repartidor':
        # Repartidor solo se ve a sí mismo
        usuarios = UsuarioProfile.objects.filter(pk=user_profile.pk)
    else:
        # Admin y coordinador ven todos los usuarios
        usuarios = UsuarioProfile.objects.select_related('user', 'moto').all()
        
        # Filtros opcionales
        rol_filter = request.GET.get('rol')
        activo_filter = request.GET.get('activo')
        
        if rol_filter:
            usuarios = usuarios.filter(rol=rol_filter)
        if activo_filter == 'true':
            usuarios = usuarios.filter(activo=True)
        elif activo_filter == 'false':
            usuarios = usuarios.filter(activo=False)
    
    usuarios = usuarios.order_by('-fecha_creacion')
    
    context = {
        'usuarios': usuarios,
        'user_profile': user_profile,
        'rol_actual': request.GET.get('rol', ''),
        'activo_actual': request.GET.get('activo', ''),
    }
    
    return render(request, 'core/usuario_list.html', context)


@login_required
def usuario_create(request):
    """Crear nuevo usuario - Solo admin"""
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Solo admin puede crear usuarios
    if user_profile.rol != 'admin':
        messages.error(request, 'No tienes permisos para crear usuarios.')
        return redirect('usuario_list')
    
    if request.method == 'POST':
        user_form = UsuarioForm(request.POST)
        profile_form = UsuarioProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Crear usuario (el signal creará automáticamente el perfil)
            user = user_form.save()
            
            # Obtener o crear el perfil (debería existir por el signal)
            profile, created = UsuarioProfile.objects.get_or_create(
                user=user,
                defaults={
                    'telefono': '',
                    'rol': 'repartidor',
                    'estado_turno': 'disponible',
                    'activo': True,
                }
            )
            
            # Actualizar el perfil con los datos del formulario
            profile.telefono = profile_form.cleaned_data.get('telefono', '')
            profile.rut = profile_form.cleaned_data.get('rut', '')
            profile.rol = profile_form.cleaned_data.get('rol', 'repartidor')
            profile.estado_turno = profile_form.cleaned_data.get('estado_turno', 'disponible')
            profile.activo = profile_form.cleaned_data.get('activo', True)
            profile.moto = profile_form.cleaned_data.get('moto')
            profile.save()
            
            # Si se asignó una moto, actualizar su estado
            if profile.moto:
                profile.moto.estado = 'en_uso'
                profile.moto.save()
            
            messages.success(request, f'Usuario {user.username} creado exitosamente.')
            return redirect('usuario_detail', pk=profile.pk)
    else:
        user_form = UsuarioForm()
        profile_form = UsuarioProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Crear Usuario',
    }
    
    return render(request, 'core/usuario_form.html', context)


@login_required
def usuario_edit(request, pk):
    """Editar usuario - Admin puede editar todo, coordinador solo puede cambiar moto"""
    usuario = get_object_or_404(UsuarioProfile, pk=pk)
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Repartidor solo puede verse a sí mismo
    if user_profile.rol == 'repartidor' and usuario.pk != user_profile.pk:
        messages.error(request, 'No tienes permisos para editar otros usuarios.')
        return redirect('usuario_list')
    
    if request.method == 'POST':
        if user_profile.rol == 'admin':
            # Admin puede editar todo
            user_form = UsuarioForm(request.POST, instance=usuario.user)
            profile_form = UsuarioProfileForm(request.POST, instance=usuario)
            
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                profile = profile_form.save()
                
                # Si se asignó una moto, actualizar su estado
                if profile.moto:
                    profile.moto.estado = 'en_uso'
                    profile.moto.save()
                
                messages.success(request, f'Usuario {user.username} actualizado exitosamente.')
                return redirect('usuario_detail', pk=profile.pk)
        elif user_profile.rol == 'coordinador':
            # Coordinador solo puede cambiar la moto
            moto_id = request.POST.get('moto')
            moto_anterior = usuario.moto
            
            if moto_id:
                moto = get_object_or_404(Moto, pk=moto_id, activa=True)
                usuario.moto = moto
                moto.estado = 'en_uso'
                moto.save()
            else:
                usuario.moto = None
            
            # Liberar moto anterior si había una
            if moto_anterior and moto_anterior != usuario.moto:
                moto_anterior.estado = 'disponible'
                moto_anterior.save()
            
            usuario.save()
            messages.success(request, 'Moto actualizada exitosamente.')
            return redirect('usuario_detail', pk=usuario.pk)
    else:
        if user_profile.rol == 'admin':
            user_form = UsuarioForm(instance=usuario.user)
            profile_form = UsuarioProfileForm(instance=usuario)
        else:
            user_form = None
            profile_form = None
    
    context = {
        'usuario': usuario,
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
        'title': 'Editar Usuario',
    }
    
    return render(request, 'core/usuario_form.html', context)


@login_required
def usuario_detail(request, pk):
    """Detalle de usuario"""
    usuario = get_object_or_404(UsuarioProfile.objects.select_related('user', 'moto'), pk=pk)
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Repartidor solo puede verse a sí mismo
    if user_profile.rol == 'repartidor' and usuario.pk != user_profile.pk:
        messages.error(request, 'No tienes permisos para ver otros usuarios.')
        return redirect('usuario_list')
    
    # Obtener motos disponibles para coordinador
    motos_disponibles = None
    if user_profile.rol == 'coordinador':
        motos_disponibles = Moto.objects.filter(
            activa=True
        ).filter(
            Q(estado='disponible') | Q(estado='en_uso')
        )
    
    context = {
        'usuario': usuario,
        'user_profile': user_profile,
        'motos_disponibles': motos_disponibles,
    }
    
    return render(request, 'core/usuario_detail.html', context)


@login_required
def cambiar_estado_turno(request, pk):
    """Cambiar estado de turno - Solo repartidor puede cambiar su propio estado"""
    usuario = get_object_or_404(UsuarioProfile, pk=pk)
    user_profile, _ = UsuarioProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'telefono': '',
            'rol': 'repartidor',
            'estado_turno': 'disponible',
            'activo': True,
        }
    )
    
    # Solo repartidor puede cambiar su propio estado
    if user_profile.rol != 'repartidor' or usuario.pk != user_profile.pk:
        messages.error(request, 'No tienes permisos para cambiar el estado de turno.')
        return redirect('usuario_detail', pk=pk)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado_turno')
        
        if nuevo_estado not in dict(UsuarioProfile.ESTADO_TURNO_CHOICES):
            messages.error(request, 'Estado inválido.')
            return redirect('usuario_detail', pk=pk)
        
        # Validación especial para descanso
        if nuevo_estado == 'descanso':
            # Si ya está en descanso, verificar que no haya pasado 1 hora
            if usuario.estado_turno == 'descanso' and usuario.fecha_inicio_descanso:
                tiempo_descanso = timezone.now() - usuario.fecha_inicio_descanso
                if tiempo_descanso >= timedelta(hours=1):
                    messages.warning(request, 'Has excedido el tiempo máximo de descanso (1 hora). Cambiando a disponible.')
                    usuario.estado_turno = 'disponible'
                    usuario.fecha_inicio_descanso = None
                else:
                    tiempo_restante = timedelta(hours=1) - tiempo_descanso
                    minutos_restantes = int(tiempo_restante.total_seconds() / 60)
                    messages.info(request, f'Estás en descanso. Tiempo restante: {minutos_restantes} minutos.')
                    return redirect('usuario_detail', pk=pk)
            else:
                # Iniciar descanso
                usuario.estado_turno = 'descanso'
                usuario.fecha_inicio_descanso = timezone.now()
        else:
            # Si cambia de descanso a otro estado, limpiar fecha_inicio_descanso
            if usuario.estado_turno == 'descanso':
                usuario.fecha_inicio_descanso = None
            usuario.estado_turno = nuevo_estado
        
        usuario.save()
        messages.success(request, f'Estado de turno cambiado a {usuario.get_estado_turno_display()}.')
    
    return redirect('usuario_detail', pk=pk)

