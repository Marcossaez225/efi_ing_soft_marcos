# comments/urls.py

from django.urls import path
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('create/<int:vehicle_id>/', CommentCreateView.as_view(), name='comment_create'),
    path('update/<int:pk>/', CommentUpdateView.as_view(), name='comment_update'),
    path('delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
]
