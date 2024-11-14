from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Vehicle, Brand, VehicleImage, Comment

# Formulario para crear y actualizar un vehículo
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'brand', 'model', 'year_of_manufacture', 'number_of_doors',
            'engine_displacement', 'fuel_type', 'country_of_manufacture', 'price_in_usd'
        ]
        labels = {
            'brand': _('Brand'),
            'model': _('Model'),
            'year_of_manufacture': _('Year of Manufacture'),
            'number_of_doors': _('Number of Doors'),
            'engine_displacement': _('Engine Displacement'),
            'fuel_type': _('Fuel Type'),
            'country_of_manufacture': _('Country of Manufacture'),
            'price_in_usd': _('Price (USD)'),
        }

# Formulario para ordenar y filtrar vehículos en la lista
class VehicleSortFilterForm(forms.Form):
    SORT_CHOICES = [
        ('brand', _('Brand')),
        ('price_in_usd', _('Price')),
        ('year_of_manufacture', _('Year')),
    ]
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, initial='brand', label=_('Sort By'))
    min_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label=_('Min Price'))
    max_price = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label=_('Max Price'))
    min_year = forms.IntegerField(required=False, label=_('Min Year'))
    max_year = forms.IntegerField(required=False, label=_('Max Year'))
    brand = forms.ChoiceField(choices=[('', _('All'))], required=False, label=_('Brand'))
    fuel_type = forms.ChoiceField(choices=[('', _('All'))], required=False, label=_('Fuel Type'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].choices += [(brand.id, brand.name) for brand in Brand.objects.all()]
        self.fields['fuel_type'].choices += [(ft, ft) for ft in Vehicle.objects.values_list('fuel_type', flat=True).distinct()]

# Formulario para subir imágenes de vehículos
class VehicleImageUploadForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ['image']
        labels = {
            'image': _('Image')
        }

    def save_image(self, vehicle):
        image = self.cleaned_data.get('image')
        if hasattr(vehicle, 'image'):
            vehicle_image = vehicle.image
            vehicle_image.image = image
            vehicle_image.save()
        else:
            VehicleImage.objects.create(vehicle=vehicle, image=image)

# Formulario para agregar y editar comentarios
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': _('Comment')
        }

# Formulario de imagen para asignar a los vehículos en su detalle
class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ['image']
        labels = {
            'image': _('Image')
        }
