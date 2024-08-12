# vehicles/views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Vehicle
from comments.forms import CommentForm
from media.models import VehicleImage
from .forms import VehicleForm, VehicleSortFilterForm

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = VehicleSortFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['sort_by']:
                queryset = queryset.order_by(form.cleaned_data['sort_by'])
            if form.cleaned_data['min_price']:
                queryset = queryset.filter(price_in_usd__gte=form.cleaned_data['min_price'])
            if form.cleaned_data['max_price']:
                queryset = queryset.filter(price_in_usd__lte=form.cleaned_data['max_price'])
            if form.cleaned_data['min_year']:
                queryset = queryset.filter(year_of_manufacture__gte=form.cleaned_data['min_year'])
            if form.cleaned_data['max_year']:
                queryset = queryset.filter(year_of_manufacture__lte=form.cleaned_data['max_year'])
            if form.cleaned_data['brand']:
                queryset = queryset.filter(brand=form.cleaned_data['brand'])
            if form.cleaned_data['fuel_type']:
                queryset = queryset.filter(fuel_type=form.cleaned_data['fuel_type'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VehicleSortFilterForm(self.request.GET or None)
        
        # Añadir la primera imagen de cada vehículo al contexto
        vehicles_with_images = []
        for vehicle in context['vehicles']:
            vehicle.image = vehicle.images.first()  # Obtén la primera imagen como representativa
            vehicles_with_images.append(vehicle)
        context['vehicles'] = vehicles_with_images
        
        return context

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.get_object()
        context['comments'] = vehicle.comments.all()  # Asegúrate de que los comentarios están siendo agregados al contexto
        context['images'] = vehicle.images.all()  # Agregar imágenes al contexto
        return context

class VehicleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    form_class = VehicleForm
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        vehicle = self.object
        
        # Manejar la imagen cargada
        image = self.request.FILES.get('image')
        if image:
            VehicleImage.objects.create(vehicle=vehicle, image=image)
        
        return response

class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    form_class = VehicleForm
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Manejar la imagen cargada
        image = self.request.FILES.get('image')
        if image:
            VehicleImage.objects.create(vehicle=self.object, image=image)
        
        return response
