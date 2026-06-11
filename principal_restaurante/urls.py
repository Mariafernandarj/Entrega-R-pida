from django.urls import path
from . import views 

urlpatterns = [
    path('principal_restaurante/', views.principal_restaurante, name='principal_restaurante'),
    path('gestion_menu/', views.gestion_menu, name='gestion_menu'),
    path('gestion_menu/agregar/', views.agregar_platillo, name='agregar_platillo'),
    path('gestion_menu/editar/<int:platillo_id>/', views.editar_platillo, name='editar_platillo'),
    path('gestion_menu/disponibilidad/<int:platillo_id>/', views.cambiar_disponibilidad, name='cambiar_disponibilidad'),
]

