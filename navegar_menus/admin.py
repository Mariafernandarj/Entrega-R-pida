from django.contrib import admin
from .models import Restaurante, Platillo

@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion')

@admin.register(Platillo)
class PlatilloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'restaurante', 'agotado')