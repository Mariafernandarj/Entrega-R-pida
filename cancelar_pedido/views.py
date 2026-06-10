from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from solicitudes_reparto.models import Pedido

@login_required(login_url='iniciar_sesion')
def cancelar_mi_pedido(request, pedido_id):
    # se busca el pedido exacto usando el id
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # verificar si aun se puede cancelar
    estados_prohibidos = ['En camino', 'Entregado', 'Cancelado']
    
    if pedido.estado.lower() in estados_prohibidos:
        # Si ya avanzo mucho, mandamos un mensaje de error y no hacemos nada
        messages.error(request, f'No puedes cancelar el pedido #{pedido.id} porque su estado actual es: {pedido.estado}.')
    else:
        # se guarda con la primera en mayúscula o como lo manejen en tu BD
        pedido.estado = 'Cancelado'
        pedido.save()
        messages.success(request, f'¡Tu pedido #{pedido.id} ha sido cancelado exitosamente!')

    # al final, se regresa al usuario a su pantalla de historial
    return redirect('historial_pedidos')