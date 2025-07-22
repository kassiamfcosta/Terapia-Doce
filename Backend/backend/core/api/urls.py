from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    PurchaseViewSet,
    PurchaseItemViewSet,
    ProductActionViewSet,
)
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('purchases', PurchaseViewSet, basename='purchase')
router.register('items', PurchaseItemViewSet, basename='purchaseitem')
router.register('actions', ProductActionViewSet, basename='productaction')

urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rotas da API
    path('api/clients/', include('clients.api.urls')),
    path('api/admins/',  include('admins.api.urls')),
    path('api/core/',    include('core.api.urls')),

    # Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # (Opcional) resposta amigável na raiz do site
    path('', lambda request: JsonResponse({'status': 'API Terapia Doce rodando ✅'})),
]