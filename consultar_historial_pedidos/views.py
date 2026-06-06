from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from registrar_cuenta.models import Usuario
from solicitudes_reparto.models import Pedido, Repartidor
from navegar_menus.models import Restaurante

@login_required(login_url='iniciar_sesion')
def historial_pedidos(request):
    
    # se ve que es el usuario que ha iniciado sesion (restaurante, cliente o repartidor)
    usuario_actual = Usuario.objects.filter(nombre_usuario=request.user.username).first()
    
    if not usuario_actual:
        return redirect('pagina_principal')

    # Inicise inicializa una lista vacía de pedidos
    pedidos = []

    # depende de su tipo de usuario
    if usuario_actual.tipo_usuario == 'cliente':
        # se muestra solo los pedidos de este cliente
        pedidos = Pedido.objects.filter(cliente=usuario_actual).order_by('-fecha_creacion')

    elif usuario_actual.tipo_usuario == 'restaurante':
        # busca el restaurante que se llame igual que este usuario
        mi_restaurante = Restaurante.objects.filter(nombre=request.user.username).first()
        if mi_restaurante:
            # muestra todos los pedidos que se le ha hecho a este restaurante especifico
            pedidos = Pedido.objects.filter(restaurante=mi_restaurante).order_by('-fecha_creacion')

    elif usuario_actual.tipo_usuario == 'repartidor':
        # busca el perfil de repartidor vinculado a este usuario
        mi_repartidor = Repartidor.objects.filter(nombre_usuario_repartidor=request.user.username).first()
        if mi_repartidor:
            # muestra los pedidos que se le ha asignado
            pedidos = Pedido.objects.filter(repartidor=mi_repartidor).order_by('-fecha_creacion')

    # se manda los pedidos y el tipo de usuario al HTML
    contexto = {
        'pedidos': pedidos,
        'tipo_usuario': usuario_actual.tipo_usuario #para ocultar o mostrar cosas en el HTML
    }

    return render(request, 'consultar_historial_pedidos.html', contexto)