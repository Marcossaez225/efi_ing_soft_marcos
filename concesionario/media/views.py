# media/views.py

from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import VehicleImageUploadForm
from vehicles.models import Vehicle
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import logging

logger = logging.getLogger(__name__)

class ImageUploadView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'media/image_upload.html'
    form_class = VehicleImageUploadForm

    def form_valid(self, form):
        vehicle_id = self.kwargs.get('vehicle_id')
        vehicle = Vehicle.objects.get(pk=vehicle_id)
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
