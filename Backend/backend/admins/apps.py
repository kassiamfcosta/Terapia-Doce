# admins/apps.py - Registrar signals
from django.apps import AppConfig

class AdminsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admins'
    
    def ready(self):
        import admins.signals