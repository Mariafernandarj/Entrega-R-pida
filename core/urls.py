from django.urls import path
from . import views

urlpatterns = [
    # redirige a la pagina principal
    path('principal/', views.pagina_principal, name='pagina_principal'), 
]