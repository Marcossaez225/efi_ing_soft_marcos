# users/views.py

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps
from .forms import UserRegistrationForm, UserLoginForm

# Acceder al modelo FollowedVehicle usando apps.get_model
FollowedVehicle = apps.get_model('vehicles', 'FollowedVehicle')

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful. You can now log in.")
        return response

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)

class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener los vehículos seguidos por el usuario autenticado
        context['followed_vehicles'] = FollowedVehicle.objects.filter(user=self.request.user).select_related('vehicle')
        return context

@login_required
def unfollow_vehicle_from_profile(request, vehicle_id):
    """
    Permite a un usuario autenticado dejar de seguir un vehículo.

    Parámetros:
        request: La solicitud HTTP.
        vehicle_id: El ID del vehículo a dejar de seguir.

    Retorna:
        Redirige a la página de perfil del usuario.
    """
    followed_vehicle = FollowedVehicle.objects.filter(user=request.user, vehicle_id=vehicle_id).first()
    if followed_vehicle:
        followed_vehicle.delete()
    return redirect('profile')
