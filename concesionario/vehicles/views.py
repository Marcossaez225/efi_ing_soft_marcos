# vehicles/views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Vehicle, FollowedVehicle
from media.models import VehicleImage
from .forms import VehicleForm, VehicleSortFilterForm, VehicleImageForm
from comments.forms import CommentForm
from comments.views import get_ordered_comments

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
        
        # Añadir la imagen principal de cada vehículo al contexto
        vehicles_with_images = []
        for vehicle in context['vehicles']:
            main_image = vehicle.images.filter(is_main=True).first()
            if not main_image:
                main_image = vehicle.images.first()  # Si no hay una imagen principal, usar la primera
            vehicle.main_image = main_image
            vehicles_with_images.append(vehicle)
        context['vehicles'] = vehicles_with_images
        
        return context

class VehicleDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.get_object()

        # Obtener la imagen principal (portada) o la primera imagen disponible
        main_image = vehicle.images.filter(is_main=True).first()
        if not main_image:
            main_image = vehicle.images.first()

        context['main_image'] = main_image
        context['comments'] = get_ordered_comments(vehicle)
        context['images'] = vehicle.images.all()
        context['form'] = CommentForm()

        # Formulario de subida de imágenes
        if self.request.user.is_staff:
            context['image_form'] = VehicleImageForm()

        # Verificar si el usuario sigue el vehículo
        if self.request.user.is_authenticated:
            context['is_followed'] = FollowedVehicle.objects.filter(user=self.request.user, vehicle=vehicle).exists()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Obtén el objeto Vehicle
        if request.user.is_staff:
            image_form = VehicleImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                vehicle_image = image_form.save(commit=False)
                vehicle_image.vehicle = self.object  # Asigna el vehículo al que pertenece la imagen
                vehicle_image.save()  # Guarda la nueva imagen
                return redirect('vehicle_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)  # Si no es una solicitud POST válida, realiza la solicitud GET habitual

    def test_func(self):
        # Solo permite a los usuarios staff (administradores) subir imágenes
        return self.request.user.is_staff

    def handle_no_permission(self):
        # Redirige a la página de inicio si el usuario no tiene permisos
        return redirect('home')

class VehicleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    form_class = VehicleForm

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

def follow_vehicle(request, vehicle_id):
    """
    Permite a un usuario autenticado seguir un vehículo.

    Parámetros:
        request: La solicitud HTTP.
        vehicle_id: El ID del vehículo a seguir.

    Retorna:
        Redirige a la página de detalles del vehículo seguido.
    """
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    FollowedVehicle.objects.get_or_create(user=request.user, vehicle=vehicle)
    return redirect('vehicle_detail', pk=vehicle.id)

def unfollow_vehicle(request, vehicle_id):
    """
    Permite a un usuario autenticado dejar de seguir un vehículo.

    Parámetros:
        request: La solicitud HTTP.
        vehicle_id: El ID del vehículo a dejar de seguir.

    Retorna:
        Redirige a la página de detalles del vehículo.
    """
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    followed_vehicle = FollowedVehicle.objects.filter(user=request.user, vehicle=vehicle).first()
    if followed_vehicle:
        followed_vehicle.delete()
    return redirect('vehicle_detail', pk=vehicle.id)
