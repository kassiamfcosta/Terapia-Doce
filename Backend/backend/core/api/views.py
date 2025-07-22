from rest_framework import viewsets, permissions
from core.models import Product, Purchase, PurchaseItem, ProductAction
from .serializers import (
    ProductSerializer, PurchaseSerializer,
    PurchaseItemSerializer, ProductActionSerializer
)
from backend.api.permissions import IsAdminStaff

# 1) Produtos — apenas staff
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminStaff]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.admin)
    def perform_update(self, serializer):
        instance = serializer.save()
        ProductAction.objects.create(
            admin=self.request.user.admin,
            product=instance,
            action_type='update'
        )
    def perform_destroy(self, instance):
        ProductAction.objects.create(
            admin=self.request.user.admin,
            product=instance,
            action_type='delete'
        )
        instance.delete()

# 2) Compras — usuário autenticado
class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]  # import rest_framework.permissions

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Purchase.objects.all()
        return Purchase.objects.filter(client__user=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.client)

# 3) Itens de compra — exposto apenas para leitura (aninhamento no Purchase)
class PurchaseItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [permissions.IsAuthenticated]

# 4) Ações de produto — somente leitura para staff
class ProductActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductAction.objects.all()
    serializer_class = ProductActionSerializer
    permission_classes = [IsAdminStaff]
