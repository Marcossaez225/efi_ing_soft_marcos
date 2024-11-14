from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import HomePageView

# Importaciones para drf_yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de drf_yasg para la documentación de la API
schema_view = get_schema_view(
    openapi.Info(
        title="Concesionaria API",
        default_version='v1',
        description="Documentación de la API para el proyecto de concesionaria",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Incluye todas las rutas de la API bajo 'api/'
    path('vehicles/', include('vehicles.urls')),  # Incluye las rutas de 'vehicles' sin prefijo 'api/'
    path('users/', include('users.urls')),  # Incluye las rutas de 'users' para manejar el perfil y autenticación
    path('', HomePageView.as_view(), name='home'),
    # URL para Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
