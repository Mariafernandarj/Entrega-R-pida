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
    path(
        'ver_pedidos_restaurante/',
        views.ver_pedidos_restaurante,
        name='ver_pedidos_restaurante'
    ),
    path(
        'cambiar_estado_pedido/<int:pedido_id>/',
        views.cambiar_estado_pedido,
        name='cambiar_estado_pedido'
    ),
]
