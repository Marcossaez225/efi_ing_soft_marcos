from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response  
from rest_framework.permissions import AllowAny
from vehicles.models import Brand, Vehicle, Comment, Client
from api.serializers.serializers import (
    BrandSerializer,
    VehicleSerializer,
    CommentSerializer,
    UserSerializer,
    ClientSerializer,
    VehicleSummarySerializer,
)

# Listado de Marcas (accesible sin autenticación)
class BrandListView(generics.ListAPIView):
    """
    Devuelve un listado de todas las marcas disponibles.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]  # Público

# Listado de Autos (accesible sin autenticación)
class VehicleListView(generics.ListAPIView):
    """
    Devuelve un listado de todos los autos, incluyendo información de la marca.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [AllowAny]  # Público

# Listado de Usuarios (solo accesible para Admin)
class UserListView(generics.ListAPIView):
    """
    Devuelve un listado de todos los usuarios registrados.
    **Requiere permisos de administrador**.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# Listado de Comentarios de un Auto en particular
class VehicleCommentListView(generics.GenericAPIView):
    """
    Devuelve los comentarios asociados a un vehículo específico.
    Incluye información básica del vehículo.
    """
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # Público

    def get(self, request, *args, **kwargs):
        vehicle_id = self.kwargs['vehicle_id']
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle_data = VehicleSummarySerializer(vehicle).data
            comments = Comment.objects.filter(vehicle=vehicle)
            comments_data = self.get_serializer(comments, many=True).data
            return Response({
                "vehicle_info": vehicle_data,
                "comments": comments_data
            }, status=status.HTTP_200_OK)

        except Vehicle.DoesNotExist:
            return Response({"detail": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)

# Crear un nuevo cliente (solo para usuarios con is_staff=True)
class ClientCreateView(generics.CreateAPIView):
    """
    Crea un nuevo cliente.
    **Requiere que el usuario tenga permisos de staff (is_staff=True)**.

    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]  # Restringido a usuarios staff

# Listado de Clientes (solo para Admin o usuarios staff)
class ClientListView(generics.ListAPIView):
    """
    Devuelve un listado de todos los clientes registrados.
    **Requiere que el usuario tenga permisos de staff (is_staff=True)**.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]  # Restringido a usuarios staff
