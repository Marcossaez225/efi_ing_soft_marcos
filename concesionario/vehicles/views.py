from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from .models import Vehicle
from comments.models import Comment
from comments.forms import CommentForm

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = self.get_object()
        context['comments'] = vehicle.comments.all() 
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        vehicle = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.vehicle = vehicle
            comment.user = request.user
            comment.save()
            return redirect('vehicle_detail', pk=vehicle.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class VehicleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    fields = [
        'brand', 'model', 'year_of_manufacture', 'number_of_doors',
        'engine_displacement', 'fuel_type', 'country_of_manufacture', 'price_in_usd'
    ]
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    fields = [
        'brand', 'model', 'year_of_manufacture', 'number_of_doors',
        'engine_displacement', 'fuel_type', 'country_of_manufacture', 'price_in_usd'
    ]
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')
