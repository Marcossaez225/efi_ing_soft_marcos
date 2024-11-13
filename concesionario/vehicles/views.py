from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Vehicle, FollowedVehicle, Comment, VehicleImage
from .forms import VehicleForm, VehicleSortFilterForm, VehicleImageForm, CommentForm
import logging

logger = logging.getLogger(__name__)

# Vista para listar vehículos
class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Aplica filtros y ordenamiento
        form = VehicleSortFilterForm(self.request.GET or None)
        if form.is_valid():
            # Ordenar por la opción seleccionada en el formulario
            sort_by = form.cleaned_data.get('sort_by')
            if sort_by:
                queryset = queryset.order_by(sort_by)
            
            # Filtrar por rango de precios
            min_price = form.cleaned_data.get('min_price')
            if min_price is not None:
                queryset = queryset.filter(price_in_usd__gte=min_price)
                
            max_price = form.cleaned_data.get('max_price')
            if max_price is not None:
                queryset = queryset.filter(price_in_usd__lte=max_price)
                
            # Filtrar por rango de años
            min_year = form.cleaned_data.get('min_year')
            if min_year is not None:
                queryset = queryset.filter(year_of_manufacture__gte=min_year)
                
            max_year = form.cleaned_data.get('max_year')
            if max_year is not None:
                queryset = queryset.filter(year_of_manufacture__lte=max_year)
                
            # Filtrar por marca y tipo de combustible
            brand = form.cleaned_data.get('brand')
            if brand:
                queryset = queryset.filter(brand__id=brand)
                
            fuel_type = form.cleaned_data.get('fuel_type')
            if fuel_type:
                queryset = queryset.filter(fuel_type=fuel_type)
        
        # Añade la imagen principal a cada vehículo en el queryset
        for vehicle in queryset:
            main_image = vehicle.images.filter(is_main=True).first() or vehicle.images.first()
            vehicle.main_image = main_image

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VehicleSortFilterForm(self.request.GET or None)
        return context


# Vista de detalles de un vehículo
class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.get_object()

        # Obtener la imagen principal o la primera imagen disponible
        main_image = vehicle.images.filter(is_main=True).first() or vehicle.images.first()
        context['main_image'] = main_image
        context['comments'] = vehicle.comments.order_by('-created_at')
        context['images'] = vehicle.images.all()
        context['form'] = CommentForm()

        # Formulario de subida de imágenes solo para administradores
        if self.request.user.is_staff:
            context['image_form'] = VehicleImageForm()

        # Verificar si el usuario sigue el vehículo
        if self.request.user.is_authenticated:
            context['is_followed'] = FollowedVehicle.objects.filter(user=self.request.user, vehicle=vehicle).exists()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_staff:
            image_form = VehicleImageForm(request.POST, request.FILES)
            if image_form.is_valid():
                vehicle_image = image_form.save(commit=False)
                vehicle_image.vehicle = self.object
                vehicle_image.save()
                return redirect('vehicle_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)

# Vistas de comentarios
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'vehicles/comment_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        form.instance.vehicle = vehicle
        form.save()
        return redirect('vehicle_detail', pk=vehicle_id)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'vehicles/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('vehicle_detail', kwargs={'pk': self.object.vehicle.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'vehicles/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('vehicle_detail', kwargs={'pk': self.object.vehicle.pk})

# Vista para subir imágenes
class ImageUploadView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'vehicles/image_upload.html'
    form_class = VehicleImageForm

    def form_valid(self, form):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
        try:
            form.save_image(vehicle)
            messages.success(self.request, "Image has been successfully uploaded.")
            logger.debug(f"Image uploaded for vehicle ID: {vehicle_id}")
        except Exception as e:
            messages.error(self.request, "An error occurred while uploading the image.")
            logger.error(f"Error uploading image: {e}")
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        vehicle_id = self.kwargs.get('vehicle_id')
        return reverse_lazy('vehicle_detail', kwargs={'pk': vehicle_id})

    def test_func(self):
        return self.request.user.is_staff

# Vista para crear un vehículo
class VehicleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    form_class = VehicleForm

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)
        image = self.request.FILES.get('image')
        if image:
            VehicleImage.objects.create(vehicle=self.object, image=image)
        return response

# Vista para actualizar un vehículo
class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    form_class = VehicleForm

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        response = super().form_valid(form)
        image = self.request.FILES.get('image')
        if image:
            VehicleImage.objects.create(vehicle=self.object, image=image)
        return response

# Vistas para seguir y dejar de seguir un vehículo
def follow_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    FollowedVehicle.objects.get_or_create(user=request.user, vehicle=vehicle)
    return redirect('vehicle_detail', pk=vehicle.id)

def unfollow_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    FollowedVehicle.objects.filter(user=request.user, vehicle=vehicle).delete()
    return redirect('vehicle_detail', pk=vehicle.id)
