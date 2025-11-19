from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.urls import reverse


class UsuarioProfile(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('coordinador', 'Coordinador'),
        ('repartidor', 'Repartidor'),
    ]
    
    ESTADO_TURNO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('descanso', 'Descanso'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rut = models.CharField(max_length=12, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='repartidor')
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)
    moto = models.OneToOneField('Moto', on_delete=models.SET_NULL, blank=True, null=True, related_name='usuario_asignado')
    estado_turno = models.CharField(max_length=20, choices=ESTADO_TURNO_CHOICES, default='disponible')
    fecha_inicio_descanso = models.DateTimeField(blank=True, null=True, help_text='Fecha y hora en que inició el descanso')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_rol_display()})"
    
    def get_absolute_url(self):
        return reverse('usuario_detail', kwargs={'pk': self.pk})


class Moto(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_uso', 'En Uso'),
        ('mantenimiento', 'Mantenimiento'),
        ('fuera_servicio', 'Fuera de Servicio'),
    ]
    
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField(validators=[MinValueValidator(1900)])
    color = models.CharField(max_length=30)
    cilindrada = models.IntegerField(validators=[MinValueValidator(0)])
    kilometraje = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_ultimo_mantenimiento = models.DateField(blank=True, null=True)
    proximo_mantenimiento = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Moto'
        verbose_name_plural = 'Motos'
        ordering = ['patente']
    
    def __str__(self):
        return f"{self.patente} - {self.marca} {self.modelo}"
    
    @property
    def repartidor_asignado(self):
        try:
            return UsuarioProfile.objects.get(moto=self)
        except UsuarioProfile.DoesNotExist:
            return None
    
    @property
    def dias_sin_mantenimiento(self):
        if self.fecha_ultimo_mantenimiento:
            return (timezone.now().date() - self.fecha_ultimo_mantenimiento).days
        return None
    
    def get_absolute_url(self):
        return reverse('moto_detail', kwargs={'pk': self.pk})


class Farmacia(models.Model):
    """Modelo para representar farmacias"""
    nombre = models.CharField(max_length=200)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100, default='Santiago')
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Farmacia'
        verbose_name_plural = 'Farmacias'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"
    
    def get_absolute_url(self):
        return reverse('farmacia_detail', kwargs={'pk': self.pk})


class Orden(models.Model):
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]
    
    TIPO_CHOICES = [
        ('receta_detendida', 'Receta Detenida'),
        ('normal', 'Normal'),
    ]
    
    ESTADO_CHOICES = [
        ('retiro_receta', 'Retiro de Receta'),
        ('traslado', 'Traslado'),
        ('despacho', 'Despacho'),
        ('re_despacho', 'Re-despacho'),
    ]
    
    cliente = models.CharField(max_length=200)
    direccion = models.TextField()
    telefono_cliente = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True)
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='normal')
    estado_actual = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='retiro_receta')
    farmacia_origen = models.ForeignKey('Farmacia', on_delete=models.SET_NULL, blank=True, null=True, related_name='ordenes_origen', verbose_name='Farmacia Origen')
    farmacia_destino = models.ForeignKey('Farmacia', on_delete=models.SET_NULL, blank=True, null=True, related_name='ordenes_destino', verbose_name='Farmacia Destino')
    responsable = models.ForeignKey(UsuarioProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='ordenes_asignadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Orden #{self.id} - {self.cliente}"
    
    def save(self, *args, **kwargs):
        # Prioridad automática según tipo
        if self.tipo == 'receta_detendida' and not self.prioridad:
            self.prioridad = 'alta'
        elif self.tipo == 'normal' and not self.prioridad:
            self.prioridad = 'media'
        
        # Validar que farmacia_destino sea diferente de farmacia_origen
        if self.farmacia_origen and self.farmacia_destino:
            if self.farmacia_origen == self.farmacia_destino:
                raise ValueError('La farmacia destino debe ser diferente de la farmacia origen')
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('orden_detail', kwargs={'pk': self.pk})


class Medicamento(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='medicamentos')
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} (x{self.cantidad}) - Orden #{self.orden.id}"


class Despacho(models.Model):
    ESTADO_CHOICES = [
        ('despacho', 'Despacho'),
        ('re_despacho', 'Re-despacho'),
    ]
    
    RESULTADO_CHOICES = [
        ('entregado', 'Entregado'),
        ('no_disponible', 'No Disponible'),
        ('error', 'Error'),
    ]
    
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='despachos')
    numero_despacho = models.IntegerField(default=1)
    repartidor = models.ForeignKey(UsuarioProfile, on_delete=models.SET_NULL, null=True, related_name='despachos')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='despacho')
    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES, blank=True, null=True)
    foto_entrega = models.ImageField(upload_to='fotos_entregas/', blank=True, null=True)
    observaciones = models.TextField(blank=True)
    coordenadas_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    coordenadas_lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Despacho'
        verbose_name_plural = 'Despachos'
        ordering = ['-fecha']
        unique_together = ['orden', 'numero_despacho']
    
    def __str__(self):
        return f"Despacho #{self.numero_despacho} - Orden #{self.orden.id}"
    
    def save(self, *args, **kwargs):
        if not self.numero_despacho:
            # Obtener el último número de despacho para esta orden
            ultimo_despacho = Despacho.objects.filter(orden=self.orden).order_by('-numero_despacho').first()
            if ultimo_despacho:
                self.numero_despacho = ultimo_despacho.numero_despacho + 1
            else:
                self.numero_despacho = 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('despacho_detail', kwargs={'pk': self.pk})


class OrdenMovimiento(models.Model):
    ESTADO_CHOICES = [
        ('retiro_receta', 'Retiro de Receta'),
        ('traslado', 'Traslado'),
        ('despacho', 'Despacho'),
        ('re_despacho', 'Re-despacho'),
    ]
    
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='movimientos')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    descripcion = models.TextField(blank=True)
    repartidor = models.ForeignKey(UsuarioProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='movimientos')
    despacho = models.ForeignKey(Despacho, on_delete=models.SET_NULL, blank=True, null=True, related_name='movimientos')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Movimiento de Orden'
        verbose_name_plural = 'Movimientos de Órdenes'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.orden} - {self.get_estado_display()} ({self.timestamp})"


class Ruta(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    zona = models.CharField(max_length=100)
    vehiculo = models.CharField(max_length=100, blank=True)
    repartidor = models.ForeignKey(UsuarioProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='rutas')
    activa = models.BooleanField(default=True)
    ordenes = models.ManyToManyField(Orden, related_name='rutas', blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.zona}"
    
    def get_google_maps_url(self):
        """Genera URL de Google Maps con múltiples destinos"""
        if not self.ordenes.exists():
            return None
        
        ordenes_list = list(self.ordenes.all())
        if len(ordenes_list) == 1:
            destino = ordenes_list[0].direccion.replace(' ', '+')
            return f"https://www.google.com/maps/dir/?api=1&destination={destino}"
        
        # Múltiples destinos
        waypoints = '|'.join([orden.direccion.replace(' ', '+') for orden in ordenes_list[:-1]])
        destino = ordenes_list[-1].direccion.replace(' ', '+')
        return f"https://www.google.com/maps/dir/?api=1&destination={destino}&waypoints={waypoints}"
    
    def get_absolute_url(self):
        return reverse('ruta_detail', kwargs={'pk': self.pk})


class Reporte(models.Model):
    fecha = models.DateField(unique=True)
    entregas_totales = models.IntegerField(default=0)
    entregas_exitosas = models.IntegerField(default=0)
    entregas_fallidas = models.IntegerField(default=0)
    tiempo_promedio = models.DurationField(blank=True, null=True)
    ingresos_dia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Reporte {self.fecha}"
    
    @property
    def tasa_exito(self):
        if self.entregas_totales > 0:
            return (self.entregas_exitosas / self.entregas_totales) * 100
        return 0
    
    def get_absolute_url(self):
        return reverse('reporte_detail', kwargs={'pk': self.pk})

