from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
# Create your models here.

# Método que define el tiempo lmite de espera de cada pedido a 3 minutos
def default_fecha_limite():
    return timezone.now() + timedelta(minutes=3)
    
# Estados posibles de cada pedido
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('preparando', 'En preparación'),
        ('entregado_repartidor', 'Entregado a repartidor'),
        ('recibido', 'Recibido'),
        ('en_camino', 'En camino'),
        ('entregado_cliente','Entregado al cliente'),
        ('expirado', 'Expirado'),
    ]

    # Relaciones con otros modelos
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE)
    repartidor = models.ForeignKey('Repartidor', null=True, blank=True, on_delete=models.SET_NULL)

    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    fecha_limite = models.DateTimeField(default=default_fecha_limite)

    #Método que nos dice si un pedido está o no expirado
    def esta_expirado(self):
        return timezone.now() > self.fecha_limite
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.estado}"

    class Meta:
        ordering = ['-fecha_creacion']

class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Repartidor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    @staticmethod
    def obtener_pedido_disponible():
        """Devuelve el repartidor con menos pedidos activos"""
        return Repartidor.objects.annotate(
            pedidos_activos=Count(
                'pedido',
                filter=models.Q(pedido__estado__in=['aceptado', 'en camino'])
            )
        ).order_by('pedidos_activos').first()
