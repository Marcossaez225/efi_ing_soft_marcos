from django.contrib.auth.models import User
from rest_framework import generics, permissions
from vehicles.models import Brand, Vehicle, Comment, Client
from api.serializers.serializers import (
    BrandSerializer,
    VehicleSerializer,
    CommentSerializer,
    UserSerializer,
    ClientSerializer,
)


# Listado de Marcas
class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# Listado de Autos
class VehicleListView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

# Listado de Usuarios
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Solo accesible para administradores

# Listado de Comentarios de un Auto en particular
class VehicleCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        vehicle_id = self.kwargs['vehicle_id']
        return Comment.objects.filter(vehicle__id=vehicle_id)

class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]


class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]