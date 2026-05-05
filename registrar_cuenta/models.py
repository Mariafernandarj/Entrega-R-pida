from django.db import models

# Create your models here.
class Usuario(models.Model):
    TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('repartidor', 'Repartidor'),
        ('restaurante', 'Restaurante'),
    ]

    nombre_usuario = models.CharField(max_length=150, unique=True)
    contrasena = models.CharField(max_length=255)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre_usuario} ({self.tipo_usuario})"