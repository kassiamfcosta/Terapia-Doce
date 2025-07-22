# clients/api/views.py
from rest_framework import viewsets
from clients.models import Client
from .serializers import ClientSerializer
from backend.api.permissions import IsAuthenticatedOrCreateOnly

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Client.objects.all()
        # Filtrar apenas o cliente do usuário logado
        try:
            return Client.objects.filter(user=user)
        except:
            return Client.objects.none()

    def perform_create(self, serializer):
        # Verificar se é um usuário autenticado criando seu próprio perfil
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Para criação sem autenticação (registro)
            serializer.save()