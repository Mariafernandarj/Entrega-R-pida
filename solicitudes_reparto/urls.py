from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('test/', views.test_base, name='test_base'),
    path('solicitudes_de_reparto/', views.solicitudes_de_reparto, name='solicitudes_de_reparto'),
    path('ver_pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('aceptar/<int:pedido_id>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('logout/', views.ver_pedidos, name='logout')
    
]
