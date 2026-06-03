from navegar_menus.models import Platillo
from django.urls import path
from . import views

urlpatterns = [
    path('busqueda_platillo/', views.buscar_platillo, name='busqueda_platillo'),
    path('restaurante/<int:id_restaurante>/', views.restauranteSeleccionado, name='restaurante_seleccionado'),
]