from rest_framework import viewsets
from admins.models import Admin
from .serializers import AdminSerializer
from backend.api.permissions import IsAdminStaff

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminStaff]

    # Staff pode criar, editar e apagar administradores
