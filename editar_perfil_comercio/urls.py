from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.ver_perfil, name='perfil_comercio'),
    path('perfil/editar/', views.editar_perfil, name='editar_comercio'),
    path('editar/cliente/', views.editar_cliente, name='editar_cliente'),
    path('editar/repartidor/', views.editar_repartidor, name='editar_repartidor'),
]