# media/urls.py

from django.urls import path
from .views import ImageUploadView

urlpatterns = [
    path('<int:vehicle_id>/upload/', ImageUploadView.as_view(), name='image_upload'),
]
