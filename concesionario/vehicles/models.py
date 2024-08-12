from django.db import models
from django.urls import reverse

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    FUEL_CHOICES = [
        ('electric', 'Electric'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('gasoline', 'Gasoline'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="vehicles")
    model = models.CharField(max_length=100)
    year_of_manufacture = models.IntegerField()
    number_of_doors = models.IntegerField()
    engine_displacement = models.DecimalField(max_digits=5, decimal_places=2)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    country_of_manufacture = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="manufactured_vehicles")
    price_in_usd = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year_of_manufacture})"

    def get_absolute_url(self):
        return reverse('vehicle_detail', kwargs={'pk': self.pk})
