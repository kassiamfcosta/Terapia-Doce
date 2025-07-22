# backend/urls.py - Versão Corrigida
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({'status': 'API Terapia Doce rodando ✅'})

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # APIs de cada app
    path('api/clients/', include('clients.api.urls')),
    path('api/admins/', include('admins.api.urls')),
    path('api/core/', include('core.api.urls')),
    
    # Rota raiz
    path('', home_view, name='home'),
]