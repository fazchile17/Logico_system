from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UsuarioProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea automáticamente un UsuarioProfile cuando se crea un User"""
    if created:
        UsuarioProfile.objects.get_or_create(
            user=instance,
            defaults={
                'telefono': '',
                'rol': 'repartidor',
                'estado_turno': 'disponible',
                'activo': True,
            }
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el perfil cuando se guarda el usuario"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

