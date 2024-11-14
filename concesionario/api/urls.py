# api/urls.py
from django.urls import path
from api.views.views import BrandListView, VehicleListView, UserListView, VehicleCommentListView

app_name = "api" 

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('vehicles/<int:vehicle_id>/comments/', VehicleCommentListView.as_view(), name='vehicle-comments'),
]
