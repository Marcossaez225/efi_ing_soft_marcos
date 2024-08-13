from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

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
