# vehicles/urls.py

from django.urls import path
from .views import VehicleListView, VehicleDetailView, VehicleCreateView, VehicleUpdateView

urlpatterns = [
    path('', VehicleListView.as_view(), name='vehicle_list'),
    path('<int:pk>/', VehicleDetailView.as_view(), name='vehicle_detail'),
    path('create/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('<int:pk>/update/', VehicleUpdateView.as_view(), name='vehicle_update'),
]
