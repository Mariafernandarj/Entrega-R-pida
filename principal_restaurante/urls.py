from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('principal_restaurante', views.principal_restaurante, name='principal_restaurante'),
    
]
