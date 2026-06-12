from django.urls import path
from . import views

urlpatterns = [
    #  poner 'api/' al inicio del nombre porque devuelve datos (JSON) y no pantallas (HTML)
    path('api/revisar/', views.revisar_pedidos_nuevos, name='api_revisar_pedidos'),
]