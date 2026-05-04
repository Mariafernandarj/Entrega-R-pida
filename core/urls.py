from django.urls import path
from . import views

urlpatterns = [
    # Le damos el name='pagina_principal' exacto que pide tu redirect
    path('principal/', views.pagina_principal, name='pagina_principal'), 
]