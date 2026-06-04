from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path(
        'solicitudes_restaurante/',
        views.solicitudes_restaurante,
        name='solicitudes_restaurante'
    ),
    path(
        'procesar_pedido_restaurante/<int:pedido_id>/',
        views.procesar_pedido_restaurante,
        name='procesar_pedido_restaurante'
    ),
]
