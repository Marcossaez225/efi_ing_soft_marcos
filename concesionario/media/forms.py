# media/forms.py

from django import forms
from .models import VehicleImage

# Form for uploading vehicle images
class VehicleImageUploadForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ['image']  # Only allows uploading a single image

    def save_image(self, vehicle):
        image = self.cleaned_data.get('image')

        # If an image already exists for the vehicle, update it
        if hasattr(vehicle, 'image'):
            vehicle_image = vehicle.image
            vehicle_image.image = image
            vehicle_image.save()
        else:
            # Create a new image for the vehicle
            VehicleImage.objects.create(vehicle=vehicle, image=image)
