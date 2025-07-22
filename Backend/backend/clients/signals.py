# clients/signals.py (arquivo novo)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Client

@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    """
    Cria automaticamente um perfil de Client quando um User é criado
    (apenas se não for staff)
    """
    if created and not instance.is_staff:
        Client.objects.create(
            user=instance,
            name=instance.get_full_name() or instance.username,
            email=instance.email
        )