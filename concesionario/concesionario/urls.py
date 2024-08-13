from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vehicles/', include('vehicles.urls')),
    path('media/', include('media.urls')),
    path('users/', include('users.urls')), 
    path('comments/', include('comments.urls')),
    path('', HomePageView.as_view(), name='home'),
]

if settings.DEBUG:
    # Sirve archivos multimedia
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
