# vehicles/admin.py

from django.contrib import admin
from .models import Brand, Country, Vehicle
from media.models import VehicleImage

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1  # Número de formularios vacíos para nuevas imágenes
    fields = ['image', 'is_main']
    max_num = 8  # Máximo de imágenes permitidas por vehículo

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('get_brand_name', 'get_country_name', 'model', 'engine_displacement', 'fuel_type', 'number_of_doors', 'year_of_manufacture', 'price_in_usd')
    inlines = [VehicleImageInline]  # Incluir las imágenes como inlines

    def get_brand_name(self, obj):
        return obj.brand.name
    get_brand_name.short_description = 'Marca'

    def get_country_name(self, obj):
        return obj.country_of_manufacture.name
    get_country_name.short_description = 'País de Fabricación'
