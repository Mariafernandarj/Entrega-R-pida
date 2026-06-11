from django.urls import path
from . import views 

urlpatterns = [
    path('principal_restaurante/', views.principal_restaurante, name='principal_restaurante'),
]
