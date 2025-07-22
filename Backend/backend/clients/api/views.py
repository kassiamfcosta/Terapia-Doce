from rest_framework import viewsets
from clients.models import Client
from .serializers import ClientSerializer
from backend.api.permissions import IsAuthenticatedOrCreateOnly

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def get_queryset(self):
        # Usuário só vê o próprio perfil, exceto staff
        user = self.request.user
        if user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(user=user)

    def perform_create(self, serializer):
        # Associa o objeto Client ao usuário logado
        serializer.save(user=self.request.user)
