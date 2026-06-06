from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models import Count
from registrar_cuenta.models import Usuario
from navegar_menus.models import Restaurante, Platillo

def default_fecha_limite():
    return timezone.now() + timedelta(minutes=3)
    
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
        ('preparando', 'En preparación'),
        ('entregado_repartidor', 'Entregado a repartidor'),
        ('recibido', 'Recibido'),
        ('en_camino', 'En camino'),
        ('entregado_cliente','Entregado al cliente'),
        ('expirado', 'Expirado'),
    ]

    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos_cliente')
    restaurante = models.ForeignKey('navegar_menus.Restaurante', on_delete=models.CASCADE)
    repartidor = models.ForeignKey('Repartidor', null=True, blank=True, on_delete=models.SET_NULL)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    pagado = models.BooleanField(default=False) #cambia a verdadero cuando se le da en aceptar desde pago tarjeta/transferencia
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField(default=default_fecha_limite)

    def esta_expirado(self):
        return timezone.now() > self.fecha_limite
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.estado}"

    def reasignar(self):
        from django.db.models import Count, Q
        nuevo_repartidor = Repartidor.objects.exclude(
            id=self.repartidor.id 
        ).annotate(
            pedidos_activos=Count('pedido',filter=Q(pedido__estado='aceptado'))
        ).order_by('pedidos_activos').first()

        if nuevo_repartidor:
            self.repartidor = nuevo_repartidor
            self.estado = 'pendiente' 
            self.save()
            return True
        return False 
        
    class Meta:
        ordering = ['-fecha_creacion']
    
class Repartidor(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Reemplazamos el OneToOneField por un campo de texto para mantener el vínculo lógico con Usuario
    nombre_usuario_repartidor = models.CharField(max_length=150, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    @staticmethod
    def obtener_pedido_disponible():
        return Repartidor.objects.annotate(
            pedidos_activos=Count(
                'pedido',
                filter=models.Q(pedido__estado__in=['aceptado', 'en camino'])
            )
        ).order_by('pedidos_activos').first()
        
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad}x {self.platillo.nombre} (Pedido #{self.pedido.id})"