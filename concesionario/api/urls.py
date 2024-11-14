from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api.views.views import (
    BrandListView, VehicleListView, UserListView, VehicleCommentListView, ClientCreateView, ClientListView
)

app_name = "api"

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('vehicles/<int:vehicle_id>/comments/', VehicleCommentListView.as_view(), name='vehicle-comments'),
    path('clients/create/', ClientCreateView.as_view(), name='client-create'),  # Crear clientes
    path('clients/', ClientListView.as_view(), name='client-list'),  # Listar todos los clientes
    path('token-auth/', obtain_auth_token, name='token-auth'),  # Nuevo endpoint para obtener tokens
]
