from django.db import models

class Restaurante(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='restaurantes/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Platillo(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='platillos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.ImageField(upload_to='platillos/', blank=True, null=True)
    agotado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre