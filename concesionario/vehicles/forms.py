# vehicles/forms.py

from django import forms
from .models import Vehicle, Brand
from media.models import VehicleImage  # Importa el modelo de imágenes

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'brand', 'model', 'year_of_manufacture', 'number_of_doors',
            'engine_displacement', 'fuel_type', 'country_of_manufacture', 'price_in_usd'
        ]

class VehicleSortFilterForm(forms.Form):
    SORT_CHOICES = [
        ('brand', 'Brand'),
        ('price_in_usd', 'Price'),
        ('year_of_manufacture', 'Year'),
    ]
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial='brand')
    min_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10)
    max_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10)
    min_year = forms.IntegerField(required=False)
    max_year = forms.IntegerField(required=False)
    brand = forms.ChoiceField(choices=[('', 'All')], required=False)
    fuel_type = forms.ChoiceField(choices=[('', 'All')], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener opciones de marca mostrando los nombres
        self.fields['brand'].choices += [(brand.id, brand.name) for brand in Brand.objects.all()]
        # Obtener opciones de tipo de combustible
        self.fields['fuel_type'].choices += [(ft, ft) for ft in Vehicle.objects.values_list('fuel_type', flat=True).distinct()]

# Formulario para la subida de imágenes
class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ['image']
