from django.urls import path
from . import views

urlpatterns = [
    path('resultados/', views.buscar_comida, name='buscar_comida'),
    path('restaurante/<int:id>/', views.restaurante_seleccionado, name='restaurante_seleccionado'),
]