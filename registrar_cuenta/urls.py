from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.seleccionar_tipo, name='seleccionar_tipo'),
    path('registro/<str:tipo>/', views.formulario_registro, name='formulario_registro'),
]