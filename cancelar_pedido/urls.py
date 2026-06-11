from django.urls import path
from . import views

urlpatterns = [
    # <int:pedido_id> para atrapar el número exacto del pedido que el cliente quiere cancelar
    path('<int:pedido_id>/', views.cancelar_mi_pedido, name='cancelar_mi_pedido'),
]