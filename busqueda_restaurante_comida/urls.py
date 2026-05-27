from navegar_menus.models import Platillo
from django.urls import path
from . import views

urlpatterns = [
    path('busqueda_platillo/', views.buscar_platillo, name='busqueda_platillo'),
    path('restaurante/<int:id>/', views.restaurante_seleccionado, name='restaurante_seleccionado'),
]