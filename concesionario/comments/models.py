# comments/models.py

from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle  # Importa directamente el modelo Vehicle

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, related_name='comments', on_delete=models.CASCADE)  # Añade related_name='comments'
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:50]  # Muestra solo los primeros 50 caracteres del comentario
