from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from solicitudes_reparto.models import Pedido
from solicitudes_reparto.views import cambiar_estado_repartidor
from navegar_menus.models import Restaurante
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from registrar_cuenta.models import Usuario

def procesar_pedido_restaurante(request, pedido_id):
    """El restaurante acepta o rechaza un pedido según disponibilidad de insumos"""
    
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)

        # Validar que el pedido siga pendiente (pero SIN expiración)
        if pedido.estado != 'pendiente':
            messages.warning(request, "Este pedido ya fue procesado.")
            return redirect('solicitudes_restaurante')

        try:
            # Suponiendo que mandas desde el frontend una acción: 'aceptar' o 'rechazar'
            accion = request.POST.get('accion')

            if accion == 'aceptar':
                pedido.estado = 'aceptado'
                messages.success(
                    request,
                    f"Pedido #{pedido.id} aceptado por el restaurante."
                )

            elif accion == 'rechazar':
                pedido.estado = 'rechazado'
                messages.info(
                    request,
                    f"Pedido #{pedido.id} rechazado por falta de insumos."
                )

            else:
                messages.error(request, "Acción no válida.")
                return redirect('solicitudes_restaurante')

            pedido.save()
            return redirect('solicitudes_restaurante')

        except Exception as e:
            print(f"Error al procesar pedido #{pedido_id}: {e}")
            messages.error(request, "Ocurrió un error al procesar el pedido")

    return redirect('solicitudes_restaurante')

def solicitudes_restaurante(request):
    try:
        # Buscamos el perfil del restaurante de este usuario específico
        mi_restaurante = Restaurante.objects.get(nombre_usuario_dueno=request.user.username)
        
        # Filtramos los pedidos para que solo vea los suyos
        # (Asegúrate de que en models.py de Pedido el campo se llame 'restaurante')
        pedidos = Pedido.objects.filter(estado='pendiente', restaurante=mi_restaurante)
    except Restaurante.DoesNotExist:
        # Si no tiene restaurante, no tiene pedidos (o puedes crearlo automáticamente aquí también)
        pedidos = []
        messages.warning(request, "No tienes un perfil de restaurante configurado.")

    return render(request, 'solicitudes_restaurante.html', {
        'pedidos': pedidos
    })

def ver_pedidos_restaurante(request):
    # Verificar que exista el usuario
    try:
        cuenta = Usuario.objects.get(nombre_usuario=request.user.username)

        if cuenta.tipo_usuario != 'restaurante':
            messages.error(request, "Acceso denegado: Esta área es solo para restaurantes.")
            return redirect('principal_restaurante')

    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')

    # Buscar el restaurante asociado
    try:
        restaurante = Restaurante.objects.get( nombre_usuario_dueno=request.user.username )
    except Restaurante.DoesNotExist:
        messages.error(request, "No existe un perfil de restaurante asociado a esta cuenta.")
        return redirect('principal_restaurante')

    # Obtener pedidos del restaurante
    pedidos = Pedido.objects.filter(
        restaurante=restaurante,
        #estado='aceptado'
        estado__in=['aceptado', 'preparando', 'entregado_repartidor', 'rechazado']
    )

    return render( request, 'ver_pedidos_restaurante.html',
        { 'pedidos': pedidos }
    )

def cambiar_estado_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)

        try:
            mi_restaurante = Restaurante.objects.get(nombre_usuario_dueno=request.user.username)
        except Restaurante.DoesNotExist:
            messages.error(request, "No tienes un perfil de restaurante.")
            return redirect('solicitudes_restaurante')

        if pedido.restaurante != mi_restaurante:
            messages.error(request, "No tienes permiso para modificar este pedido.")
            return redirect('solicitudes_restaurante')

        # Estados que el restaurante puede asignar
        ESTADOS_PERMITIDOS = ['aceptado', 'rechazado', 'preparando', 'entregado_repartidor']

        nuevo_estado = request.POST.get('estado')

        if nuevo_estado not in ESTADOS_PERMITIDOS:
            messages.error(request, "Estado no válido.")
            return redirect('ver_pedidos_restaurante')
        pedido.estado = nuevo_estado
        pedido.save()

        if nuevo_estado == 'entregado_repartidor':
            repartidor = pedido.asignar_repartidor()
            if repartidor:
                messages.success(request, f"Pedido #{pedido.id} enviado a repartidor: {repartidor.nombre}." )
            else:
                messages.warning(request, f"Pedido #{pedido.id} listo, pero no hay repartidores disponibles.")
        else:
            messages.success(request, f"Pedido #{pedido.id} actualizado a '{pedido.get_estado_display()}'.")

    return redirect('ver_pedidos_restaurante')
