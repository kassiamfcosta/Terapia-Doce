# core/api/urls.py - Versão Corrigida
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    PurchaseViewSet,
    PurchaseItemViewSet,
    ProductActionViewSet,
)

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('purchases', PurchaseViewSet, basename='purchase')
router.register('items', PurchaseItemViewSet, basename='purchaseitem')
router.register('actions', ProductActionViewSet, basename='productaction')

urlpatterns = router.urls