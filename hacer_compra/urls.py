from django.urls import path
from . import views

urlpatterns = [
    # ID para saber el platillo seleccionado
    path('platillo/<int:id_platillo>/', views.platillo_seleccionado, name='platillo_seleccionado'),
    path('carrito/', views.agregar_carrito, name='agregar_carrito'),
    path('pago/', views.pago_producto, name='pago_producto'),
    path('pago/tarjeta/', views.pago_tarjeta, name='pago_tarjeta'),
    path('pago/transferencia/', views.pago_transferencia, name='pago_transferencia'),
]