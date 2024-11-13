from django.urls import path
from .views import (
    VehicleListView,
    VehicleDetailView,
    VehicleCreateView,
    VehicleUpdateView,
    follow_vehicle,
    unfollow_vehicle,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    ImageUploadView
)

urlpatterns = [
    # Listar todos los vehículos
    path('', VehicleListView.as_view(), name='vehicle_list'),

    # Detalles de un vehículo específico
    path('<int:pk>/', VehicleDetailView.as_view(), name='vehicle_detail'),

    # Crear un nuevo vehículo
    path('create/', VehicleCreateView.as_view(), name='vehicle_create'),

    # Actualizar un vehículo existente
    path('<int:pk>/update/', VehicleUpdateView.as_view(), name='vehicle_update'),

    # Seguir un vehículo
    path('<int:vehicle_id>/follow/', follow_vehicle, name='follow_vehicle'),

    # Dejar de seguir un vehículo
    path('<int:vehicle_id>/unfollow/', unfollow_vehicle, name='unfollow_vehicle'),

    # Crear un comentario
    path('comments/create/<int:vehicle_id>/', CommentCreateView.as_view(), name='comment_create'),

    # Actualizar un comentario existente
    path('comments/update/<int:pk>/', CommentUpdateView.as_view(), name='comment_update'),

    # Eliminar un comentario
    path('comments/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),

    # Subir una imagen para un vehículo
    path('images/<int:vehicle_id>/upload/', ImageUploadView.as_view(), name='image_upload'),
]
