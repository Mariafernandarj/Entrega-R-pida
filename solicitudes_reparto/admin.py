from django.contrib import admin
from .models import Pedido, Repartidor
# Register your models here.

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado', 'fecha_creacion', 'fecha_creacion', 'pagado')
    list_filter = ('estado',)
    search_fields = ('id',)
    # Solo permite editar el estado desde el admin
    fields = ('restaurante', 'repartidor', 'estado')

@admin.register(Repartidor)
class RepartidorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'nombre_usuario_repartidor') 
    search_fields = ('nombre', 'user__username')
