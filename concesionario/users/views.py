from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.utils import translation
from .forms import UserRegistrationForm, UserLoginForm

# Access the FollowedVehicle model using apps.get_model
FollowedVehicle = apps.get_model('vehicles', 'FollowedVehicle')

# View for user registration
class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Display a success message on successful registration
        response = super().form_valid(form)
        messages.success(self.request, "Registration successful. You can now log in.")
        return response

# View for user login
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'


# View for user logout
class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        # Display a success message on successful logout
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)

# View for displaying the user's profile
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve vehicles followed by the authenticated user
        context['followed_vehicles'] = FollowedVehicle.objects.filter(user=self.request.user).select_related('vehicle')
        return context

class UpdateLang(View):
    def get(self, request):
        # Alternar idioma entre 'es' y 'en'
        current_lang = request.LANGUAGE_CODE
        new_lang = 'es' if current_lang == 'en' else 'en'

        # Almacena la preferencia en la sesión del usuario
        translation.activate(new_lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = new_lang

        return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unfollow_vehicle_from_profile(request, vehicle_id):
    """
    Allows an authenticated user to unfollow a vehicle.

    Parameters:
        request: The HTTP request.
        vehicle_id: The ID of the vehicle to unfollow.

    Returns:
        Redirects to the user's profile page.
    """
    followed_vehicle = FollowedVehicle.objects.filter(user=request.user, vehicle_id=vehicle_id).first()
    if followed_vehicle:
        followed_vehicle.delete()
    return redirect('profile')