from django.urls import path
from . import views 

urlpatterns = [
    # 👇 Se le añade el '/' al final del patrón de la URL
    path('principal_restaurante/', views.principal_restaurante, name='principal_restaurante'),
]