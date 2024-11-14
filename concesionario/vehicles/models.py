from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
import os
from uuid import uuid4

class Brand(models.Model):
    """Modelo que representa una marca de vehículo."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    """Modelo que representa un país."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    """
    Modelo que representa un vehículo.

    Atributos:
        brand: La marca del vehículo.
        model: El modelo del vehículo.
        year_of_manufacture: El año en que se fabricó el vehículo.
        number_of_doors: El número de puertas del vehículo.
        engine_displacement: El desplazamiento del motor del vehículo.
        fuel_type: El tipo de combustible utilizado por el vehículo.
        country_of_manufacture: El país donde se fabricó el vehículo.
        price_in_usd: El precio del vehículo en dólares estadounidenses.
    """

    FUEL_CHOICES = [
        ('electric', 'Electric'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('gasoline', 'Gasoline'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="vehicles")
    model = models.CharField(max_length=100)
    year_of_manufacture = models.IntegerField(
        validators=[
            MinValueValidator(1886),  # Año del primer automóvil moderno
            MaxValueValidator(datetime.now().year)  # Año actual como máximo
        ]
    )
    number_of_doors = models.PositiveIntegerField()
    engine_displacement = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[
            MinValueValidator(0.1),  # Mínimo de 0.1 litros
        ]
    )
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    country_of_manufacture = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="manufactured_vehicles")
    price_in_usd = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year_of_manufacture})"

    def get_absolute_url(self):
        return reverse('vehicle_detail', kwargs={'pk': self.pk})

class FollowedVehicle(models.Model):
    """
    Modelo que representa la relación entre un usuario y un vehículo seguido.

    Atributos:
        user: El usuario que sigue el vehículo.
        vehicle: El vehículo que está siendo seguido.
        followed_at: La fecha y hora en que el usuario comenzó a seguir el vehículo.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)  # Marca el tiempo de seguimiento

    class Meta:
        unique_together = ('user', 'vehicle')  # Evita duplicados, un usuario no puede seguir el mismo vehículo más de una vez

    def __str__(self):
        return f"{self.user.username} follows {self.vehicle}"

# Modelo Comment que integraba anteriormente en la app comments
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50]  # Muestra solo los primeros 50 caracteres del comentario

# Función de ruta para almacenamiento único de imágenes
def get_file_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    new_filename = f"{uuid4().hex}{extension}"
    return os.path.join(f'images/uploads/{instance.vehicle.id}/', new_filename)

# Modelo VehicleImage que integraba anteriormente en la app media
class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_file_path)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.vehicle.model}"


# vehicles/models.py

class Client(models.Model):
    """Modelo para representar un cliente de la concesionaria."""
    
    # Asociado opcionalmente a un usuario del sistema
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Información básica de contacto
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)  # Email opcional
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    
    # Información adicional
    date_joined = models.DateTimeField(auto_now_add=True)  # Fecha de registro como cliente
    notes = models.TextField(blank=True, null=True)  # Campo para notas sobre el cliente

    def __str__(self):
        return self.full_name or f"Cliente {self.id}"
