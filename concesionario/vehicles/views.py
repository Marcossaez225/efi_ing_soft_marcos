# vehicles/views.py
from django.views.generic import ListView, DetailView, CreateView
from .models import Vehicle

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'  # Asegúrate de que el nombre de la plantilla es correcto
    context_object_name = 'vehicles'

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'  # Asegúrate de que el nombre de la plantilla es correcto
    context_object_name = 'vehicle'

class VehicleCreateView(CreateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'  # Crea esta plantilla para el formulario
    fields = [
        'brand', 'model', 'year_of_manufacture', 'number_of_doors',
        'engine_displacement', 'fuel_type', 'country_of_manufacture', 'price_in_usd'
    ]
