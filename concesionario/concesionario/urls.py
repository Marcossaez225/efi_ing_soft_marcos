from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import HomePageView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Concesionario API",
        default_version='v1',
        description="Documentación de la API para el proyecto de concesionaria",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# URLs sin soporte de internacionalización para la API
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Coloca la API fuera de i18n_patterns
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-doc'),  # URL adicional para Swagger
    path('i18n/', include('django.conf.urls.i18n')),  # Soporte para selector de idioma
]

# URLs con soporte de internacionalización para el resto del sitio
urlpatterns += i18n_patterns(
    path('vehicles/', include('vehicles.urls')),
    path('users/', include('users.urls')),
    path('', HomePageView.as_view(), name='home'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
