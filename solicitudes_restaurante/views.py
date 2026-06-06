from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from solicitudes_reparto.models import Pedido
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
            return redirect('pedidos_restaurante')

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
                return redirect('pedidos_restaurante')

            pedido.save()
            return redirect('pedidos_restaurante')

        except Exception as e:
            print(f"Error al procesar pedido #{pedido_id}: {e}")
            messages.error(request, "Ocurrió un error al procesar el pedido")

    return redirect('pedidos_restaurante')

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
        cuenta = Usuario.objects.get(
            nombre_usuario=request.user.username
        )

        if cuenta.tipo_usuario != 'restaurante':
            messages.error(
                request,
                "Acceso denegado: Esta área es solo para restaurantes."
            )
            return redirect('principal_restaurante')

    except Usuario.DoesNotExist:
        return redirect('iniciar_sesion')

    # Buscar el restaurante asociado
    try:
        restaurante = Restaurante.objects.get(
            nombre_usuario_dueno=request.user.username
        )

    except Restaurante.DoesNotExist:
        messages.error(
            request,
            "No existe un perfil de restaurante asociado a esta cuenta."
        )
        return redirect('principal_restaurante')

    # Obtener pedidos del restaurante
    pedidos = Pedido.objects.filter(
        restaurante=restaurante,
        estado='aceptado'
    )

    return render( request, 'ver_pedidos_restaurante.html',
        { 'pedidos': pedidos }
    )
