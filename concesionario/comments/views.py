# comments/views.py

from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Comment
from .forms import CommentForm
from vehicles.models import Vehicle

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        vehicle_id = self.kwargs.get('vehicle_id')
        form.instance.vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vehicle_detail', kwargs={'pk': self.object.vehicle.pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('vehicle_detail', kwargs={'pk': self.object.vehicle.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('vehicle_detail', kwargs={'pk': self.object.vehicle.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir el vehículo al contexto
        context['vehicle'] = self.object.vehicle
        return context
