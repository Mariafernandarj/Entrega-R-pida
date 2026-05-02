from django.contrib import admin
from .models import Pedido, Restaurante
# Register your models here.

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado', 'fecha_creacion', 'fecha_creacion')
    list_filter = ('estado',)
    search_fields = ('id',)
    # Solo permite editar el estado desde el admin
    fields = ('restaurante', 'repartidor', 'estado')
    
@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
