from django.urls import path
from . import views

urlpatterns = [
    # Ruta para ver el historial
    path('historial/', views.historial_pedidos, name='historial_pedidos'),
]