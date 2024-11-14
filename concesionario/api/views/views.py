from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from vehicles.models import Brand, Vehicle, Comment, Client
from api.serializers.serializers import (
    BrandSerializer,
    VehicleSerializer,
    CommentSerializer,
    UserSerializer,
    ClientSerializer,
    VehicleSummarySerializer,
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
    permission_classes = [permissions.IsAdminUser]

# Listado de Comentarios de un Auto en particular con detalles de vehículo
class VehicleCommentListView(generics.GenericAPIView):
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        vehicle_id = self.kwargs['vehicle_id']
        try:
            # Obtener los detalles del vehículo en formato resumido
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle_data = VehicleSummarySerializer(vehicle).data

            # Obtener comentarios asociados al vehículo
            comments = Comment.objects.filter(vehicle=vehicle)
            comments_data = self.get_serializer(comments, many=True).data

            # Estructurar la respuesta con detalles del vehículo y comentarios
            response_data = {
                "vehicle_info": vehicle_data,
                "comments": comments_data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Vehicle.DoesNotExist:
            return Response({"detail": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)

# Crear un nuevo cliente
class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]

# Listado de Clientes
class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]
