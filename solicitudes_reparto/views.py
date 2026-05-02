from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Pedido

from django.shortcuts import render

# Create your views here.

@login_required
def solicitudes_de_reparto(request):
    """Página principal: lista de pedidos disponibles para repartir """
    #Elimina pedidos expirados
    Pedido.objects.filter(
        estado='pendiente',
        fecha_limite__lt = timezone.now()
    ).update(estado = 'expirado')

    pedidos_disponibles = Pedido.objects.filter(estado='pendiente')
    return render(request, 'solicitudes_de_reparto.html', { 'pedidos': pedidos_disponibles })
    
@login_required
def aceptar_solicitud(request, pedido_id):
    """Acepta un pedido y lo asigna al repartidor """
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id = pedido_id, estado = 'pendiente')
        # Verifica si el pedidoexpiró
        if pedido.esta_expirado():
            messages.warning(request, "Este pedido ya no está disponible")
            return redirect('solicitudes_de_reparto')
        try:
            if not hasattr(request.user, 'repartidor'):
                messages.error(request, 'No tienes perfil de repartidor')
                return redirect('solicitudes_de_reparto')
            pedido.repartidor = request.user.repartidor ##Puede cambiar depende del modelooo ojoooo##
            pedido.estado = 'pendiente'
            pedido.save()
            messages.success(request, "Pedido aceptado correctamente")
            return redirect('ver_pedidos')
        except Exception as e:
            #Error al guardar
            print(e)
            messages.error(request, "Ocurrió un error al aceptar el pedido")
        
    return redirect('solicitudes_de_reparto')

@login_required
def ver_pedidos(request):
    """Muestra los pedidos asignados al repartidor actual"""
    pedidos = Pedido.objects.filter(
        repartidor = request.user.repartidor,
        estado = 'asignado'
    )
    return render(request, 'ver_pedidos.html', {'pedidos': pedidos})

def test_base(request):
    return render(request, "test_base.html")
