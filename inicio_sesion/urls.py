from django.urls import path
from . import views

urlpatterns = [
    path('', views.iniciar_sesion, name='iniciar_sesion'),
    path('perfil/editar/', views.perfil_comercio, name='perfil_comercio'),
]