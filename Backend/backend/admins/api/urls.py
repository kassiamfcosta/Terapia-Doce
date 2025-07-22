from rest_framework.routers import DefaultRouter
from .views import AdminViewSet

router = DefaultRouter()
router.register('admins', AdminViewSet, basename='admin')

urlpatterns = router.urls
