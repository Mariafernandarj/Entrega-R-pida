from django.contrib import admin

# Register your models here.
from .models import Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_usuario', 'contrasena', 'tipo_usuario')