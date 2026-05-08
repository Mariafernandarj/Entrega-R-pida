from django.urls import path
from . import views

urlpatterns = [
    path('principal/', views.pagina_principal, name='pagina_principal'),
    path('platillo/<int:platillo_id>/', views.detalle_platillo, name='detalle_platillo'),
]