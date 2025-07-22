# admins/signals.py (arquivo novo)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Admin

@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
    """
    Cria automaticamente um perfil de Admin quando um User staff é criado
    """
    if created and instance.is_staff:
        Admin.objects.create(
            user=instance,
            name=instance.get_full_name() or instance.username,
            email=instance.email,
            role='admin'
        )