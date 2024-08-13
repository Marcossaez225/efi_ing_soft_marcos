# users/urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, ProfileView, unfollow_vehicle

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('unfollow/<int:vehicle_id>/', unfollow_vehicle, name='unfollow_vehicle'),
]
