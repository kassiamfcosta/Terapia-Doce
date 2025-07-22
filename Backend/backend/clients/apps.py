# clients/apps.py - Registrar signals
from django.apps import AppConfig

class ClientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clients'
    
    def ready(self):
        import clients.signals  # Importar signals quando o app estiver pronto