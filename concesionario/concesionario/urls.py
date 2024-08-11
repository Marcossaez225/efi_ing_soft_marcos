# concesionario/concesionario/urls.py

from django.contrib import admin
from django.urls import path, include
from .views import HomePageView  # Importa la vista de la página de inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vehicles/', include('vehicles.urls')),
    path('', HomePageView.as_view(), name='home'),  # Ruta para la página de inicio
    # path('users/', include('users.urls')),
    # path('comments/', include('comments.urls')),
    # path('media/', include('media.urls')),
]
