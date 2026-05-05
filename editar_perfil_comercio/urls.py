from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.ver_perfil, name='perfil_comercio'),
    path('perfil/editar/', views.editar_perfil, name='editar_comercio'),
]