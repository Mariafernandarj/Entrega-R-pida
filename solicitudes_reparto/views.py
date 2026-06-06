from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Pedido, Repartidor
from registrar_cuenta.models import Usuario

from django.shortcuts import render

# Create your views here.
def solicitudes_de_reparto(request):
    """Página principal: lista de pedidos disponibles para repartir """
    #Elimina pedidos expirados
    pedidos_expirados = Pedido.objects.filter(
        estado='pendiente',
        fecha_limite__lt = timezone.now()
    )
    
    for pedido in pedidos_expirados:
        pedido.reasignar()
        
    pedidos_disponibles = Pedido.objects.filter(estado='pendiente')
    return render(request, 'solicitudes_de_reparto.html', { 'pedidos': pedidos_disponibles })
    
def aceptar_solicitud(request, pedido_id):
    """Acepta un pedido y lo asigna al repartidor """
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id = pedido_id)
        
        # Verifica si el pedidoexpiró
        if pedido.estado != 'pendiente' or pedido.esta_expirado():
            messages.warning(request, "Este pedido ya no está disponible")
            return redirect('solicitudes_de_reparto')
        try:
            #Corrección usanodo el nombre usuario
            repartidor = Repartidor.objects.get(nombre_usuario_repartidor=request.user.username)
            pedido.repartidor = repartidor
            pedido.estado = 'aceptado'
            pedido.save()

            messages.success(
                request,
                f"Pedido #{pedido.id} aceptado y asignado a {repartidor.nombre}."
            )
            return redirect('ver_pedidos')
        
        except Repartidor.DoesNotExist:
            messages.error(
                request,
                 f"No puedes aceptar pedidos porque no tiene perfil repartidor :( "
            )            
        except Exception as e:
            #Error al guardar
            print(f"Error al aceptar pedido #{pedido_id}: {e}")
            messages.error(request, "Ocurrió un error al aceptar el pedido")
        
    return redirect('solicitudes_de_reparto')

def ver_pedidos(request):
    # Verificar qué rol tiene el usuario realmente
    try:
        cuenta = Usuario.objects.get(nombre_usuario=request.user.username)
        
    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')

    if cuenta.tipo_usuario != 'repartidor':
        messages.error(
            request,
            "Acceso denegado: Esta área es solo para repartidores."
        )
        return redirect('principal_repartidor')
        
    try:
        repartidor = Repartidor.objects.get(nombre_usuario_repartidor=request.user.username)

    except Repartidor.DoesNotExist:
        messages.error(request, "No existe un perfil de repartidor asociado.")
        return redirect('principal_repartidor')
    
    pedidos = Pedido.objects.filter(
        repartidor=repartidor,
        estado='aceptado'
    )
    
    return render(
        request,
        'ver_pedidos.html',
        {'pedidos': pedidos}
    )

def test_base(request):
    return render(request, "test_base.html")
