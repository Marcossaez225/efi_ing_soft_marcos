# comments/views.py

from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Comment
from .forms import CommentForm
from vehicles.models import Vehicle

def get_ordered_comments(vehicle):
    # Ordenar comentarios de más reciente a más antiguo
    return Comment.objects.filter(vehicle=vehicle).order_by('-created_at')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'  # No será necesario si el formulario está en línea

    def form_valid(self, form):
        # Asignar el usuario y el vehículo al comentario
        form.instance.user = self.request.user
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        form.instance.vehicle = vehicle
        form.save()
        return redirect('vehicle_detail', pk=vehicle_id)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'

    def test_func(self):
        # Verificar si el usuario tiene permiso para editar
        comment = self.get_object()
        return self.request.user == comment.user or self.request.user.is_staff

    def get_success_url(self):
        # Redirigir a la página de detalles del vehículo
        vehicle_id = self.object.vehicle.pk
        return reverse_lazy('vehicle_detail', kwargs={'pk': vehicle_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegúrate de pasar el vehículo al contexto
        context['vehicle'] = self.object.vehicle
        return context

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment_confirm_delete.html'  # Para confirmación de eliminación

    def test_func(self):
        # Verificar si el usuario tiene permiso para eliminar
        comment = self.get_object()
        return self.request.user == comment.user or self.request.user.is_staff

    def get_success_url(self):
        # Redirigir a la página de detalles del vehículo
        vehicle_id = self.object.vehicle.pk
        return reverse_lazy('vehicle_detail', kwargs={'pk': vehicle_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle'] = self.object.vehicle  # Añadir vehículo al contexto
        return context
