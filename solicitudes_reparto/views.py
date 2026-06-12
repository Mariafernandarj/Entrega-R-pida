from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Pedido, Repartidor
from registrar_cuenta.models import Usuario
from django.http import JsonResponse


from django.shortcuts import render

# Create your views here.
def solicitudes_de_reparto(request):
    """Página principal: lista de pedidos disponibles para repartir """
    #Elimina pedidos expirados
    pedidos_expirados = Pedido.objects.filter(
        estado='preparando',
        repartidor__isnull=False,
        fecha_limite__isnull=False,
        fecha_limite__lt = timezone.now()
    )
    
    for pedido in pedidos_expirados:
        pedido.reasignar()

    try:
        repartidor = Repartidor.objects.get(nombre_usuario_repartidor=request.user.username)
        pedidos_disponibles = Pedido.objects.filter(estado='preparando', repartidor=repartidor, fecha_limite__isnull=False)
    except Repartidor.DoesNotExist:
        pedidos_disponibles = Pedido.objects.none()
        
    return render(request, 'solicitudes_de_reparto.html', { 'pedidos': pedidos_disponibles})
    
def aceptar_solicitud(request, pedido_id):
    """Acepta un pedido y lo asigna al repartidor """
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        
        # Verifica si el pedidoexpiró
        if pedido.estado != 'preparando' or pedido.esta_expirado():
            messages.warning(request, "Este pedido ya no está disponible")
            return redirect('solicitudes_de_reparto')
        try:
            #Corrección usanodo el nombre usuario
            repartidor = Repartidor.objects.get(nombre_usuario_repartidor=request.user.username)
            if pedido.repartidor != repartidor:
                messages.error(request, "Este pedido no está asignado a ti.")
                return redirect('solicitudes_de_reparto')
            
            pedido.estado = 'recibido'
            pedido.fecha_limite = None
            pedido.save()
            messages.success(request, f"Pedido #{pedido.id} aceptado y asignado a {repartidor.nombre}.")
            return redirect('ver_pedidos')
        
        except Repartidor.DoesNotExist:
            messages.error(request, f"No puedes aceptar pedidos porque no tiene perfil repartidor :( ")            
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
        estado__in=['entregado_repartidor', 'recibido', 'en_camino', 'entregado_cliente']
    )
    
    return render(request,'ver_pedidos.html',{'pedidos': pedidos})

def cambiar_estado_repartidor(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)

        try:
            mi_repartidor = Repartidor.objects.get(nombre_usuario_repartidor=request.user.username)
        except Repartidor.DoesNotExist:
            messages.error(request, "No tienes perfil de repartidor.")
            return redirect('ver_pedidos')

        if pedido.repartidor != mi_repartidor:
            messages.error(request, "Este pedido no te pertenece.")
            return redirect('ver_pedidos')

        # Verifica expiración antes de cualquier cambio
        if pedido.esta_expirado():
            pedido.reasignar()
            messages.warning(request, "El tiempo expiró. El pedido fue reasignado.")
            return redirect('ver_pedidos')
        nuevo_estado = request.POST.get('estado')

         # Transiciones válidas por estado actual
        TRANSICIONES = {
            'preparando':            ['recibido'],           
            'entregado_repartidor':  ['recibido'],          
            'recibido':              ['en_camino'], 
            'en_camino':             ['entregado_cliente'],
        }

        transiciones_permitidas = TRANSICIONES.get(pedido.estado, [])

        if nuevo_estado not in transiciones_permitidas:
            messages.error(request, f"No puedes cambiar de '{pedido.get_estado_display()}' a '{nuevo_estado}'.")
            return redirect('ver_pedidos')

        pedido.estado = nuevo_estado
        pedido.save()
        messages.success(request, f"Pedido #{pedido.id} actualizado a '{pedido.get_estado_display()}'.")

    return redirect('ver_pedidos')

def historial_entregados(request):
    """Muestra el historial de pedidos que el repartidor ya entregó al cliente"""
    
    try:
        cuenta = Usuario.objects.get(nombre_usuario=request.user.username)
    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')

    if cuenta.tipo_usuario != 'repartidor':
        messages.error(request, "Acceso denegado: Esta área es solo para repartidores.")
        return redirect('principal_repartidor')
        
    # Obtener el perfil del repartidor
    try:
        repartidor = Repartidor.objects.get(nombre_usuario_repartidor=request.user.username)
    except Repartidor.DoesNotExist:
        messages.error(request, "No existe un perfil de repartidor asociado.")
        return redirect('principal_repartidor')
    
    # Filtrar SOLO los pedidos con estado 'entregado_cliente'
    # Usamos order_by('-id') para que los más recientes salgan arriba
    pedidos_entregados = Pedido.objects.filter(
        repartidor=repartidor,
        estado='entregado_cliente'
    ).order_by('-id')

    # AGREGA ESTA LÍNEA PARA DEBUGGEAR:
    print("ESTADOS EN EL HISTORIAL:", [p.estado for p in pedidos_entregados])
    
    return render(request, 'historial_entregados.html', {'pedidos': pedidos_entregados})

def detalle_pedido_modal(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = pedido.detalles.select_related('platillo').all()
    
    return JsonResponse({
        'id': pedido.id,
        'cliente': pedido.cliente.nombre_usuario,
        'direccion': pedido.cliente.direccion or 'No especificada',
        'telefono': pedido.cliente.telefono or 'No especificado',
        'estado': pedido.get_estado_display(),
        'total': str(pedido.total),
        'platillos': [
            {
                'nombre': d.platillo.nombre,
                'cantidad': d.cantidad,
                'subtotal': str(d.subtotal),
            }
            for d in detalles
        ]
    })
