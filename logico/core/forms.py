from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Orden, Medicamento, Despacho, Moto, Ruta, UsuarioProfile, Farmacia


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = [
            'cliente', 'direccion', 'telefono_cliente', 'descripcion',
            'prioridad', 'tipo', 'estado_actual', 'farmacia_origen', 
            'farmacia_destino', 'responsable'
        ]
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefono_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'estado_actual': forms.Select(attrs={'class': 'form-select'}),
            'farmacia_origen': forms.Select(attrs={'class': 'form-select'}),
            'farmacia_destino': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Excluir admin de la lista de repartidores
        self.fields['responsable'].queryset = UsuarioProfile.objects.filter(
            rol='repartidor', 
            activo=True
        ).exclude(user__is_superuser=True)
        self.fields['responsable'].required = False
        
        # Configurar farmacias
        self.fields['farmacia_origen'].queryset = Farmacia.objects.filter(activa=True)
        self.fields['farmacia_origen'].required = False
        self.fields['farmacia_destino'].queryset = Farmacia.objects.filter(activa=True)
        self.fields['farmacia_destino'].required = False
        
        # Si hay una instancia (edición), excluir farmacia_origen de farmacia_destino
        if self.instance and self.instance.pk and self.instance.farmacia_origen:
            self.fields['farmacia_destino'].queryset = Farmacia.objects.filter(
                activa=True
            ).exclude(pk=self.instance.farmacia_origen.pk)
    
    def clean(self):
        cleaned_data = super().clean()
        farmacia_origen = cleaned_data.get('farmacia_origen')
        farmacia_destino = cleaned_data.get('farmacia_destino')
        
        # Validar que si hay traslado, haya farmacias
        estado_actual = cleaned_data.get('estado_actual')
        if estado_actual == 'traslado':
            if not farmacia_origen:
                raise forms.ValidationError({
                    'farmacia_origen': 'La farmacia origen es requerida para traslados.'
                })
            if not farmacia_destino:
                raise forms.ValidationError({
                    'farmacia_destino': 'La farmacia destino es requerida para traslados.'
                })
        
        # Validar que farmacia_destino sea diferente de farmacia_origen
        if farmacia_origen and farmacia_destino:
            if farmacia_origen == farmacia_destino:
                raise forms.ValidationError({
                    'farmacia_destino': 'La farmacia destino debe ser diferente de la farmacia origen.'
                })
        
        return cleaned_data


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['codigo', 'nombre', 'cantidad', 'observaciones']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class DespachoForm(forms.ModelForm):
    class Meta:
        model = Despacho
        fields = [
            'repartidor', 'resultado', 'foto_entrega', 
            'observaciones', 'coordenadas_lat', 'coordenadas_lng'
        ]
        widgets = {
            'repartidor': forms.Select(attrs={'class': 'form-select'}),
            'resultado': forms.Select(attrs={'class': 'form-select'}),
            'foto_entrega': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'coordenadas_lat': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'coordenadas_lng': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir admin de la lista de repartidores
        self.fields['repartidor'].queryset = UsuarioProfile.objects.filter(
            rol='repartidor', 
            activo=True
        ).exclude(user__is_superuser=True)
        self.fields['resultado'].required = False
        self.fields['coordenadas_lat'].required = False
        self.fields['coordenadas_lng'].required = False


class MotoForm(forms.ModelForm):
    class Meta:
        model = Moto
        fields = [
            'patente', 'marca', 'modelo', 'año', 'color',
            'cilindrada', 'kilometraje', 'estado',
            'fecha_ultimo_mantenimiento', 'proximo_mantenimiento',
            'observaciones', 'activa'
        ]
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'año': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'cilindrada': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ultimo_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proximo_mantenimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ['nombre', 'descripcion', 'zona', 'vehiculo', 'repartidor', 'activa', 'ordenes']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'zona': forms.TextInput(attrs={'class': 'form-control'}),
            'vehiculo': forms.TextInput(attrs={'class': 'form-control'}),
            'repartidor': forms.Select(attrs={'class': 'form-select'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ordenes': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 10}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Excluir admin de la lista de repartidores
        self.fields['repartidor'].queryset = UsuarioProfile.objects.filter(
            rol='repartidor', 
            activo=True
        ).exclude(user__is_superuser=True)
        self.fields['repartidor'].required = False
        self.fields['ordenes'].queryset = Orden.objects.all()
        self.fields['ordenes'].required = False


class UsuarioForm(forms.ModelForm):
    """Formulario para crear/editar usuario (User model)"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Dejar en blanco si no deseas cambiar la contraseña'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Confirmar Contraseña'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es un usuario nuevo, la contraseña es requerida
        if not self.instance.pk:
            self.fields['password'].required = True
            self.fields['password_confirm'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Si es un usuario nuevo, la contraseña es requerida
        if not self.instance.pk and not password:
            raise forms.ValidationError({'password': 'La contraseña es requerida para nuevos usuarios.'})
        
        if password and password != password_confirm:
            raise forms.ValidationError({'password_confirm': 'Las contraseñas no coinciden.'})
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UsuarioProfileForm(forms.ModelForm):
    """Formulario para crear/editar perfil de usuario"""
    class Meta:
        model = UsuarioProfile
        fields = ['rut', 'telefono', 'rol', 'moto', 'activo']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'moto': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar motos disponibles o en uso
        self.fields['moto'].queryset = Moto.objects.filter(
            activa=True
        ).filter(
            Q(estado='disponible') | Q(estado='en_uso')
        )
        self.fields['moto'].required = False
        self.fields['telefono'].required = True

